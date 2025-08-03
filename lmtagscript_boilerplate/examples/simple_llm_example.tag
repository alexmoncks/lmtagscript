# Exemplo Simples - Referências @ do LMTagScript
# Demonstra uso básico das referências @ para LLMs

TASK: Demonstrar uso das referências @
ACTION: Usar todos os tipos de referências disponíveis
GOAL: Mostrar como LLMs podem acessar ferramentas e recursos

# ========================================
# 1. @tool - Ferramentas e Serviços
# ========================================

@tool:google_drive {
  action: "list_files",
  folder: "123456789",
  filter: "pdf"
}

@tool:spreadsheet {
  operation: "create",
  template: "monthly_report"
}

@tool:email_service {
  template: "notification",
  recipients: ["user@example.com"]
}

# ========================================
# 2. @file - Arquivos e Documentos
# ========================================

@file:"/documents/report.pdf" {
  permission: "read",
  format: "text"
}

@file:"/templates/template.xlsx" {
  copy_to: "/output/",
  name: "report_2024"
}

@file:"/data/sales.csv" {
  permission: "read",
  format: "csv"
}

# ========================================
# 3. @project - Projetos e Repositórios
# ========================================

@project:analytics_dashboard {
  access: "read",
  include: ["charts", "tables"]
}

@project:sales_crm {
  access: "read_write",
  components: ["leads", "deals"]
}

@project:lmtagscript {
  access: "read",
  include: ["docs", "examples"]
}

# ========================================
# 4. @db - Bancos de Dados
# ========================================

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

@db:crm_database {
  operation: "insert",
  table: "leads",
  values: {
    "name": "João Silva",
    "email": "joao@example.com",
    "source": "website"
  }
}

# ========================================
# 5. Lógica de Controle
# ========================================

IF data_available = true THEN
  TASK: Processar dados
  ACTION: Usar ferramentas disponíveis
  GOAL: Gerar relatório
  
  @tool:data_processor {
    input: @db:sales_database,
    output: @file:"/processed/data.json"
  }
  
ELSE
  TASK: Coletar dados
  ACTION: Solicitar informações
  GOAL: Obter dados necessários
  
  @tool:data_collector {
    sources: ["crm", "website"],
    timeframe: "last_7_days"
  }
END

# ========================================
# 6. Integração com APIs de LLM
# ========================================

CALL API @tool:openai.chat WITH {
  model: "gpt-4",
  messages: [
    {
      role: "user",
      content: "Analise os dados de @db:sales_database"
    }
  ]
}

# ========================================
# 7. Loops com Referências
# ========================================

FOR EACH file IN @tool:google_drive.list_files DO
  TASK: Processar arquivo
  ACTION: Extrair informações
  GOAL: Analisar conteúdo
  
  @file:file.path {
    extract_text: true,
    save_to: "/processed/"
  }
END

# ========================================
# 8. Tratamento de Erros
# ========================================

ON ERROR
  TASK: Recuperar de erro
  ACTION: Usar dados de backup
  GOAL: Manter funcionalidade
  
  @tool:backup_storage {
    operation: "retrieve",
    fallback: true
  }
END

# ========================================
# 9. Resultado Final
# ========================================

TASK: Salvar resultado
ACTION: Consolidar dados processados
GOAL: Entregar relatório final

@file:"/reports/final_report.pdf" {
  permission: "write",
  format: "pdf"
}

@tool:email_service {
  template: "final_report",
  recipients: ["manager@example.com"],
  attachments: ["@file:/reports/final_report.pdf"]
} 