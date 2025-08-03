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

## 🔤 Syntax Overview

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

## 🔌 External Integration Example

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

## 🔐 Safety & Reliability

```tagscript
LOOPGUARD {
  max_depth: 3,
  allow_repeat: false
}
```

## 📁 Project Structure

```
lmtagscript/
├── lmtagscript_boilerplate/     # Language specification
│   ├── grammar/                 # EBNF grammar
│   ├── examples/                # Usage examples
│   └── README.md               # Specification documentation
├── lmtagscript_interpreter/     # Python interpreter
│   ├── main.py                 # Main parser
│   ├── input.tag               # Example file
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

### Example Output

```json
{
  "task": "Process purchase",
  "action": "Validate user and stock",
  "goal": "Complete the order",
  "api_call": {
    "service": "purchase_api",
    "endpoint": "finalize",
    "payload": {
      "user_id": "12345"
    }
  },
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

**LMTagScript** - Orchestrating AI with clarity and control. 