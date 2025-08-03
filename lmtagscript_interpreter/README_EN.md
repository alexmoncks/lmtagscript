# TagScript Interpreter

This is the official initial interpreter for the TagScript language, implemented in Python.

## 🚀 Features

- **TagScript Parser**: Converts TagScript code to structured JSON
- **TAG Support**: Task, Action, Goal
- **Flow Control**: IF/ELSE, FOR EACH
- **API Calls**: Native syntax for integrations
- **Error Handling**: ON ERROR blocks
- **Security**: Loopguard to prevent infinite loops
- **@ References**: Support for LLM tool references

## 📋 Prerequisites

- Python 3.8+
- Only standard Python libraries (no external dependencies)

## 🛠️ How to Use

### Basic Execution

1. Edit the `input.tag` file with your TagScript code
2. Run the interpreter:
   ```bash
   python main.py
   ```
3. The result will be displayed as structured JSON

### TagScript Code Example

```tagscript
TASK: Process purchase
ACTION: Validate user and stock
GOAL: Complete the order

IF stock_available = true THEN
  TASK: Proceed to payment
  ACTION: Call payment API
  GOAL: Finish transaction
ELSE
  TASK: Notify user
  ACTION: Send out-of-stock message
  GOAL: Inform and retain user

CALL API purchase_api.finalize WITH {
  user_id: "12345"
}
ON ERROR
  TASK: Fallback to manual
  ACTION: Log the failed purchase
  GOAL: Prevent loss of order
```

### JSON Output Example

```json
{
  "task": "Process purchase",
  "action": "Validate user and stock",
  "goal": "Complete the order",
  "if_blocks": [
    {
      "condition": {
        "left": "stock_available",
        "operator": "=",
        "right": "true"
      },
      "then": "TASK: Proceed to payment...",
      "else": "TASK: Notify user..."
    }
  ],
  "api_call": {
    "service": "purchase_api",
    "endpoint": "finalize",
    "payload": {
      "user_id": "12345"
    }
  },
  "on_error": "TASK: Fallback to manual..."
}
```

## 🔧 Code Structure

### main.py

The main file contains:

- **Regex Patterns**: To identify TagScript elements
- **parse_tagscript() function**: Converts code to data structure
- **Element Extraction**: TAG, classes, functions, conditionals, etc.

### Supported Elements

- ✅ **TAG**: Task, Action, Goal
- ✅ **Classes**: Data structure definitions
- ✅ **Functions**: DEFINE FUNCTION and CALL
- ✅ **Conditionals**: IF/ELSE
- ✅ **Loops**: FOR EACH
- ✅ **APIs**: CALL API
- ✅ **Errors**: ON ERROR
- ✅ **Security**: LOOPGUARD
- ✅ **@ References**: LLM tool access

## 🧪 Testing

1. Create a `.tag` file with your code
2. Run the interpreter
3. Verify the JSON output is correct
4. Test different language structures

## 🔮 Next Steps

- [ ] More robust syntax validation
- [ ] Support for more data types
- [ ] Integration with real APIs
- [ ] Command line interface
- [ ] Web playground

## 📚 Resources

- [Grammar Specification](../lmtagscript_boilerplate/grammar/LMtagscript.ebnf)
- [Usage Examples](../lmtagscript_boilerplate/examples/)
- [Main README](../README.md)

---

**TagScript Interpreter** - Transforming TagScript code into structured JSON. 