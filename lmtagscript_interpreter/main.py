
import re
import json

def parse_tagscript(content):
    """Parse TagScript content and return structured JSON"""
    lines = content.split('\n')
    result = {}
    current_block = None
    if_blocks = []
    api_calls = []
    llm_references = []
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line or line.startswith('#'):
            i += 1
            continue
            
        # Parse TAG statements
        if line.startswith('TASK:'):
            result['task'] = line[5:].strip()
        elif line.startswith('ACTION:'):
            result['action'] = line[7:].strip()
        elif line.startswith('GOAL:'):
            result['goal'] = line[5:].strip()
            
        # Parse IF statements
        elif line.startswith('IF'):
            if_match = re.match(r'IF\s+(.+?)\s+THEN', line)
            if if_match:
                condition = if_match.group(1)
                if_block = {
                    'condition': parse_condition(condition),
                    'then': '',
                    'else': ''
                }
                current_block = 'if_then'
                if_blocks.append(if_block)
                
        elif line.startswith('ELSE'):
            current_block = 'if_else'
            
        elif line.startswith('END'):
            current_block = None
            
        # Parse API calls
        elif line.startswith('CALL API'):
            api_match = re.match(r'CALL API\s+(.+?)\s+WITH\s+(.+)', line)
            if api_match:
                service_endpoint = api_match.group(1)
                payload = api_match.group(2)
                
                # Check if it's an LLM reference
                if '@' in service_endpoint:
                    llm_ref = parse_llm_reference(service_endpoint)
                    api_calls.append({
                        'type': 'llm_api',
                        'reference': llm_ref,
                        'payload': parse_json_like(payload)
                    })
                else:
                    service, endpoint = service_endpoint.split('.', 1)
                    api_calls.append({
                        'service': service,
                        'endpoint': endpoint,
                        'payload': parse_json_like(payload)
                    })
                    
        # Parse LLM references (@)
        elif line.startswith('@'):
            # Check if parameters span multiple lines
            llm_ref, consumed_lines = parse_llm_reference_multiline(lines, i)
            llm_references.append(llm_ref)
            i += consumed_lines - 1  # -1 because we'll increment i at the end
            
        # Parse FOR loops
        elif line.startswith('FOR EACH'):
            for_match = re.match(r'FOR EACH\s+(.+?)\s+IN\s+(.+?)\s+DO', line)
            if for_match:
                variable = for_match.group(1)
                collection = for_match.group(2)
                result['for_loop'] = {
                    'variable': variable,
                    'collection': collection
                }
                
        # Parse ON ERROR
        elif line.startswith('ON ERROR'):
            result['error_handling'] = True
            
        # Handle block content
        elif current_block == 'if_then' and if_blocks:
            if_blocks[-1]['then'] += line + '\n'
        elif current_block == 'if_else' and if_blocks:
            if_blocks[-1]['else'] += line + '\n'
            
        i += 1
            
    # Add parsed structures to result
    if if_blocks:
        result['if_blocks'] = if_blocks
    if api_calls:
        result['api_calls'] = api_calls
    if llm_references:
        result['llm_references'] = llm_references
        
    return result

def parse_llm_reference_multiline(lines, start_index):
    """Parse LLM reference that might span multiple lines"""
    line = lines[start_index].strip()
    content = line[1:]  # Remove @
    
    # Parse different types of LLM references
    if content.startswith('tool:'):
        return parse_tool_reference_multiline(lines, start_index)
    elif content.startswith('file:'):
        return parse_file_reference_multiline(lines, start_index)
    elif content.startswith('project:'):
        return parse_project_reference_multiline(lines, start_index)
    elif content.startswith('db:'):
        return parse_database_reference_multiline(lines, start_index)
    else:
        return {'type': 'unknown', 'content': content}, 1

def parse_tool_reference_multiline(lines, start_index):
    """Parse tool reference (@tool:...) with multiline parameters"""
    line = lines[start_index]
    content = line[1:]  # Remove @
    tool_part = content[5:]  # Remove 'tool:'
    
    # Check if parameters are present
    if '{' in tool_part:
        tool_name = tool_part.split('{')[0].strip()
        params, consumed_lines = parse_multiline_json(lines, start_index, tool_part.find('{'))
        return {
            'type': 'tool',
            'tool': tool_name,
            'parameters': params
        }, consumed_lines
    else:
        return {
            'type': 'tool',
            'tool': tool_part.strip()
        }, 1

def parse_file_reference_multiline(lines, start_index):
    """Parse file reference (@file:...) with multiline parameters"""
    line = lines[start_index]
    content = line[1:]  # Remove @
    file_part = content[5:]  # Remove 'file:'
    
    if '{' in file_part:
        file_path = file_part.split('{')[0].strip().strip('"')
        params, consumed_lines = parse_multiline_json(lines, start_index, file_part.find('{'))
        return {
            'type': 'file',
            'path': file_path,
            'parameters': params
        }, consumed_lines
    else:
        return {
            'type': 'file',
            'path': file_part.strip().strip('"')
        }, 1

def parse_project_reference_multiline(lines, start_index):
    """Parse project reference (@project:...) with multiline parameters"""
    line = lines[start_index]
    content = line[1:]  # Remove @
    project_part = content[8:]  # Remove 'project:'
    
    if '{' in project_part:
        project_name = project_part.split('{')[0].strip()
        params, consumed_lines = parse_multiline_json(lines, start_index, project_part.find('{'))
        return {
            'type': 'project',
            'project': project_name,
            'parameters': params
        }, consumed_lines
    else:
        return {
            'type': 'project',
            'project': project_part.strip()
        }, 1

def parse_database_reference_multiline(lines, start_index):
    """Parse database reference (@db:...) with multiline parameters"""
    line = lines[start_index]
    content = line[1:]  # Remove @
    db_part = content[3:]  # Remove 'db:'
    
    if '{' in db_part:
        db_name = db_part.split('{')[0].strip()
        params, consumed_lines = parse_multiline_json(lines, start_index, db_part.find('{'))
        return {
            'type': 'database',
            'database': db_name,
            'parameters': params
        }, consumed_lines
    else:
        return {
            'type': 'database',
            'database': db_part.strip()
        }, 1

def parse_multiline_json(lines, start_index, brace_start):
    """Parse JSON-like parameters that might span multiple lines"""
    params = {}
    consumed_lines = 1
    brace_count = 0
    current_line = lines[start_index]
    
    # Find the starting brace in the current line
    brace_pos = current_line.find('{', brace_start)
    if brace_pos == -1:
        return params, consumed_lines
    
    brace_count = 1
    param_content = current_line[brace_pos + 1:]
    
    # Continue parsing until we find the closing brace
    while brace_count > 0 and start_index + consumed_lines < len(lines):
        if consumed_lines == 1:
            # We're still on the first line
            for char in param_content:
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        break
        else:
            # We're on subsequent lines
            line = lines[start_index + consumed_lines - 1]
            for char in line:
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        break
        
        if brace_count > 0:
            consumed_lines += 1
    
    # Now parse the parameters
    full_param_text = ''
    for i in range(consumed_lines):
        if i == 0:
            full_param_text += param_content
        else:
            full_param_text += lines[start_index + i]
    
    # Remove the closing brace
    full_param_text = full_param_text.rstrip().rstrip('}')
    
    # Parse the parameters
    params = parse_json_like('{' + full_param_text + '}')
    
    return params, consumed_lines

def parse_condition(condition_str):
    """Parse condition string into structured format"""
    operators = ['=', '!=', '<', '>', '<=', '>=']
    for op in operators:
        if op in condition_str:
            parts = condition_str.split(op)
            return {
                'left': parts[0].strip(),
                'operator': op,
                'right': parts[1].strip()
            }
    return {'raw': condition_str}

def parse_json_like(json_str):
    """Parse JSON-like string into Python dict"""
    try:
        # Remove outer braces if present
        if json_str.startswith('{') and json_str.endswith('}'):
            json_str = json_str[1:-1]
        
        # Simple key-value parsing
        result = {}
        pairs = json_str.split(',')
        for pair in pairs:
            if ':' in pair:
                key, value = pair.split(':', 1)
                key = key.strip().strip('"')
                value = value.strip().strip('"')
                result[key] = value
        return result
    except:
        return {'raw': json_str}

def parse_llm_reference(line):
    """Parse LLM reference (@) into structured format"""
    # Remove @ from beginning
    content = line[1:]
    
    # Parse different types of LLM references
    if content.startswith('tool:'):
        return parse_tool_reference(content)
    elif content.startswith('file:'):
        return parse_file_reference(content)
    elif content.startswith('project:'):
        return parse_project_reference(content)
    elif content.startswith('db:'):
        return parse_database_reference(content)
    else:
        return {'type': 'unknown', 'content': content}

def parse_tool_reference(content):
    """Parse tool reference (@tool:...)"""
    # Extract tool name and parameters
    tool_part = content[5:]  # Remove 'tool:'
    
    # Check if parameters are present
    if '{' in tool_part and '}' in tool_part:
        tool_name = tool_part.split('{')[0].strip()
        params_str = tool_part[tool_part.find('{'):tool_part.rfind('}')+1]
        params = parse_json_like(params_str)
        return {
            'type': 'tool',
            'tool': tool_name,
            'parameters': params
        }
    else:
        return {
            'type': 'tool',
            'tool': tool_part.strip()
        }

def parse_file_reference(content):
    """Parse file reference (@file:...)"""
    file_part = content[5:]  # Remove 'file:'
    
    if '{' in file_part and '}' in file_part:
        file_path = file_part.split('{')[0].strip().strip('"')
        params_str = file_part[file_part.find('{'):file_part.rfind('}')+1]
        params = parse_json_like(params_str)
        return {
            'type': 'file',
            'path': file_path,
            'parameters': params
        }
    else:
        return {
            'type': 'file',
            'path': file_part.strip().strip('"')
        }

def parse_project_reference(content):
    """Parse project reference (@project:...)"""
    project_part = content[8:]  # Remove 'project:'
    
    if '{' in project_part and '}' in project_part:
        project_name = project_part.split('{')[0].strip()
        params_str = project_part[project_part.find('{'):project_part.rfind('}')+1]
        params = parse_json_like(params_str)
        return {
            'type': 'project',
            'project': project_name,
            'parameters': params
        }
    else:
        return {
            'type': 'project',
            'project': project_part.strip()
        }

def parse_database_reference(content):
    """Parse database reference (@db:...)"""
    db_part = content[3:]  # Remove 'db:'
    
    if '{' in db_part and '}' in db_part:
        db_name = db_part.split('{')[0].strip()
        params_str = db_part[db_part.find('{'):db_part.rfind('}')+1]
        params = parse_json_like(params_str)
        return {
            'type': 'database',
            'database': db_name,
            'parameters': params
        }
    else:
        return {
            'type': 'database',
            'database': db_part.strip()
        }

if __name__ == "__main__":
    # Read input file
    try:
        with open('input.tag', 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print("Error: input.tag file not found")
        exit(1)
    
    # Parse content
    result = parse_tagscript(content)
    
    # Output JSON
    print(json.dumps(result, indent=2, ensure_ascii=False))
