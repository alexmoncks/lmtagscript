# LMTagScript - Language Specification

This directory contains the complete LMTagScript language specification, including grammar, documentation, and examples.

## 📚 Content

- **`grammar/`**: Formal syntax definition in EBNF
- **`examples/`**: Practical usage examples
- **`README.md`**: This documentation

## 🔤 EBNF Grammar

The complete grammar is defined in `grammar/LMtagscript.ebnf` and includes:

### Basic Elements
- **TAG**: Task, Action, Goal
- **Identifiers**: Variable and function names
- **Types**: string, int, float, bool
- **Values**: Strings, numbers, identifiers

### Control Structures
- **Conditionals**: IF/ELSE
- **Loops**: FOR EACH
- **Functions**: DEFINE FUNCTION and CALL
- **Classes**: CLASS with properties

### Integrations
- **APIs**: CALL API
- **Webhooks**: TRIGGER WEBHOOK
- **Connections**: CONNECT TO
- **Error Handling**: ON ERROR

### Security
- **Loopguard**: Infinite loop prevention
- **Validation**: Type and syntax checking

## 📖 Examples

### Basic Example
```tagscript
TASK: Greet the user
ACTION: Use a friendly and concise tone
GOAL: Make a good first impression

CALL API welcome_service.send WITH {
  name: "Alex",
  language: "en"
}
```

### Example with Flow Control
```tagscript
TASK: Process user input
ACTION: Validate and respond
GOAL: Provide helpful feedback

IF user_type = "premium" THEN
  TASK: Provide premium features
  ACTION: Enable advanced options
  GOAL: Enhance user experience
ELSE
  TASK: Show basic features
  ACTION: Display standard options
  GOAL: Guide to upgrade
```

### Example with Classes and Functions
```tagscript
CLASS User
  name: string
  email: string
  is_premium: bool

DEFINE FUNCTION send_welcome(user)
  TASK: Send welcome message
  ACTION: Generate personalized greeting
  GOAL: Create positive first impression

CALL send_welcome(new_user)
```

## 🛠️ How to Use the Specification

### For Developers
1. Read the EBNF grammar in `grammar/LMtagscript.ebnf`
2. Study the examples in `examples/`
3. Implement a parser following the specification
4. Test with the provided examples

### For Users
1. Familiarize yourself with the basic syntax
2. Experiment with the examples
3. Use the Python interpreter to test code
4. Consult documentation for advanced features

## 🔮 Language Roadmap

### Planned Features
- [ ] Module and import support
- [ ] Plugin system
- [ ] Integration with more tools
- [ ] Runtime type validation
- [ ] Debugger and development tools

### Syntax Improvements
- [ ] Comment support
- [ ] Multi-line strings
- [ ] More complex expressions
- [ ] Macros and templates

## 📋 Conventions

### Naming
- **Keywords**: Uppercase (TASK, ACTION, GOAL)
- **Identifiers**: snake_case
- **Classes**: PascalCase
- **Constants**: UPPER_SNAKE_CASE

### Formatting
- Consistent indentation
- Adequate spacing
- Comments when necessary
- Line breaks for readability

## 🤝 Contributing

To contribute to the specification:

1. **Propose improvements**: Open an issue discussing the change
2. **Update grammar**: Modify the EBNF file
3. **Add examples**: Create examples for new features
4. **Test compatibility**: Verify existing examples still work

## 📚 Additional Resources

- [Python Interpreter](../lmtagscript_interpreter/)
- [Main README](../../README.md)
- [Contributing Guide](../../CONTRIBUTING.md)

---

**LMTagScript Specification** - Defining the universal language for AI orchestration. 