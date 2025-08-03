# LMTagScript

**LMTagScript** é uma linguagem de domínio específico (DSL) projetada para orquestrar interações com IA com precisão, estrutura e modularidade. Inspirada em linguagens de programação e frameworks de automação como n8n, ela preenche a lacuna entre engenharia de prompts e workflows do mundo real.

## 🚀 Propósito

Definir uma linguagem universal para prompts de IA, orquestração de processos e integração de ferramentas — permitindo que desenvolvedores e não-desenvolvedores construam fluxos inteligentes com clareza e controle.

## 🧱 Princípios Fundamentais

- **TAG**: Task, Action, Goal
- **Modularidade**: Funções e classes reutilizáveis
- **Controle**: Condicionais, loops, triggers, tratamento de erros
- **Conectividade**: Sintaxe nativa para APIs, n8n, webhooks, bancos de dados
- **Segurança**: Loopguard, validação, retry/fallback
- **Referências @**: Acesso direto a ferramentas LLM

## 🔤 Visão Geral da Sintaxe

### Estrutura Básica TAG
```tagscript
TASK: Gerar descrição do produto
ACTION: Usar linguagem persuasiva e mencionar benefícios
GOAL: Ajudar clientes a tomar decisões de compra informadas

CLASS Product
  name: string
  price: float
  description: string

DEFINE FUNCTION summarize(product)
  TASK: Resumir produto
  ACTION: Destacar características principais
  GOAL: Preparar para uso em marketing

CALL summarize(prod1)
```

### Controle de Fluxo
```tagscript
IF stock_available = true THEN
  TASK: Processar pagamento
  ACTION: Chamar API de pagamento
  GOAL: Finalizar transação
ELSE
  TASK: Notificar usuário
  ACTION: Enviar mensagem de estoque esgotado
  GOAL: Informar e reter cliente
END

FOR EACH item IN cart DO
  TASK: Verificar disponibilidade
  ACTION: Consultar sistema de inventário
  GOAL: Determinar nível de estoque
END
```

## 🔗 Referências @ para LLMs

### Visão Geral
As referências `@` permitem que LLMs acessem ferramentas e recursos através de métodos permitidos pelas plataformas, contornando limitações de segurança para links externos.

### Tipos de Referências

#### @tool - Ferramentas e Serviços
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

#### @file - Arquivos e Documentos
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

#### @project - Projetos e Repositórios
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

#### @db - Bancos de Dados
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

## 🔌 Exemplo de Integração Externa

### APIs Tradicionais
```tagscript
CONNECT TO api AS stock_checker {
  url: "https://api.example.com/check",
  token: ENV("API_KEY")
}

CALL API stock_checker.check_stock WITH {
  sku: "ABC-123"
}
ON ERROR
  TASK: Registrar falha
  ACTION: Notificar administrador
  GOAL: Manter confiabilidade
```

### Integração com LLMs via @
```tagscript
CALL API @tool:openai.chat WITH {
  model: "gpt-4",
  messages: [
    {
      role: "user",
      content: "Analise os dados de @db:sales_database e gere insights"
    }
  ]
}
```

## 🔐 Segurança e Confiabilidade

```tagscript
LOOPGUARD {
  max_depth: 3,
  allow_repeat: false
}

ON ERROR
  TASK: Implementar fallback robusto
  ACTION: Usar dados de backup e notificar equipe
  GOAL: Manter continuidade do processo
  
  @tool:backup_storage {
    operation: "retrieve",
    fallback: true
  }
END
```

## 📁 Estrutura do Projeto

```
lmtagscript/
├── lmtagscript_boilerplate/     # Especificação da linguagem
│   ├── grammar/                 # Gramática EBNF
│   ├── examples/                # Exemplos de uso
│   │   ├── comprehensive_llm_example.tag
│   │   ├── simple_llm_example.tag
│   │   └── llm_references_example.tag
│   └── README.md               # Documentação da especificação
├── lmtagscript_interpreter/     # Interpretador Python
│   ├── main.py                 # Parser principal
│   ├── input.tag               # Arquivo de exemplo
│   ├── test_comprehensive.py   # Script de teste
│   └── README.md               # Documentação do interpretador
└── README.md                   # Este arquivo
```

## 🛠️ Como Usar

### Interpretador Python

1. Navegue para o diretório do interpretador:
   ```bash
   cd lmtagscript_interpreter
   ```

2. Edite o arquivo `input.tag` com seu código TagScript

3. Execute o interpretador:
   ```bash
   python main.py
   ```

4. O resultado será exibido em JSON estruturado

### Exemplo Completo com Referências @

```tagscript
TASK: Criar relatório de vendas automatizado
ACTION: Coletar dados de múltiplas fontes e gerar análise
GOAL: Fornecer insights acionáveis para a equipe de vendas

# Acessar Google Drive
@tool:google_drive {
  action: "list_files",
  folder: "1ABC123DEF456",
  filter: "pdf"
}

# Ler dados históricos
@file:"/data/historical_sales.csv" {
  permission: "read",
  format: "csv"
}

# Consultar banco de dados
@db:sales_database {
  query: "SELECT * FROM sales WHERE date >= '2024-01-01'",
  limit: 1000
}

# Processamento condicional
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

# Análise com IA
CALL API @tool:openai.chat WITH {
  model: "gpt-4",
  messages: [
    {
      role: "user",
      content: "Analise os dados e gere um relatório executivo"
    }
  ]
}

# Salvar resultado
@file:"/reports/final_report.pdf" {
  permission: "write",
  format: "pdf"
}
```

### Exemplo de Saída JSON

```json
{
  "task": "Criar relatório de vendas automatizado",
  "action": "Coletar dados de múltiplas fontes e gerar análise",
  "goal": "Fornecer insights acionáveis para a equipe de vendas",
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

## 🛠️ Roadmap de Ferramentas

- [ ] Interpretador em Node.js
- [ ] Playground com parsing em tempo real
- [ ] Compilador TagScript → JSON de prompts
- [ ] Sistema de plugins para ferramentas (n8n, OpenAI, ElevenLabs)
- [ ] CLI runner para execução em lote
- [ ] Integração com Supabase, Vercel, Cloudflare Workers
- [ ] Suporte a mais tipos de referências @
- [ ] Validação avançada de sintaxe
- [ ] Debugger integrado

## 🤝 Contribuindo

Aceitamos contribuições, ideias de funcionalidades, relatórios de problemas e casos de uso.
Comece abrindo uma issue ou pull request.

### Como Contribuir

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📘 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 📚 Recursos Adicionais

- [Especificação da Gramática](lmtagscript_boilerplate/grammar/LMtagscript.ebnf)
- [Exemplos de Uso](lmtagscript_boilerplate/examples/)
- [Documentação do Interpretador](lmtagscript_interpreter/README.md)
- [Guia de Referências @](lmtagscript_boilerplate/README.md#-referências--para-llms)

## ⭐ Estrelas e Apoio

Se este projeto foi útil para você, considere dar uma estrela ⭐ no GitHub!

## 🚀 Sponsor o Projeto

Apoie o desenvolvimento do LMTagScript e ajude a construir a linguagem universal para orquestração de IA!

### 💰 Formas de Apoio

- **PayPal:** alex@marramoncks.com.br
- **Wise:** [https://wise.com/pay/me/alexanderm5339](https://wise.com/pay/me/alexanderm5339)

[![Sponsor](https://img.shields.io/badge/Sponsor-LMTagScript-red?style=for-the-badge)](SPONSOR.md)

Veja mais detalhes em [SPONSOR.md](SPONSOR.md)

---

**LMTagScript** - Orquestrando IA com clareza e controle através de referências @ inteligentes. 