
import re
import json
import logging
import argparse
import sys
import os
from typing import Dict, List, Any, Tuple, Optional

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TagScriptParser:
    """Parser principal para TagScript com suporte a estruturas complexas"""
    
    def __init__(self):
        self.result = {}
        self.current_block = None
        self.block_stack = []
        self.if_blocks = []
        self.api_calls = []
        self.llm_references = []
        self.loop_guards = []
        self.variables = {}
        self.functions = []
        self.classes = []
        self.calls = []
        
    def parse(self, content: str) -> Dict[str, Any]:
        """Parse TagScript content and return structured JSON"""
        try:
            lines = content.split('\n')
            self._parse_lines(lines)
            self._finalize_result()
            return self.result
        except Exception as e:
            logger.error(f"Erro durante o parsing: {e}")
            raise
    
    def _parse_lines(self, lines: List[str]) -> None:
        """Parse todas as linhas do TagScript"""
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            if not line or line.startswith('#'):
                i += 1
                continue
            
            try:
                consumed_lines = self._parse_line(line, lines, i)
                i += consumed_lines
            except Exception as e:
                logger.warning(f"Erro ao processar linha {i+1}: {e}")
                i += 1
    
    def _parse_line(self, line: str, lines: List[str], line_index: int) -> int:
        """Parse uma única linha e retorna o número de linhas consumidas"""
        
        # Parse TAG statements (agora suporta múltiplas)
        if line.startswith('TASK:'):
            self._add_tag('task', line[5:].strip())
            return 1
        elif line.startswith('ACTION:'):
            self._add_tag('action', line[7:].strip())
            return 1
        elif line.startswith('GOAL:'):
            self._add_tag('goal', line[5:].strip())
            return 1
            
        # Parse CLASS declarations
        elif line.startswith('CLASS'):
            return self._parse_class_definition(line, lines, line_index)
            
        # Parse DEFINE FUNCTION
        elif line.startswith('DEFINE FUNCTION'):
            return self._parse_function_definition(line, lines, line_index)
            
        # Parse CALL statements
        elif line.startswith('CALL'):
            return self._parse_call_statement(line, lines, line_index)
            
        # Parse IF statements
        elif line.startswith('IF'):
            return self._parse_if_statement(line, lines, line_index)
            
        elif line.startswith('ELSE'):
            self.current_block = 'if_else'
            return 1
            
        elif line.startswith('END'):
            return self._parse_end_statement()
            
        # Parse API calls
        elif line.startswith('CALL API'):
            return self._parse_api_call(line, lines, line_index)
            
        # Parse LLM references (@)
        elif line.startswith('@'):
            return self._parse_llm_reference_multiline(lines, line_index)
            
        # Parse FOR loops
        elif line.startswith('FOR EACH'):
            return self._parse_for_loop(line)
            
        # Parse LOOPGUARD
        elif line.startswith('LOOPGUARD'):
            return self._parse_loopguard(line, lines, line_index)
            
        # Parse ON ERROR
        elif line.startswith('ON ERROR'):
            self.result['error_handling'] = True
            return 1
            
        # Handle block content
        elif self.current_block == 'if_then' and self.if_blocks:
            self.if_blocks[-1]['then'] += line + '\n'
            return 1
        elif self.current_block == 'if_else' and self.if_blocks:
            self.if_blocks[-1]['else'] += line + '\n'
            return 1
            
        return 1
    
    def _add_tag(self, tag_type: str, value: str) -> None:
        """Adiciona uma TAG ao resultado, suportando múltiplas"""
        if tag_type not in self.result:
            self.result[tag_type] = []
        self.result[tag_type].append(value)
    
    def _parse_class_definition(self, line: str, lines: List[str], line_index: int) -> int:
        """Parse CLASS definition"""
        class_match = re.match(r'CLASS\s+(\w+)', line)
        if class_match:
            class_name = class_match.group(1)
            class_def = {
                'name': class_name,
                'properties': {},
                'methods': [],
                'line_number': line_index + 1
            }
            
            # Parse propriedades da classe (linhas seguintes)
            consumed_lines = 1
            i = line_index + 1
            while i < len(lines) and lines[i].strip() and not lines[i].strip().startswith('#'):
                prop_line = lines[i].strip()
                if ':' in prop_line and not prop_line.startswith(('TASK:', 'ACTION:', 'GOAL:', 'IF', 'ELSE', 'END')):
                    key, value = prop_line.split(':', 1)
                    class_def['properties'][key.strip()] = value.strip()
                    consumed_lines += 1
                    i += 1
                else:
                    break
            
            self.classes.append(class_def)
            return consumed_lines
        return 1
    
    def _parse_function_definition(self, line: str, lines: List[str], line_index: int) -> int:
        """Parse DEFINE FUNCTION"""
        func_match = re.match(r'DEFINE FUNCTION\s+(\w+)', line)
        if func_match:
            func_name = func_match.group(1)
            func_def = {
                'name': func_name,
                'task': '',
                'action': '',
                'goal': '',
                'line_number': line_index + 1
            }
            
            # Parse conteúdo da função (TASK, ACTION, GOAL)
            consumed_lines = 1
            i = line_index + 1
            while i < len(lines) and lines[i].strip() and not lines[i].strip().startswith('#'):
                func_line = lines[i].strip()
                if func_line.startswith('TASK:'):
                    func_def['task'] = func_line[5:].strip()
                elif func_line.startswith('ACTION:'):
                    func_def['action'] = func_line[7:].strip()
                elif func_line.startswith('GOAL:'):
                    func_def['goal'] = func_line[5:].strip()
                elif func_line.startswith('END') or func_line.startswith('DEFINE FUNCTION'):
                    break
                consumed_lines += 1
                i += 1
            
            self.functions.append(func_def)
            return consumed_lines
        return 1
    
    def _parse_call_statement(self, line: str, lines: List[str], line_index: int) -> int:
        """Parse CALL statements (chamadas de função)"""
        call_match = re.match(r'CALL\s+(\w+)', line)
        if call_match:
            func_name = call_match.group(1)
            call_def = {
                'function': func_name,
                'arguments': '',
                'line_number': line_index + 1
            }
            
            # Parse argumentos se houver
            if '(' in line and ')' in line:
                args_match = re.search(r'\((.*?)\)', line)
                if args_match:
                    call_def['arguments'] = args_match.group(1).strip()
            
            self.calls.append(call_def)
        return 1
    
    def _parse_if_statement(self, line: str, lines: List[str], line_index: int) -> int:
        """Parse IF statement com suporte a condições complexas"""
        if_match = re.match(r'IF\s+(.+?)\s+THEN', line)
        if if_match:
            condition = if_match.group(1)
            if_block = {
                'condition': self._parse_condition(condition),
                'then': '',
                'else': '',
                'line_number': line_index + 1
            }
            self.current_block = 'if_then'
            self.if_blocks.append(if_block)
            self.block_stack.append('if')
        return 1
    
    def _parse_end_statement(self) -> int:
        """Parse END statement e gerencia o stack de blocos"""
        if self.block_stack:
            block_type = self.block_stack.pop()
            if block_type == 'if':
                self.current_block = None
        return 1
    
    def _parse_api_call(self, line: str, lines: List[str], line_index: int) -> int:
        """Parse CALL API com suporte a payloads complexos"""
        api_match = re.match(r'CALL API\s+(.+?)\s+WITH\s+(.+)', line)
        if api_match:
            service_endpoint = api_match.group(1)
            payload = api_match.group(2)
            
            # Check if it's an LLM reference
            if '@' in service_endpoint:
                llm_ref = self._parse_llm_reference(service_endpoint)
                api_call = {
                    'type': 'llm_api',
                    'reference': llm_ref,
                    'payload': self._parse_json_like(payload)
                }
            else:
                service, endpoint = service_endpoint.split('.', 1)
                api_call = {
                    'service': service,
                    'endpoint': endpoint,
                    'payload': self._parse_json_like(payload)
                }
            
            self.api_calls.append(api_call)
        return 1
    
    def _parse_llm_reference_multiline(self, lines: List[str], start_index: int) -> int:
        """Parse LLM reference que pode abranger múltiplas linhas"""
        line = lines[start_index].strip()
        content = line[1:]  # Remove @
        
        # Parse different types of LLM references
        if content.startswith('tool:'):
            llm_ref, consumed_lines = self._parse_tool_reference_multiline(lines, start_index)
        elif content.startswith('file:'):
            llm_ref, consumed_lines = self._parse_file_reference_multiline(lines, start_index)
        elif content.startswith('project:'):
            llm_ref, consumed_lines = self._parse_project_reference_multiline(lines, start_index)
        elif content.startswith('db:'):
            llm_ref, consumed_lines = self._parse_database_reference_multiline(lines, start_index)
        else:
            llm_ref = {'type': 'unknown', 'content': content}
            consumed_lines = 1
        
        self.llm_references.append(llm_ref)
        return consumed_lines
    
    def _parse_tool_reference_multiline(self, lines: List[str], start_index: int) -> Tuple[Dict, int]:
        """Parse tool reference (@tool:...) com parâmetros multilinha"""
        line = lines[start_index]
        content = line[1:]  # Remove @
        tool_part = content[5:]  # Remove 'tool:'
        
        # Check if parameters are present
        if '{' in tool_part:
            tool_name = tool_part.split('{')[0].strip()
            params, consumed_lines = self._parse_multiline_json(lines, start_index, tool_part.find('{'))
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
    
    def _parse_file_reference_multiline(self, lines: List[str], start_index: int) -> Tuple[Dict, int]:
        """Parse file reference (@file:...) com parâmetros multilinha"""
        line = lines[start_index]
        content = line[1:]  # Remove @
        file_part = content[5:]  # Remove 'file:'
        
        if '{' in file_part:
            file_path = file_part.split('{')[0].strip().strip('"')
            params, consumed_lines = self._parse_multiline_json(lines, start_index, file_part.find('{'))
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
    
    def _parse_project_reference_multiline(self, lines: List[str], start_index: int) -> Tuple[Dict, int]:
        """Parse project reference (@project:...) com parâmetros multilinha"""
        line = lines[start_index]
        content = line[1:]  # Remove @
        project_part = content[8:]  # Remove 'project:'
        
        if '{' in project_part:
            project_name = project_part.split('{')[0].strip()
            params, consumed_lines = self._parse_multiline_json(lines, start_index, project_part.find('{'))
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
    
    def _parse_database_reference_multiline(self, lines: List[str], start_index: int) -> Tuple[Dict, int]:
        """Parse database reference (@db:...) com parâmetros multilinha"""
        line = lines[start_index]
        content = line[1:]  # Remove @
        db_part = content[3:]  # Remove 'db:'
        
        if '{' in db_part:
            db_name = db_part.split('{')[0].strip()
            params, consumed_lines = self._parse_multiline_json(lines, start_index, db_part.find('{'))
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
    
    def _parse_for_loop(self, line: str) -> int:
        """Parse FOR EACH loop"""
        for_match = re.match(r'FOR EACH\s+(.+?)\s+IN\s+(.+?)\s+DO', line)
        if for_match:
            variable = for_match.group(1)
            collection = for_match.group(2)
            self.result['for_loop'] = {
                'variable': variable,
                'collection': collection
            }
        return 1
    
    def _parse_loopguard(self, line: str, lines: List[str], line_index: int) -> int:
        """Parse LOOPGUARD statement com melhor detecção"""
        # Remove 'LOOPGUARD' e parse os parâmetros
        params_str = line[10:].strip()
        if params_str.startswith('{'):
            # Se tem chaves, usa parsing multilinha
            params, consumed_lines = self._parse_multiline_json(lines, line_index, 0)
            if params:
                self.loop_guards.append(params)
            return consumed_lines
        elif params_str:  # Se não tem chaves, tenta parsear como parâmetros simples
            # Parse formato: max_depth: 3, allow_repeat: false
            params = {}
            pairs = params_str.split(',')
            for pair in pairs:
                if ':' in pair:
                    key, value = pair.split(':', 1)
                    key = key.strip()
                    value = value.strip()
                    # Try to parse as number or boolean
                    try:
                        if value.lower() in ['true', 'false']:
                            value = value.lower() == 'true'
                        elif '.' in value:
                            value = float(value)
                        else:
                            value = int(value)
                    except ValueError:
                        pass
                    params[key] = value
            if params:
                self.loop_guards.append(params)
        return 1
    
    def _parse_multiline_json(self, lines: List[str], start_index: int, brace_start: int) -> Tuple[Dict, int]:
        """Parse JSON-like parameters que podem abranger múltiplas linhas com suporte a arrays"""
        params = {}
        consumed_lines = 1
        brace_count = 0
        bracket_count = 0
        current_line = lines[start_index]
        
        # Find the starting brace in the current line
        brace_pos = current_line.find('{', brace_start)
        if brace_pos == -1:
            return params, consumed_lines
        
        brace_count = 1
        param_content = current_line[brace_pos + 1:]
        
        # Continue parsing until we find the closing brace
        while (brace_count > 0 or bracket_count > 0) and start_index + consumed_lines < len(lines):
            if consumed_lines == 1:
                # We're still on the first line
                for char in param_content:
                    if char == '{':
                        brace_count += 1
                    elif char == '}':
                        brace_count -= 1
                    elif char == '[':
                        bracket_count += 1
                    elif char == ']':
                        bracket_count -= 1
                    if brace_count == 0 and bracket_count == 0:
                        break
            else:
                # We're on subsequent lines
                line = lines[start_index + consumed_lines - 1]
                for char in line:
                    if char == '{':
                        brace_count += 1
                    elif char == '}':
                        brace_count -= 1
                    elif char == '[':
                        bracket_count += 1
                    elif char == ']':
                        bracket_count -= 1
                    if brace_count == 0 and bracket_count == 0:
                        break
            
            if brace_count > 0 or bracket_count > 0:
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
        params = self._parse_json_like('{' + full_param_text + '}')
        
        return params, consumed_lines
    
    def _parse_condition(self, condition_str: str) -> Dict[str, Any]:
        """Parse condition string em formato estruturado com suporte a operadores complexos"""
        # Suporte a operadores lógicos
        logical_operators = [' AND ', ' OR ', ' NOT ']
        for op in logical_operators:
            if op in condition_str:
                parts = condition_str.split(op)
                return {
                    'type': 'logical',
                    'operator': op.strip(),
                    'left': self._parse_condition(parts[0]),
                    'right': self._parse_condition(parts[1]) if len(parts) > 1 else None
                }
        
        # Suporte a operadores de comparação
        comparison_operators = ['=', '!=', '<', '>', '<=', '>=', 'IN', 'CONTAINS']
        for op in comparison_operators:
            if op in condition_str:
                parts = condition_str.split(op)
                if len(parts) == 2:
                    return {
                        'type': 'comparison',
                        'left': parts[0].strip(),
                        'operator': op,
                        'right': parts[1].strip()
                    }
        
        # Suporte a funções
        function_match = re.match(r'(\w+)\((.+)\)', condition_str)
        if function_match:
            func_name = function_match.group(1)
            func_args = function_match.group(2)
            return {
                'type': 'function',
                'name': func_name,
                'arguments': [arg.strip() for arg in func_args.split(',')]
            }
        
        return {'type': 'raw', 'value': condition_str}
    
    def _parse_json_like(self, json_str: str) -> Any:
        """Parse JSON-like string em Python dict com suporte a arrays"""
        try:
            # Remove outer braces if present
            if json_str.startswith('{') and json_str.endswith('}'):
                json_str = json_str[1:-1]
            
            # Check if it's an array
            if json_str.startswith('[') and json_str.endswith(']'):
                return self._parse_array_like(json_str)
            
            # Simple key-value parsing
            result = {}
            pairs = json_str.split(',')
            for pair in pairs:
                if ':' in pair:
                    key, value = pair.split(':', 1)
                    key = key.strip().strip('"')
                    value = value.strip().strip('"')
                    
                    # Try to parse as number
                    try:
                        if '.' in value:
                            value = float(value)
                        else:
                            value = int(value)
                    except ValueError:
                        pass
                    
                    result[key] = value
            return result
        except Exception as e:
            logger.warning(f"Erro ao parsear JSON-like: {e}")
            return {'raw': json_str}
    
    def _parse_array_like(self, array_str: str) -> List[Any]:
        """Parse array-like string"""
        try:
            # Remove outer brackets
            content = array_str[1:-1].strip()
            if not content:
                return []
            
            # Split by comma and parse each element
            elements = []
            current_element = ""
            brace_count = 0
            bracket_count = 0
            
            for char in content:
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                elif char == '[':
                    bracket_count += 1
                elif char == ']':
                    bracket_count -= 1
                elif char == ',' and brace_count == 0 and bracket_count == 0:
                    elements.append(current_element.strip())
                    current_element = ""
                    continue
                
                current_element += char
            
            # Add the last element
            if current_element.strip():
                elements.append(current_element.strip())
            
            # Parse each element
            parsed_elements = []
            for element in elements:
                element = element.strip()
                if element.startswith('{') and element.endswith('}'):
                    parsed_elements.append(self._parse_json_like(element))
                elif element.startswith('[') and element.endswith(']'):
                    parsed_elements.append(self._parse_array_like(element))
                else:
                    # Try to parse as number
                    try:
                        if '.' in element:
                            parsed_elements.append(float(element))
                        else:
                            parsed_elements.append(int(element))
                    except ValueError:
                        parsed_elements.append(element.strip('"'))
            
            return parsed_elements
        except Exception as e:
            logger.warning(f"Erro ao parsear array: {e}")
            return []
    
    def _parse_llm_reference(self, line: str) -> Dict[str, Any]:
        """Parse LLM reference (@) em formato estruturado"""
        # Remove @ from beginning
        content = line[1:]
        
        # Parse different types of LLM references
        if content.startswith('tool:'):
            return self._parse_tool_reference(content)
        elif content.startswith('file:'):
            return self._parse_file_reference(content)
        elif content.startswith('project:'):
            return self._parse_project_reference(content)
        elif content.startswith('db:'):
            return self._parse_database_reference(content)
        else:
            return {'type': 'unknown', 'content': content}
    
    def _parse_tool_reference(self, content: str) -> Dict[str, Any]:
        """Parse tool reference (@tool:...)"""
        tool_part = content[5:]  # Remove 'tool:'
        
        if '{' in tool_part and '}' in tool_part:
            tool_name = tool_part.split('{')[0].strip()
            params_str = tool_part[tool_part.find('{'):tool_part.rfind('}')+1]
            params = self._parse_json_like(params_str)
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
    
    def _parse_file_reference(self, content: str) -> Dict[str, Any]:
        """Parse file reference (@file:...)"""
        file_part = content[5:]  # Remove 'file:'
        
        if '{' in file_part and '}' in file_part:
            file_path = file_part.split('{')[0].strip().strip('"')
            params_str = file_part[file_part.find('{'):file_part.rfind('}')+1]
            params = self._parse_json_like(params_str)
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
    
    def _parse_project_reference(self, content: str) -> Dict[str, Any]:
        """Parse project reference (@project:...)"""
        project_part = content[8:]  # Remove 'project:'
        
        if '{' in project_part and '}' in project_part:
            project_name = project_part.split('{')[0].strip()
            params_str = project_part[project_part.find('{'):project_part.rfind('}')+1]
            params = self._parse_json_like(params_str)
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
    
    def _parse_database_reference(self, content: str) -> Dict[str, Any]:
        """Parse database reference (@db:...)"""
        db_part = content[3:]  # Remove 'db:'
        
        if '{' in db_part and '}' in db_part:
            db_name = db_part.split('{')[0].strip()
            params_str = db_part[db_part.find('{'):db_part.rfind('}')+1]
            params = self._parse_json_like(params_str)
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
    
    def _finalize_result(self) -> None:
        """Finaliza o resultado adicionando todas as estruturas parseadas"""
        if self.if_blocks:
            self.result['if_blocks'] = self.if_blocks
        if self.api_calls:
            self.result['api_calls'] = self.api_calls
        if self.llm_references:
            self.result['llm_references'] = self.llm_references
        if self.loop_guards:
            self.result['loop_guards'] = self.loop_guards
        if self.variables:
            self.result['variables'] = self.variables
        if self.functions:
            self.result['functions'] = self.functions
        if self.classes:
            self.result['classes'] = self.classes
        if self.calls:
            self.result['calls'] = self.calls

def parse_tagscript(content: str) -> Dict[str, Any]:
    """Função de conveniência para manter compatibilidade com código existente"""
    parser = TagScriptParser()
    return parser.parse(content)

def main():
    """Função principal com suporte a argumentos de linha de comando"""
    parser = argparse.ArgumentParser(
        description='LMTagScript Parser - Converte arquivos TagScript para JSON',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python main.py                           # Usa input.tag e output.json padrão
  python main.py -i meu_script.tag         # Arquivo de entrada customizado
  python main.py -o resultado.json         # Arquivo de saída customizado
  python main.py -i script.tag -o saida.json  # Ambos customizados
  python main.py -v                         # Modo verbose
  python main.py --pretty                   # JSON formatado com indentação
        """
    )
    
    parser.add_argument(
        '-i', '--input',
        type=str,
        default='input.tag',
        help='Arquivo TagScript de entrada (padrão: input.tag)'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        default='output.json',
        help='Arquivo JSON de saída (padrão: output.json)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Modo verbose com logging detalhado'
    )
    
    parser.add_argument(
        '--pretty',
        action='store_true',
        help='Formata o JSON de saída com indentação'
    )
    
    parser.add_argument(
        '--stdout',
        action='store_true',
        help='Envia a saída para stdout ao invés de arquivo'
    )
    
    parser.add_argument(
        '--encoding',
        type=str,
        default='utf-8',
        help='Encoding dos arquivos (padrão: utf-8)'
    )
    
    args = parser.parse_args()
    
    # Configurar logging baseado no modo verbose
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.info(f"Modo verbose ativado")
    
    # Verificar se o arquivo de entrada existe
    if not os.path.exists(args.input):
        logger.error(f"Arquivo de entrada não encontrado: {args.input}")
        print(f"❌ Erro: Arquivo '{args.input}' não encontrado")
        print(f"💡 Dica: Use -i para especificar um arquivo diferente")
        sys.exit(1)
    
    try:
        # Ler arquivo de entrada
        logger.info(f"Lendo arquivo de entrada: {args.input}")
        with open(args.input, 'r', encoding=args.encoding) as f:
            content = f.read()
        
        # Parsear conteúdo
        logger.info("Iniciando parsing do TagScript")
        result = parse_tagscript(content)
        logger.info("Parsing concluído com sucesso")
        
        # Preparar JSON de saída
        if args.pretty:
            json_output = json.dumps(result, indent=2, ensure_ascii=False)
        else:
            json_output = json.dumps(result, ensure_ascii=False)
        
        # Saída
        if args.stdout:
            # Enviar para stdout
            print(json_output)
            logger.info("Saída enviada para stdout")
        else:
            # Salvar em arquivo
            logger.info(f"Salvando resultado em: {args.output}")
            with open(args.output, 'w', encoding=args.encoding) as f:
                f.write(json_output)
            
            print(f"✅ TagScript parseado com sucesso!")
            print(f"📁 Entrada: {args.input}")
            print(f"📄 Saída: {args.output}")
            print(f"📊 Estruturas encontradas:")
            print(f"   • TASKs: {len(result.get('task', []))}")
            print(f"   • ACTIONs: {len(result.get('action', []))}")
            print(f"   • GOALs: {len(result.get('goal', []))}")
            print(f"   • Referências @: {len(result.get('llm_references', []))}")
            print(f"   • Blocos IF: {len(result.get('if_blocks', []))}")
            print(f"   • Chamadas API: {len(result.get('api_calls', []))}")
            print(f"   • LOOPGUARDs: {len(result.get('loop_guards', []))}")
            print(f"   • Funções: {len(result.get('functions', []))}")
            print(f"   • Classes: {len(result.get('classes', []))}")
            print(f"   • Calls: {len(result.get('calls', []))}")
            
            logger.info("Arquivo de saída salvo com sucesso")
    
    except FileNotFoundError as e:
        logger.error(f"Erro de arquivo: {e}")
        print(f"❌ Erro: {e}")
        sys.exit(1)
    except UnicodeDecodeError as e:
        logger.error(f"Erro de encoding: {e}")
        print(f"❌ Erro de encoding: {e}")
        print(f"💡 Tente usar --encoding para especificar o encoding correto")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Erro durante o parsing: {e}")
        print(f"❌ Erro durante o parsing: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
