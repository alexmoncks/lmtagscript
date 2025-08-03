# Exemplo de uso de referências @ para LLMs
# Permite que LLMs acessem ferramentas e recursos através de @

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

# Referência a projeto
@project:lmtagscript {
  access: "read",
  include: ["docs", "examples"]
}

# Referência a banco de dados
@db:analytics {
  query: "SELECT * FROM sales WHERE date >= '2024-01-01'",
  limit: 100
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

# Integração com APIs através de @
CALL API @tool:openai.chat WITH {
  model: "gpt-4",
  messages: [
    {
      role: "user",
      content: "Analise os dados de @db:analytics e gere insights"
    }
  ]
}

# Uso em loops
FOR EACH file IN @tool:google_drive.list_files DO
  TASK: Processar arquivo
  ACTION: Extrair texto e analisar
  GOAL: Identificar padrões
  
  @file:file.path {
    extract_text: true,
    save_to: "/processed/"
  }
END

# Tratamento de erros com @
ON ERROR
  TASK: Registrar falha de acesso
  ACTION: Tentar método alternativo
  GOAL: Garantir continuidade
  
  @tool:backup_storage {
    operation: "retrieve",
    fallback: true
  }
END 