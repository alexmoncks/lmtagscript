# LMTagScript - Language Specification

**LMTagScript** is a domain-specific language (DSL) designed to orchestrate AI interactions with precision, structure, and modularity.

## 🧱 Basic Elements

### TAG - Task, Action, Goal
```tagscript
TASK: Generate product description
ACTION: Use persuasive language and mention benefits
GOAL: Help customers make informed buying decisions
```

### Control Structures
```tagscript
IF condition = true THEN
  TASK: Execute action
  ACTION: Process data
  GOAL: Obtain result
ELSE
  TASK: Alternative action
  ACTION: Fallback
  GOAL: Maintain functionality
END

FOR EACH item IN collection DO
  TASK: Process item
  ACTION: Apply logic
  GOAL: Transform data
END
```

### External Integrations
```tagscript
CONNECT TO api AS service_name {
  url: "https://api.example.com",
  token: ENV("API_KEY")
}

CALL API service_name.endpoint WITH {
  param1: "value1",
  param2: "value2"
}
```

### Security
```tagscript
LOOPGUARD {
  max_depth: 3,
  allow_repeat: false
}

ON ERROR
  TASK: Error handling
  ACTION: Log and notification
  GOAL: Maintain stability
END
```

## 🔗 @ References for LLMs

### Overview
The `@` references allow LLMs to access tools and resources through methods permitted by platforms, bypassing security limitations for external links.

### Reference Types

#### @tool - Tools
```tagscript
@tool:google_drive {
  action: "list_files",
  folder: "1ABC123DEF456",
  filter: "pdf"
}

@tool:spreadsheet {
  operation: "create",
  template: "sales_report"
}
```

#### @file - Files
```tagscript
@file:"/my-project/documents/report.pdf" {
  permission: "read",
  format: "text"
}

@file:"/templates/report-template.xlsx" {
  copy_to: "/reports/",
  name: "report-" + current_date
}
```

#### @project - Projects
```tagscript
@project:lmtagscript {
  access: "read",
  include: ["docs", "examples"]
}

@project:analytics_dashboard {
  components: ["charts", "tables"],
  permissions: "write"
}
```

#### @db - Databases
```tagscript
@db:analytics {
  query: "SELECT * FROM sales WHERE date >= '2024-01-01'",
  limit: 100
}

@db:user_profiles {
  operation: "update",
  where: "user_id = 12345"
}
```

### API Integration
```tagscript
CALL API @tool:openai.chat WITH {
  model: "gpt-4",
  messages: [
    {
      role: "user",
      content: "Analyze data from @db:analytics and generate insights"
    }
  ]
}
```

### Usage in Loops
```tagscript
FOR EACH file IN @tool:google_drive.list_files DO
  TASK: Process file
  ACTION: Extract text and analyze
  GOAL: Identify patterns
  
  @file:file.path {
    extract_text: true,
    save_to: "/processed/"
  }
END
```

### Error Handling
```tagscript
ON ERROR
  TASK: Log access failure
  ACTION: Try alternative method
  GOAL: Ensure continuity
  
  @tool:backup_storage {
    operation: "retrieve",
    fallback: true
  }
END
```

## 📚 Advanced Examples

### Classes and Functions
```tagscript
CLASS Product
  name: string
  price: float
  description: string

DEFINE FUNCTION summarize(product)
  TASK: Summarize product
  ACTION: Highlight key features
  GOAL: Prepare for marketing use

CALL summarize(prod1)
```

### Complete Example with @
```tagscript
TASK: Analyze Google Drive data
ACTION: Use LLM-permitted tools
GOAL: Extract insights from shared documents

# Reference to file in Google Drive
@file:"/my-project/documents/sales-report.pdf" {
  permission: "read",
  format: "text"
}

# Reference to specific tool
@tool:google_drive {
  action: "list_files",
  folder: "1ABC123DEF456",
  filter: "pdf"
}

# Processing with multiple references
TASK: Consolidate information
ACTION: Combine data from different sources
GOAL: Create unified report

IF data_available = true THEN
  @tool:spreadsheet {
    operation: "create",
    template: "sales_report"
  }
  
  @file:"/templates/report-template.xlsx" {
    copy_to: "/reports/",
    name: "report-" + current_date
  }
ELSE
  TASK: Notify error
  ACTION: Send alert
  GOAL: Maintain transparency
END
```

## 🛠️ How to Use the Specification

### For Developers
1. **Implement Parser**: Use the EBNF grammar to create parsers
2. **Add @ Support**: Implement LLM reference parsing
3. **Integrate Tools**: Connect with permitted APIs and services
4. **Test**: Validate with real usage examples

### For Users
1. **Structure Workflows**: Use TAG to organize logic
2. **Integrate Tools**: Use @ to access resources
3. **Handle Errors**: Implement fallbacks and logging
4. **Iterate**: Refine based on results

## 🚀 Language Roadmap

### Planned Features
- [ ] **Template Support**: Reusable macros and snippets
- [ ] **Advanced Validation**: Type checking and linting
- [ ] **Debugging**: Integrated debugging tools
- [ ] **Performance**: Parsing and execution optimizations
- [ ] **Extensibility**: Plugin system for tools

### Syntax Improvements
- [ ] **Regular Expressions**: Native regex support
- [ ] **Advanced Operators**: Mathematical and logical
- [ ] **Interpolation**: Dynamic strings with variables
- [ ] **Modularization**: Import/export modules

## 📋 Conventions

### Naming
- **TAG**: Always uppercase (TASK, ACTION, GOAL)
- **Functions**: camelCase (summarize, processData)
- **Classes**: PascalCase (Product, UserProfile)
- **Variables**: snake_case (user_id, file_path)

### Formatting
- **Indentation**: 2 spaces
- **Comments**: # for single line
- **Strings**: Double quotes for consistency
- **Parameters**: Spaces around operators

## 🤝 Contributing

### How to Contribute
1. **Fork** the repository
2. **Create** a branch for your feature
3. **Implement** your changes
4. **Test** with real examples
5. **Document** new features
6. **Open** a Pull Request

### Focus Areas
- **Parser**: Improve complex syntax parsing
- **@ References**: Expand supported tool types
- **Integrations**: Add support for more APIs
- **Documentation**: Examples and tutorials
- **Tools**: IDEs, debuggers, validators

---

**LMTagScript** - Orchestrating AI with clarity and control through intelligent @ references. 