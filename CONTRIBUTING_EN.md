# Contributing Guide

Thank you for considering contributing to LMTagScript! This document provides guidelines for contributions.

## 🎯 How to Contribute

### Reporting Bugs

1. Use the bug issue template
2. Include detailed information about the problem
3. Provide steps to reproduce the bug
4. Include system information (OS, Python version, etc.)

### Suggesting Improvements

1. Use the feature request issue template
2. Describe the problem the improvement would solve
3. Propose a specific solution
4. Discuss alternatives considered

### Contributing Code

#### Prerequisites

- Python 3.8+
- Basic knowledge of parsing and programming languages
- Familiarity with EBNF (Extended Backus-Naur Form)

#### Environment Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/lmtagscript.git
   cd lmtagscript
   ```

3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\activate     # Windows
   ```

#### Development Process

1. Create a branch for your feature:
   ```bash
   git checkout -b feature/new-feature
   ```

2. Make your changes following the code guidelines

3. Test your changes:
   ```bash
   cd lmtagscript_interpreter
   python main.py
   ```

4. Commit your changes:
   ```bash
   git add .
   git commit -m "feat: add new feature"
   ```

5. Push to your branch:
   ```bash
   git push origin feature/new-feature
   ```

6. Open a Pull Request

## 📝 Code Guidelines

### Project Structure

- **`lmtagscript_boilerplate/`**: Language specification
  - `grammar/`: EBNF files
  - `examples/`: Usage examples
- **`lmtagscript_interpreter/`**: Interpreter implementation
  - `main.py`: Main parser
  - `input.tag`: Example file

### Code Conventions

#### Python
- Use PEP 8 for code style
- Document functions with docstrings
- Use type hints when appropriate
- Keep functions small and focused

#### TagScript
- Use uppercase for keywords (TASK, ACTION, GOAL)
- Use snake_case for identifiers
- Keep blocks well-indented
- Comment complex code

### Commit Patterns

Use conventional commit format:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `style:` Formatting
- `refactor:` Refactoring
- `test:` Tests
- `chore:` Maintenance

### Examples

```bash
git commit -m "feat: add support for FOR EACH loops"
git commit -m "fix: correct string parsing with quotes"
git commit -m "docs: update README with new examples"
```

## 🧪 Testing

### Testing the Interpreter

1. Create a `.tag` file with your code
2. Run the interpreter:
   ```bash
   python main.py
   ```
3. Verify the JSON output is correct

### Testing the Grammar

1. Validate EBNF syntax
2. Test edge cases
3. Verify compatibility with existing examples

## 📚 Useful Resources

### Documentation
- [EBNF Specification](lmtagscript_boilerplate/grammar/LMtagscript.ebnf)
- [Usage Examples](lmtagscript_boilerplate/examples/)
- [Main README](../README.md)

### Recommended Tools
- Editor with Python support (VS Code, PyCharm)
- Online EBNF validator
- JSON formatter to check output

## 🤝 Review Process

1. **Pull Request**: Clearly describe the changes
2. **Review**: Other contributors will review your code
3. **Feedback**: Respond to comments and make adjustments
4. **Merge**: After approval, your code will be integrated

## 📞 Communication

- Use issues for discussions
- Be respectful and constructive
- Help other contributors
- Keep discussions focused on the project

## 🎉 Recognition

Active contributors will be listed in the project README.

---

Thank you for contributing to LMTagScript! 🚀 