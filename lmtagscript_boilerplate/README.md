# LMTagScript - Especificação da Linguagem

**LMTagScript** é uma linguagem de domínio específico (DSL) projetada para orquestrar interações com IA com precisão, estrutura e modularidade.

## 🧱 Elementos Básicos

### TAG - Task, Action, Goal
```tagscript
TASK: Gerar descrição do produto
ACTION: Usar linguagem persuasiva e mencionar benefícios
GOAL: Ajudar clientes a tomar decisões de compra informadas
```

### Estruturas de Controle
```tagscript
IF condition = true THEN
  TASK: Executar ação
  ACTION: Processar dados
  GOAL: Obter resultado
ELSE
  TASK: Ação alternativa
  ACTION: Fallback
  GOAL: Manter funcionalidade
END

FOR EACH item IN collection DO
  TASK: Processar item
  ACTION: Aplicar lógica
  GOAL: Transformar dados
END
```

### Integrações Externas
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

### Segurança
```tagscript
LOOPGUARD {
  max_depth: 3,
  allow_repeat: false
}

ON ERROR
  TASK: Tratamento de erro
  ACTION: Log e notificação
  GOAL: Manter estabilidade
END
```

## 🔗 Referências @ para LLMs

### Visão Geral
As referências `@` permitem que LLMs acessem ferramentas e recursos através de métodos permitidos pelas plataformas, contornando limitações de segurança para links externos.

### Tipos de Referências

#### @tool - Ferramentas
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

#### @file - Arquivos
```tagscript
@file:"/meu-projeto/documentos/relatorio.pdf" {
  permission: "read",
  format: "text"
}

@file:"/templates/relatorio-template.xlsx" {
  copy_to: "/relatorios/",
  name: "relatorio-" + current_date
}
```

#### @project - Projetos
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

#### @db - Bancos de Dados
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

### Integração com APIs
```tagscript
CALL API @tool:openai.chat WITH {
  model: "gpt-4",
  messages: [
    {
      role: "user",
      content: "Analise os dados de @db:analytics e gere insights"
    }
  ]
}
```

### Uso em Loops
```tagscript
FOR EACH file IN @tool:google_drive.list_files DO
  TASK: Processar arquivo
  ACTION: Extrair texto e analisar
  GOAL: Identificar padrões
  
  @file:file.path {
    extract_text: true,
    save_to: "/processed/"
  }
END
```

### Tratamento de Erros
```tagscript
ON ERROR
  TASK: Registrar falha de acesso
  ACTION: Tentar método alternativo
  GOAL: Garantir continuidade
  
  @tool:backup_storage {
    operation: "retrieve",
    fallback: true
  }
END
```

## 📚 Exemplos Avançados

### Classes e Funções
```tagscript
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

### Exemplo Completo com @
```tagscript
TASK: Analisar dados do Google Drive
ACTION: Usar ferramentas permitidas pela LLM
GOAL: Extrair insights de documentos compartilhados

# Referência a arquivo no Google Drive
@file:"/meu-projeto/documentos/relatorio-vendas.pdf" {
  permission: "read",
  format: "text"
}

# Referência a ferramenta específica
@tool:google_drive {
  action: "list_files",
  folder: "1ABC123DEF456",
  filter: "pdf"
}

# Processamento com múltiplas referências
TASK: Consolidar informações
ACTION: Combinar dados de diferentes fontes
GOAL: Criar relatório unificado

IF data_available = true THEN
  @tool:spreadsheet {
    operation: "create",
    template: "sales_report"
  }
  
  @file:"/templates/relatorio-template.xlsx" {
    copy_to: "/relatorios/",
    name: "relatorio-" + current_date
  }
ELSE
  TASK: Notificar erro
  ACTION: Enviar alerta
  GOAL: Manter transparência
END
```

## 🛠️ Como Usar a Especificação

### Para Desenvolvedores
1. **Implementar Parser**: Use a gramática EBNF para criar parsers
2. **Adicionar Suporte @**: Implemente parsing de referências LLM
3. **Integrar Ferramentas**: Conecte com APIs e serviços permitidos
4. **Testar**: Valide com exemplos reais de uso

### Para Usuários
1. **Estruturar Workflows**: Use TAG para organizar lógica
2. **Integrar Ferramentas**: Use @ para acessar recursos
3. **Tratar Erros**: Implemente fallbacks e logging
4. **Iterar**: Refine baseado em resultados

## 🚀 Roadmap da Linguagem

### Funcionalidades Planejadas
- [ ] **Suporte a Templates**: Macros e snippets reutilizáveis
- [ ] **Validação Avançada**: Type checking e linting
- [ ] **Debugging**: Ferramentas de depuração integradas
- [ ] **Performance**: Otimizações de parsing e execução
- [ ] **Extensibilidade**: Sistema de plugins para ferramentas

### Melhorias de Sintaxe
- [ ] **Expressões Regulares**: Suporte nativo para regex
- [ ] **Operadores Avançados**: Matemáticos e lógicos
- [ ] **Interpolação**: Strings dinâmicas com variáveis
- [ ] **Modularização**: Import/export de módulos

## 📋 Convenções

### Nomenclatura
- **TAG**: Sempre em maiúsculas (TASK, ACTION, GOAL)
- **Funções**: camelCase (summarize, processData)
- **Classes**: PascalCase (Product, UserProfile)
- **Variáveis**: snake_case (user_id, file_path)

### Formatação
- **Indentação**: 2 espaços
- **Comentários**: # para linha única
- **Strings**: Aspas duplas para consistência
- **Parâmetros**: Espaços ao redor de operadores

## 🤝 Contribuindo

### Como Contribuir
1. **Fork** o repositório
2. **Crie** uma branch para sua feature
3. **Implemente** suas mudanças
4. **Teste** com exemplos reais
5. **Documente** novas funcionalidades
6. **Abra** um Pull Request

### Áreas de Foco
- **Parser**: Melhorar parsing de sintaxe complexa
- **Referências @**: Expandir tipos de ferramentas suportadas
- **Integrações**: Adicionar suporte a mais APIs
- **Documentação**: Exemplos e tutoriais
- **Ferramentas**: IDEs, debuggers, validators

---

**LMTagScript** - Orquestrando IA com clareza e controle através de referências @ inteligentes.
