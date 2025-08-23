# LMTagScript Parser Architecture

## 🏗️ Architecture Overview

The LMTagScript Parser has been completely refactored from a procedural architecture to a robust and extensible object-oriented architecture. This documentation describes the internal structure, design patterns and architectural decisions made.

## 🎯 Design Principles

### **1. Single Responsibility Principle (SRP)**
Each method has a single, well-defined responsibility:
- `_parse_line()`: Parse a single line
- `_parse_if_statement()`: Parse IF declarations
- `_parse_function_definition()`: Parse function definitions

### **2. Open/Closed Principle (OCP)**
The architecture is open for extension but closed for modification:
- New types of structures can be easily added
- Existing methods don't need to be modified for new functionality

### **3. Dependency Inversion Principle (DIP)**
The parser depends on abstractions (interfaces) not concrete implementations:
- Use of generic types (`Dict[str, Any]`, `List[str]`)
- Methods that return standardized structures

## 🏛️ Class Structure

### **Main Class: `TagScriptParser`**

```python
class TagScriptParser:
    """Main parser for TagScript with support for complex structures"""
    
    def __init__(self):
        # Internal parser state
        self.result = {}           # Final parsing result
        self.current_block = None  # Current block being processed
        self.block_stack = []      # Nested block stack
        self.if_blocks = []        # IF/ELSE/END blocks
        self.api_calls = []        # API calls
        self.llm_references = []   # @ references
        self.loop_guards = []      # LOOPGUARD declarations
        self.variables = {}        # Found variables
        self.functions = []        # Defined functions
        self.classes = []          # Defined classes
        self.calls = []            # Function calls
```

## 🔧 Main Methods

### **1. Public Interface Methods**

#### **`parse(content: str) -> Dict[str, Any]`**
- **Responsibility**: Main entry point of the parser
- **Flow**: 
  1. Split content into lines
  2. Call `_parse_lines()` to process each line
  3. Call `_finalize_result()` to finalize the result
  4. Return structured JSON

#### **`_parse_lines(lines: List[str]) -> None`**
- **Responsibility**: Coordinates parsing of all lines
- **Flow**:
  1. Iterate over each line
  2. Call `_parse_line()` for each line
  3. Manage line index and consumed lines
  4. Handle parsing errors with graceful fallback

### **2. Line Parsing Methods**

#### **`_parse_line(line: str, lines: List[str], line_index: int) -> int`**
- **Responsibility**: Parse a single line and route to specific methods
- **Return**: Number of lines consumed
- **Pattern**: Command Pattern - each line type is routed to a specific method

#### **`_add_tag(tag_type: str, value: str) -> None`**
- **Responsibility**: Add TAGs to result, supporting multiple
- **Implementation**: Maintains arrays for each TAG type
- **Benefit**: Preserves all TAGs found, not just the last one

### **3. Structure Parsing Methods**

#### **`_parse_if_statement(line: str, lines: List[str], line_index: int) -> int`**
- **Responsibility**: Parse IF/THEN declarations
- **Features**:
  - Extract condition using regex
  - Create IF block structure
  - Manage block stack
  - Support complex conditions (AND, OR, NOT)

#### **`_parse_function_definition(line: str, lines: List[str], line_index: int) -> int`**
- **Responsibility**: Parse DEFINE FUNCTION
- **Features**:
  - Extract function name
  - Parse TASK, ACTION, GOAL within function
  - Support multiline functions
  - Record line number for debugging

#### **`_parse_class_definition(line: str, lines: List[str], line_index: int) -> int`**
- **Responsibility**: Parse CLASS declarations
- **Features**:
  - Extract class name
  - Parse properties (key: value)
  - Support multiline properties
  - Structure prepared for future methods

#### **`_parse_call_statement(line: str, lines: List[str], line_index: int) -> int`**
- **Responsibility**: Parse CALL statements
- **Features**:
  - Extract called function name
  - Parse arguments if present
  - Support different argument formats

#### **`_parse_loopguard(line: str, lines: List[str], line_index: int) -> int`**
- **Responsibility**: Parse LOOPGUARD with multiple formats
- **Supported formats**:
  - JSON: `LOOPGUARD { max_depth: 3, allow_repeat: false }`
  - Simple: `LOOPGUARD max_depth: 5, allow_repeat: true`
  - Boolean: `LOOPGUARD debug: true, verbose: false`

### **4. Reference Parsing Methods**

#### **`_parse_llm_reference_multiline(lines: List[str], start_index: int) -> int`**
- **Responsibility**: Parse @ references that may span multiple lines
- **Supported types**:
  - `@tool:` - Tools and services
  - `@file:` - Files and documents
  - `@project:` - Projects and repositories
  - `@db:` - Databases

#### **`_parse_multiline_json(lines: List[str], start_index: int, brace_start: int) -> Tuple[Dict, int]`**
- **Responsibility**: Parse multiline JSON with nested braces and brackets support
- **Features**:
  - Count nested braces `{}` and brackets `[]`
  - Support structures spanning multiple lines
  - Robust parsing of complex parameters

### **5. Data Parsing Methods**

#### **`_parse_json_like(json_str: str) -> Any`**
- **Responsibility**: Parse JSON-like strings to Python
- **Features**:
  - Remove external braces if present
  - Detect arrays and objects
  - Parse key-value pairs
  - Automatic type conversion (int, float, bool)

#### **`_parse_array_like(array_str: str) -> List[Any]`**
- **Responsibility**: Parse JSON-like arrays
- **Features**:
  - Support for nested arrays
  - Parse complex elements (objects, arrays)
  - Automatic type conversion
  - Comma and space handling

#### **`_parse_condition(condition_str: str) -> Dict[str, Any]`**
- **Responsibility**: Parse complex conditions in IF structures
- **Supported operators**:
  - Logical: `AND`, `OR`, `NOT`
  - Comparison: `=`, `!=`, `<`, `>`, `<=`, `>=`, `IN`, `CONTAINS`
  - Functions: `function_name(arg1, arg2)`

### **6. Finalization Methods**

#### **`_finalize_result() -> None`**
- **Responsibility**: Finalize result by adding all parsed structures
- **Features**:
  - Add non-empty arrays to result
  - Maintain consistent structure
  - Prepare result for JSON serialization

## 🔄 Parsing Flow

### **1. Initialization**
```python
parser = TagScriptParser()
```

### **2. Main Parsing**
```python
result = parser.parse(content)
```

### **3. Internal Flow**
```
parse() → _parse_lines() → _parse_line() → specific methods → _finalize_result()
```

### **4. Line Routing**
```
Line → _parse_line() → Routing based on prefix:
├── TASK: → _add_tag('task', value)
├── ACTION: → _add_tag('action', value)
├── GOAL: → _add_tag('goal', value)
├── CLASS → _parse_class_definition()
├── DEFINE FUNCTION → _parse_function_definition()
├── CALL → _parse_call_statement()
├── IF → _parse_if_statement()
├── ELSE → current_block = 'if_else'
├── END → _parse_end_statement()
├── CALL API → _parse_api_call()
├── @ → _parse_llm_reference_multiline()
├── FOR EACH → _parse_for_loop()
├── LOOPGUARD → _parse_loopguard()
├── ON ERROR → error_handling = True
└── Others → current block processing
```

## 🧩 Design Patterns Used

### **1. Command Pattern**
Each line type is routed to a specific method:
```python
elif line.startswith('IF'):
    return self._parse_if_statement(line, lines, line_index)
elif line.startswith('DEFINE FUNCTION'):
    return self._parse_function_definition(line, lines, line_index)
```

### **2. State Pattern**
The parser maintains internal state to manage blocks:
```python
self.current_block = 'if_then'  # Current state
self.block_stack.append('if')    # Block stack
```

### **3. Template Method Pattern**
The `parse()` method defines the template, specific methods implement details:
```python
def parse(self, content: str) -> Dict[str, Any]:
    lines = content.split('\n')
    self._parse_lines(lines)        # Template
    self._finalize_result()         # Template
    return self.result
```

### **4. Strategy Pattern**
Different parsing strategies for different content types:
```python
if content.startswith('tool:'):
    return self._parse_tool_reference_multiline(lines, start_index)
elif content.startswith('file:'):
    return self._parse_file_reference_multiline(lines, start_index)
```

## 📊 Data Structure

### **1. Internal State**
```python
{
    'result': {},           # Final result
    'current_block': None,  # Current block
    'block_stack': [],      # Block stack
    'if_blocks': [],        # IF blocks
    'api_calls': [],        # API calls
    'llm_references': [],   # @ references
    'loop_guards': [],      # LOOPGUARDs
    'variables': {},        # Variables
    'functions': [],        # Functions
    'classes': [],          # Classes
    'calls': []             # Calls
}
```

### **2. Output Structure**
```python
{
    'task': ['TASK1', 'TASK2'],
    'action': ['ACTION1', 'ACTION2'],
    'goal': ['GOAL1', 'GOAL2'],
    'if_blocks': [...],
    'functions': [...],
    'classes': [...],
    'calls': [...],
    'llm_references': [...],
    'loop_guards': [...],
    'api_calls': [...],
    'error_handling': true
}
```

## 🔍 Error Handling

### **1. Fallback Strategy**
```python
try:
    consumed_lines = self._parse_line(line, lines, i)
    i += consumed_lines
except Exception as e:
    logger.warning(f"Error processing line {i+1}: {e}")
    i += 1  # Continue with next line
```

### **2. Structured Logging**
```python
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.error(f"Error during parsing: {e}")
```

### **3. Input Validation**
```python
if not os.path.exists(args.input):
    logger.error(f"Input file not found: {args.input}")
    sys.exit(1)
```

## 🚀 Extensibility

### **1. Add New Structure Types**
```python
elif line.startswith('NEW_STRUCTURE'):
    return self._parse_new_structure(line, lines, line_index)

def _parse_new_structure(self, line: str, lines: List[str], line_index: int) -> int:
    # New parser implementation
    return consumed_lines
```

### **2. Add New @ Reference Types**
```python
elif content.startswith('new_type:'):
    return self._parse_new_type_reference_multiline(lines, start_index)

def _parse_new_type_reference_multiline(self, lines: List[str], start_index: int) -> Tuple[Dict, int]:
    # New type implementation
    return reference, consumed_lines
```

### **3. Add New Condition Operators**
```python
# In _parse_condition()
new_operators = ['NEW_OP1', 'NEW_OP2']
for op in new_operators:
    if op in condition_str:
        # New operator implementation
        pass
```

## 📈 Performance Metrics

### **1. Time Complexity**
- **Line parsing**: O(1) - constant
- **File parsing**: O(n) - linear in number of lines
- **Multiline JSON parsing**: O(m) - where m is number of JSON lines

### **2. Space Complexity**
- **Internal state**: O(1) - constant
- **Result**: O(n) - proportional to file size
- **Structure arrays**: O(s) - where s is number of structures

### **3. Implemented Optimizations**
- **Incremental parsing**: Process line by line
- **Early exit**: Stop at malformed structures
- **Regex caching**: Patterns compiled once
- **Output streaming**: For large files

## 🔮 Improvement Roadmap

### **Version 2.1**
- [ ] More rigorous syntax validation
- [ ] Caching of parsed structures
- [ ] Regex pattern optimization

### **Version 2.2**
- [ ] Parallel parsing for large files
- [ ] Plugin system
- [ ] REST API

### **Version 3.0**
- [ ] Support for multiple languages
- [ ] Template system
- [ ] IDE integration

## 📝 Conclusion

The LMTagScript Parser architecture was designed to be:

1. **Robust**: Comprehensive error handling
2. **Extensible**: Easy addition of new functionality
3. **Maintainable**: Well-organized and documented code
4. **Performant**: Optimized for files of different sizes
5. **Testable**: Isolated and well-defined methods

This architecture provides a solid foundation for future parser growth, allowing it to evolve to meet the growing needs of the TagScript community.

---

**LMTagScript Parser Architecture** - Built to grow and evolve! 🚀

*Technical documentation v2.0 - 2025-08-23* 