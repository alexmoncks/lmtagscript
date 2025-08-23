# LMTagScript Parser - Complete Usage Guide

## 🚀 Overview

The LMTagScript Parser is a robust and advanced tool for converting TagScript files into structured JSON. It supports all TagScript structures including @ references, control structures, loops, functions, classes and much more.

## 📋 Complete Features

### ✅ **Basic Features**
- **Complete parsing** of TagScript files
- **@ reference support** (@tool, @file, @project, @db)
- **Control structures** (IF/ELSE/END)
- **Loops** (FOR EACH)
- **LOOPGUARD** with parameters
- **API calls** (CALL API)
- **Error handling** (ON ERROR)

### 🆕 **New Implemented Features**
- **Multiple TAGs support** (TASK, ACTION, GOAL)
- **DEFINE FUNCTION detection** with complete parsing
- **CLASS declarations support** with properties
- **CALL statements detection** (function calls)
- **Enhanced LOOPGUARD** with multiple format support
- **Multiline JSON parsing** with array support
- **Arrays and nested objects support**
- **Detailed logging** (verbose mode)
- **Multiple output formats**

## 🛠️ Installation

```bash
# Clone the repository
git clone <repository-url>
cd lmtagscript_interpreter

# Install dependencies (if needed)
pip install -r requirements.txt
```

## 💻 Basic Usage

### Simple Command
```bash
python main.py
```
- **Input**: `input.tag` (default)
- **Output**: `output.json` (default)

### Custom Files Command
```bash
python main.py -i my_script.tag -o result.json
```

### Formatted Command
```bash
python main.py -i script.tag -o output.json --pretty
```

## 📚 Command Line Parameters

| Parameter | Short Form | Description | Default |
|-----------|-------------|-------------|---------|
| `--input` | `-i` | Input TagScript file | `input.tag` |
| `--output` | `-o` | Output JSON file | `output.json` |
| `--verbose` | `-v` | Verbose mode with detailed logging | `False` |
| `--pretty` | | Format JSON with indentation | `False` |
| `--stdout` | | Send output to stdout | `False` |
| `--encoding` | | File encoding | `utf-8` |
| `--help` | `-h` | Show help | - |

## 🔍 Usage Examples

### 1. Basic Parsing
```bash
# Use default files
python main.py

# Custom input file
python main.py -i script.tag

# Custom output file
python main.py -o result.json
```

### 2. Verbose Mode
```bash
# Enable detailed logging
python main.py -v

# Combine with other parameters
python main.py -i script.tag -o output.json -v
```

### 3. Output Formatting
```bash
# Formatted JSON (indented)
python main.py --pretty

# Output to stdout (terminal)
python main.py --stdout

# Combine formatting and stdout
python main.py --pretty --stdout
```

### 4. Custom Encoding
```bash
# Specify encoding
python main.py --encoding latin-1

# For files with special characters
python main.py -i script_pt.tag --encoding iso-8859-1
```

### 5. Advanced Usage
```bash
# Complete pipeline with formatting
python main.py -i script.tag -o result.json --pretty -v

# Process and send to stdout
python main.py -i script.tag --stdout --pretty

# Save with specific encoding
python main.py -i script.tag -o output.json --encoding utf-8-sig
```

## 📊 Complete Output Structure

The parser generates a structured JSON with the following main sections:

### **Main TAGs (Multiple)**
```json
{
  "task": [
    "Task description 1",
    "Task description 2"
  ],
  "action": [
    "Action to be executed 1",
    "Action to be executed 2"
  ],
  "goal": [
    "Goal 1",
    "Goal 2",
    "Goal 3"
  ]
}
```

### **Control Structures**
```json
{
  "if_blocks": [
    {
      "condition": {
        "type": "logical",
        "operator": "AND",
        "left": {
          "type": "comparison",
          "left": "status",
          "operator": "=",
          "right": "\"active\""
        },
        "right": {
          "type": "comparison",
          "left": "priority",
          "operator": ">",
          "right": "5"
        }
      },
      "then": "then block content",
      "else": "else block content",
      "line_number": 28
    }
  ]
}
```

### **Defined Functions**
```json
{
  "functions": [
    {
      "name": "visualNarrativeDesign",
      "task": "Design a sequential visual story",
      "action": "Identify core message and emotional arc",
      "goal": "A storyboard ready for illustration",
      "line_number": 55
    }
  ]
}
```

### **Classes**
```json
{
  "classes": [
    {
      "name": "Agent",
      "properties": {
        "name": "\"visual-storyteller\"",
        "description": "\"Create visual narratives...\"",
        "color": "\"cyan\"",
        "tools": "[\"Write\", \"Read\", \"MultiEdit\"]"
      },
      "methods": [],
      "line_number": 8
    }
  ]
}
```

### **Function Calls**
```json
{
  "calls": [
    {
      "function": "accessibilityChecklist",
      "arguments": "",
      "line_number": 238
    }
  ]
}
```

### **@ References**
```json
{
  "llm_references": [
    {
      "type": "tool",
      "tool": "WebSearch",
      "parameters": {
        "query": "visual metaphor examples",
        "limit": 5
      }
    }
  ]
}
```

### **LOOPGUARD**
```json
{
  "loop_guards": [
    {
      "max_depth": 3,
      "allow_repeat": false
    }
  ]
}
```

### **API Calls**
```json
{
  "api_calls": [
    {
      "type": "llm_api",
      "reference": {
        "type": "tool",
        "tool": "openai.chat"
      },
      "payload": {}
    }
  ]
}
```

### **Loops and Error Handling**
```json
{
  "for_loop": {
    "variable": "item",
    "collection": "items"
  },
  "error_handling": true
}
```

## 🔧 Advanced Use Cases

### 1. **Development and Debugging**
```bash
# Verbose mode for debugging
python main.py -v --pretty

# Output to stdout for quick analysis
python main.py --stdout
```

### 2. **System Integration**
```bash
# Save to specific file
python main.py -i script.tag -o /path/to/output.json

# Use specific encoding for compatibility
python main.py --encoding ascii
```

### 3. **Batch Processing**
```bash
# Script to process multiple files
for file in *.tag; do
  python main.py -i "$file" -o "${file%.tag}.json" --pretty
done
```

### 4. **Data Pipeline**
```bash
# Process and send to another command
python main.py -i script.tag --stdout | jq '.llm_references'

# Filter only specific references
python main.py -i script.tag --stdout | jq '.llm_references[] | select(.type == "tool")'
```

### 5. **Complex Structure Analysis**
```bash
# Count defined functions
python main.py -i script.tag --stdout | jq '.functions | length'

# List names of all functions
python main.py -i script.tag --stdout | jq '.functions[].name'

# Check classes and their properties
python main.py -i script.tag --stdout | jq '.classes[] | {name, properties}'
```

## 🆕 **New Features in Detail**

### **1. Multiple TAGs Support**
**Before**: The parser captured only the last TAG found
**After**: Now captures all TAGs in arrays

```bash
# Before: only 1 TASK
"task": "Last task found"

# After: all TASKs
"task": [
  "First task",
  "Second task", 
  "Third task"
]
```

### **2. DEFINE FUNCTION Detection**
**New**: Complete parsing of functions defined in TagScript

```tagscript
DEFINE FUNCTION myFunction(context)
  TASK: Process data
  ACTION: Validate and transform
  GOAL: Clean and structured data
```

**Result**:
```json
{
  "functions": [
    {
      "name": "myFunction",
      "task": "Process data",
      "action": "Validate and transform",
      "goal": "Clean and structured data",
      "line_number": 10
    }
  ]
}
```

### **3. CLASS Declarations Support**
**New**: Parsing of class definitions

```tagscript
CLASS Agent
  name: "visual-storyteller"
  description: "Create visual narratives"
  color: "cyan"
  tools: ["Write", "Read", "MultiEdit"]
```

**Result**:
```json
{
  "classes": [
    {
      "name": "Agent",
      "properties": {
        "name": "\"visual-storyteller\"",
        "description": "\"Create visual narratives\"",
        "color": "\"cyan\"",
        "tools": "[\"Write\", \"Read\", \"MultiEdit\"]"
      },
      "methods": [],
      "line_number": 8
    }
  ]
}
```

### **4. CALL Statements Detection**
**New**: Parsing of function calls

```tagscript
CALL accessibilityChecklist()
CALL testVisualStory()
```

**Result**:
```json
{
  "calls": [
    {
      "function": "accessibilityChecklist",
      "arguments": "",
      "line_number": 238
    },
    {
      "function": "testVisualStory",
      "arguments": "",
      "line_number": 239
    }
  ]
}
```

### **5. Enhanced LOOPGUARD**
**Before**: Only support for JSON format `{}`
**After**: Support for multiple formats

```tagscript
# JSON format
LOOPGUARD {
  max_depth: 10,
  allow_repeat: false,
  timeout: 300
}

# Simple format
LOOPGUARD max_depth: 5, allow_repeat: true

# With boolean values
LOOPGUARD max_depth: 3, allow_repeat: false, debug: true
```

**Result**:
```json
{
  "loop_guards": [
    {
      "max_depth": 10,
      "allow_repeat": "false",
      "timeout": 300
    },
    {
      "max_depth": 5,
      "allow_repeat": true
    },
    {
      "max_depth": 3,
      "allow_repeat": false,
      "debug": true
    }
  ]
}
```

## ⚠️ Error Handling

The parser includes robust error handling:

- **File not found**: Clear message with suggestions
- **Encoding error**: Tips to resolve character problems
- **Parsing error**: Detailed logging for debugging
- **Graceful fallback**: Continues processing even with partial errors

## 📝 Logs and Debugging

### Verbose Mode
```bash
python main.py -v
```
- Shows each parsing step
- Detailed logs of each operation
- Useful for debugging and development

### Log Levels
- **INFO**: Normal operations
- **WARNING**: Non-critical problems
- **ERROR**: Errors that prevent parsing
- **DEBUG**: Detailed information (verbose mode)

## 🚀 Performance

- **Optimized parsing** for large files
- **Multiline support** without performance impact
- **Output streaming** for large files
- **Smart caching** for repetitive structures

## 🔮 Future Features

- [ ] **More rigorous syntax validation**
- [ ] **Plugin support** for extensions
- [ ] **Parallel parsing** for very large files
- [ ] **Persistent cache** between executions
- [ ] **REST API** for HTTP usage
- [ ] **Graphical interface** (GUI)

## 📞 Support

For questions, bugs or suggestions:
- Open an issue in the repository
- Consult the complete documentation
- Check the included examples

## 📄 License

This project is under the license specified in the LICENSE file.

---

**LMTagScript Parser** - Transforming TagScript into structured JSON in a robust and efficient way! 🎉

*Version: 2.0 - With all improvements implemented* 