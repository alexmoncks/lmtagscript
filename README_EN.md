# LMTagScript

**LMTagScript** is a domain-specific language (DSL) designed to orchestrate AI interactions with precision, structure, and modularity. Inspired by programming languages and automation frameworks like n8n, it bridges the gap between prompt engineering and real-world workflows.

## 🚀 Purpose

To define a universal language for AI prompting, process orchestration, and tool integration — enabling developers and non-developers to build intelligent flows with clarity and control.

## 🧱 Core Principles

- **TAG**: Task, Action, Goal
- **Modularity**: Reusable functions and classes
- **Control**: Conditionals, loops, triggers, error handling
- **Connectivity**: Native syntax for APIs, n8n, webhooks, databases
- **Safety**: Loopguard, validation, retry/fallback
- **@ References**: Direct access to LLM tools

## 🔤 Syntax Overview

### Basic TAG Structure
```tagscript
TASK: Generate product description
ACTION: Use persuasive language and mention benefits
GOAL: Help customers make informed buying decisions

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

### Flow Control
```tagscript
IF stock_available = true THEN
  TASK: Process payment
  ACTION: Call payment API
  GOAL: Complete transaction
ELSE
  TASK: Notify user
  ACTION: Send out-of-stock message
  GOAL: Inform and retain customer
END

FOR EACH item IN cart DO
  TASK: Check availability
  ACTION: Query inventory system
  GOAL: Determine stock level
END
```

## 🔗 @ References for LLMs

### Overview
The `@` references allow LLMs to access tools and resources through methods permitted by platforms, bypassing security limitations for external links.

### Reference Types

#### @tool - Tools and Services
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

@tool:email_service {
  template: "notification",
  recipients: ["user@example.com"]
}
```

#### @file - Files and Documents
```tagscript
@file:"/documents/report.pdf" {
  permission: "read",
  format: "text"
}

@file:"/templates/template.xlsx" {
  copy_to: "/output/",
  name: "report_2024"
}
```

#### @project - Projects and Repositories
```tagscript
@project:analytics_dashboard {
  access: "read",
  include: ["charts", "tables"]
}

@project:sales_crm {
  access: "read_write",
  components: ["leads", "deals"]
}
```

#### @db - Databases
```tagscript
@db:sales_database {
  query: "SELECT * FROM sales WHERE date >= '2024-01-01'",
  limit: 100
}

@db:analytics_db {
  operation: "update",
  table: "metrics",
  values: {
    "total_revenue": 50000,
    "conversion_rate": 0.15
  }
}
```

## 🔌 External Integration Example

### Traditional APIs
```tagscript
CONNECT TO api AS stock_checker {
  url: "https://api.example.com/check",
  token: ENV("API_KEY")
}

CALL API stock_checker.check_stock WITH {
  sku: "ABC-123"
}
ON ERROR
  TASK: Log failure
  ACTION: Notify admin
  GOAL: Maintain reliability
```

### LLM Integration via @
```tagscript
CALL API @tool:openai.chat WITH {
  model: "gpt-4",
  messages: [
    {
      role: "user",
      content: "Analyze data from @db:sales_database and generate insights"
    }
  ]
}
```

## 🔐 Safety & Reliability

```tagscript
LOOPGUARD {
  max_depth: 3,
  allow_repeat: false
}

ON ERROR
  TASK: Implement robust fallback
  ACTION: Use backup data and notify team
  GOAL: Maintain process continuity
  
  @tool:backup_storage {
    operation: "retrieve",
    fallback: true
  }
END
```

## 📁 Project Structure

```
lmtagscript/
├── lmtagscript_boilerplate/     # Language specification
│   ├── grammar/                 # EBNF grammar
│   ├── examples/                # Usage examples
│   │   ├── comprehensive_llm_example.tag
│   │   ├── simple_llm_example.tag
│   │   └── llm_references_example.tag
│   └── README.md               # Specification documentation
├── lmtagscript_interpreter/     # Python interpreter
│   ├── main.py                 # Main parser
│   ├── input.tag               # Example file
│   ├── test_comprehensive.py   # Test script
│   └── README.md               # Interpreter documentation
└── README.md                   # This file
```

## 🛠️ How to Use

### Python Interpreter

1. Navigate to the interpreter directory:
   ```bash
   cd lmtagscript_interpreter
   ```

2. Edit the `input.tag` file with your TagScript code

3. Run the interpreter:
   ```bash
   python main.py
   ```

4. The result will be displayed as structured JSON

### Complete Example with @ References

```tagscript
TASK: Create automated sales report
ACTION: Collect data from multiple sources and generate analysis
GOAL: Provide actionable insights for the sales team

# Access Google Drive
@tool:google_drive {
  action: "list_files",
  folder: "1ABC123DEF456",
  filter: "pdf"
}

# Read historical data
@file:"/data/historical_sales.csv" {
  permission: "read",
  format: "csv"
}

# Query database
@db:sales_database {
  query: "SELECT * FROM sales WHERE date >= '2024-01-01'",
  limit: 1000
}

# Conditional processing
IF data_quality_score >= 0.8 THEN
  @tool:data_processor {
    operation: "clean_and_validate",
    input: @db:sales_database,
    output: @file:"/processed/clean_data.json"
  }
ELSE
  @tool:data_collector {
    sources: ["crm", "website"],
    timeframe: "last_7_days"
  }
END

# AI analysis
CALL API @tool:openai.chat WITH {
  model: "gpt-4",
  messages: [
    {
      role: "user",
      content: "Analyze the data and generate an executive report"
    }
  ]
}

# Save result
@file:"/reports/final_report.pdf" {
  permission: "write",
  format: "pdf"
}
```

### JSON Output Example

```json
{
  "task": "Create automated sales report",
  "action": "Collect data from multiple sources and generate analysis",
  "goal": "Provide actionable insights for the sales team",
  "llm_references": [
    {
      "type": "tool",
      "tool": "google_drive",
      "parameters": {
        "action": "list_files",
        "folder": "1ABC123DEF456",
        "filter": "pdf"
      }
    },
    {
      "type": "file",
      "path": "/data/historical_sales.csv",
      "parameters": {
        "permission": "read",
        "format": "csv"
      }
    }
  ],
  "api_calls": [
    {
      "type": "llm_api",
      "reference": {
        "type": "tool",
        "tool": "openai.chat"
      },
      "payload": {
        "model": "gpt-4",
        "messages": "..."
      }
    }
  ]
}
```

## 🛠️ Tooling Roadmap

- [ ] Node.js interpreter
- [ ] Real-time parsing playground
- [ ] TagScript → Prompt JSON compiler
- [ ] Plugin system for tools (n8n, OpenAI, ElevenLabs)
- [ ] CLI runner for batch execution
- [ ] Integration with Supabase, Vercel, Cloudflare Workers
- [ ] Support for more @ reference types
- [ ] Advanced syntax validation
- [ ] Integrated debugger

## 🤝 Contributing

We welcome contributions, feature ideas, issue reports, and use cases.
Start by opening an issue or pull request.

### How to Contribute

1. Fork the project
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📘 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📚 Additional Resources

- [Grammar Specification](lmtagscript_boilerplate/grammar/LMtagscript.ebnf)
- [Usage Examples](lmtagscript_boilerplate/examples/)
- [Interpreter Documentation](lmtagscript_interpreter/README.md)
- [@ References Guide](lmtagscript_boilerplate/README_EN.md#-references-for-llms)

## ⭐ Stars and Support

If this project was helpful to you, consider giving it a star ⭐ on GitHub!

## 🚀 Sponsor the Project

Support the development of LMTagScript and help build the universal language for AI orchestration!

### 💰 Ways to Support

- **PayPal:** alex@marramoncks.com.br
- **Wise:** [https://wise.com/pay/me/alexanderm5339](https://wise.com/pay/me/alexanderm5339)

[![Sponsor](https://img.shields.io/badge/Sponsor-LMTagScript-red?style=for-the-badge)](SPONSOR.md)

See more details in [SPONSOR.md](SPONSOR.md)

---

**LMTagScript** - Orchestrating AI with clarity and control through intelligent @ references. 