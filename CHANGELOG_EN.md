# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Complete documentation in Portuguese
- Detailed contributing guide
- Advanced usage examples
- MIT license file
- Organized project structure

## [0.1.0] - 2024-01-XX

### Added
- Initial LMTagScript language specification
- Complete EBNF grammar
- Basic Python interpreter
- TAG element support (Task, Action, Goal)
- Parser for control structures (IF/ELSE, FOR EACH)
- Support for class and function definitions
- Error handling with ON ERROR
- Security system with LOOPGUARD
- External API integration
- Structured JSON conversion

### Supported Features
- ✅ **TAG**: Task, Action, Goal
- ✅ **Classes**: Data structure definitions
- ✅ **Functions**: DEFINE FUNCTION and CALL
- ✅ **Conditionals**: IF/ELSE
- ✅ **Loops**: FOR EACH
- ✅ **APIs**: CALL API
- ✅ **Errors**: ON ERROR
- ✅ **Security**: LOOPGUARD

### Project Structure
- `lmtagscript_boilerplate/`: Language specification
  - `grammar/LMtagscript.ebnf`: EBNF grammar
  - `examples/`: Usage examples
- `lmtagscript_interpreter/`: Python interpreter
  - `main.py`: Main parser
  - `input.tag`: Example file

## [Planned]

### Upcoming Versions
- [ ] More robust syntax validation
- [ ] Support for more data types
- [ ] Real API integration
- [ ] Command line interface
- [ ] Web playground
- [ ] Plugin system
- [ ] Debugger and development tools
- [ ] Module and import support
- [ ] Runtime type validation

---

## Version Notes

### Semantic Versioning
- **MAJOR**: Incompatible API changes
- **MINOR**: Compatible feature additions
- **PATCH**: Compatible bug fixes

### Commit Conventions
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `style:` Formatting
- `refactor:` Refactoring
- `test:` Tests
- `chore:` Maintenance 