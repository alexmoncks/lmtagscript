# Exemplo Abrangente - Todas as Referências @ do LMTagScript
# Demonstra uso completo das referências @ para LLMs

TASK: Criar relatório de vendas automatizado
ACTION: Coletar dados de múltiplas fontes e gerar análise
GOAL: Fornecer insights acionáveis para a equipe de vendas

# ========================================
# 1. REFERÊNCIAS @tool - Ferramentas
# ========================================

# Acessar Google Drive para listar arquivos
@tool:google_drive {
  action: "list_files",
  folder: "1ABC123DEF456",
  filter: "pdf",
  max_results: 50
}

# Usar planilha para criar relatório
@tool:spreadsheet {
  operation: "create",
  template: "sales_report_v2",
  title: "Relatório de Vendas - " + current_month
}

# Integrar com sistema de email
@tool:email_service {
  template: "sales_summary",
  recipients: ["vendas@empresa.com", "gerencia@empresa.com"],
  subject: "Relatório Semanal de Vendas"
}

# Usar ferramenta de análise de dados
@tool:data_analyzer {
  algorithm: "trend_analysis",
  time_period: "last_30_days",
  metrics: ["revenue", "conversion_rate", "customer_satisfaction"]
}

# ========================================
# 2. REFERÊNCIAS @file - Arquivos
# ========================================

# Ler arquivo de configuração
@file:"/config/sales_settings.json" {
  permission: "read",
  format: "json"
}

# Acessar template de relatório
@file:"/templates/sales_report_template.xlsx" {
  copy_to: "/reports/",
  name: "relatorio_vendas_" + current_date,
  preserve_formatting: true
}

# Ler dados históricos
@file:"/data/historical_sales.csv" {
  permission: "read",
  format: "csv",
  encoding: "utf-8"
}

# Salvar resultados processados
@file:"/output/processed_data.json" {
  permission: "write",
  format: "json",
  compress: true
}

# ========================================
# 3. REFERÊNCIAS @project - Projetos
# ========================================

# Acessar projeto de análise de dados
@project:analytics_dashboard {
  access: "read",
  include: ["charts", "tables", "metrics"],
  exclude: ["raw_data", "temp_files"]
}

# Conectar ao projeto de CRM
@project:sales_crm {
  access: "read_write",
  components: ["leads", "opportunities", "deals"],
  sync_frequency: "real_time"
}

# Acessar documentação do projeto
@project:lmtagscript {
  access: "read",
  include: ["docs", "examples", "tutorials"],
  format: "markdown"
}

# ========================================
# 4. REFERÊNCIAS @db - Bancos de Dados
# ========================================

# Consultar dados de vendas
@db:sales_database {
  query: "SELECT * FROM sales WHERE date >= '2024-01-01' AND status = 'completed'",
  limit: 1000,
  order_by: "date DESC"
}

# Atualizar métricas de performance
@db:analytics_db {
  operation: "update",
  table: "sales_metrics",
  where: "period = 'current_month'",
  values: {
    "total_revenue": calculated_revenue,
    "avg_deal_size": avg_deal,
    "conversion_rate": conversion_rate
  }
}

# Inserir novos registros de leads
@db:crm_database {
  operation: "insert",
  table: "leads",
  values: {
    "name": lead_name,
    "email": lead_email,
    "source": "automated_report",
    "created_at": current_timestamp
  }
}

# ========================================
# 5. LÓGICA DE PROCESSAMENTO
# ========================================

# Verificar se temos dados suficientes
IF data_quality_score >= 0.8 THEN
  TASK: Processar dados de alta qualidade
  ACTION: Executar análise completa
  GOAL: Gerar insights precisos
  
  # Usar múltiplas ferramentas em sequência
  @tool:data_processor {
    operation: "clean_and_validate",
    input: @db:sales_database,
    output: @file:"/processed/clean_data.json"
  }
  
  @tool:ml_analyzer {
    model: "sales_prediction",
    features: ["revenue", "deals", "conversion"],
    output: @project:analytics_dashboard
  }
  
ELSE
  TASK: Coletar dados adicionais
  ACTION: Solicitar informações complementares
  GOAL: Melhorar qualidade dos dados
  
  @tool:data_collector {
    sources: ["crm", "website", "social_media"],
    timeframe: "last_7_days"
  }
  
  @file:"/logs/data_quality_issues.log" {
    permission: "write",
    append: true,
    timestamp: true
  }
END

# ========================================
# 6. INTEGRAÇÃO COM APIS DE LLM
# ========================================

# Usar OpenAI para análise de texto
CALL API @tool:openai.chat WITH {
  model: "gpt-4",
  messages: [
    {
      role: "system",
      content: "Você é um analista de vendas especializado em interpretar dados e gerar insights acionáveis."
    },
    {
      role: "user",
      content: "Analise os dados de @db:sales_database e @file:/processed/clean_data.json. Gere um relatório executivo com 3 insights principais e recomendações."
    }
  ],
  temperature: 0.7,
  max_tokens: 2000
}

# Usar Claude para análise de tendências
CALL API @tool:claude.analyze WITH {
  model: "claude-3-sonnet",
  input: @project:analytics_dashboard,
  analysis_type: "trend_identification",
  output_format: "structured_report"
}

# ========================================
# 7. LOOPS COM REFERÊNCIAS @
# ========================================

# Processar cada arquivo do Google Drive
FOR EACH file IN @tool:google_drive.list_files DO
  TASK: Processar arquivo individual
  ACTION: Extrair e analisar conteúdo
  GOAL: Identificar oportunidades de venda
  
  @file:file.path {
    extract_text: true,
    save_to: "/processed/files/",
    metadata: {
      "original_name": file.name,
      "processed_at": current_timestamp,
      "file_size": file.size
    }
  }
  
  # Analisar conteúdo com IA
  CALL API @tool:openai.analyze WITH {
    model: "gpt-3.5-turbo",
    content: @file:file.path,
    analysis: "sales_opportunities"
  }
END

# Processar cada lead do CRM
FOR EACH lead IN @db:crm_database.leads DO
  TASK: Qualificar lead
  ACTION: Analisar perfil e comportamento
  GOAL: Priorizar leads mais promissores
  
  @tool:lead_scorer {
    lead_id: lead.id,
    criteria: ["engagement", "budget", "timeline"],
    output: @db:crm_database
  }
END

# ========================================
# 8. TRATAMENTO DE ERROS AVANÇADO
# ========================================

ON ERROR
  TASK: Implementar fallback robusto
  ACTION: Usar dados de backup e notificar equipe
  GOAL: Manter continuidade do processo
  
  # Acessar dados de backup
  @tool:backup_storage {
    operation: "retrieve",
    fallback: true,
    data_type: "sales_data"
  }
  
  # Notificar equipe via email
  @tool:email_service {
    template: "error_notification",
    recipients: ["tech@empresa.com", "vendas@empresa.com"],
    priority: "high",
    include_logs: true
  }
  
  # Registrar erro no sistema
  @file:"/logs/error_log.json" {
    permission: "write",
    append: true,
    include_stack_trace: true
  }
  
  # Atualizar status no projeto
  @project:analytics_dashboard {
    status: "error",
    last_error: error_message,
    recovery_attempts: recovery_count
  }
END

# ========================================
# 9. CONFIGURAÇÃO DE SEGURANÇA
# ========================================

LOOPGUARD {
  max_depth: 5,
  allow_repeat: false,
  timeout: 300
}

# ========================================
# 10. RESULTADO FINAL
# ========================================

TASK: Gerar relatório final
ACTION: Consolidar todos os dados e insights
GOAL: Entregar relatório executivo completo

# Salvar relatório final
@file:"/reports/sales_report_final.pdf" {
  permission: "write",
  format: "pdf",
  template: "executive_summary"
}

# Enviar para stakeholders
@tool:email_service {
  template: "final_report",
  recipients: ["ceo@empresa.com", "vendas@empresa.com", "financeiro@empresa.com"],
  attachments: ["@file:/reports/sales_report_final.pdf"]
}

# Atualizar dashboard
@project:analytics_dashboard {
  status: "completed",
  last_updated: current_timestamp,
  next_run: next_scheduled_run
}

# Registrar no banco de dados
@db:reports_database {
  operation: "insert",
  table: "generated_reports",
  values: {
    "report_type": "sales_analysis",
    "generated_at": current_timestamp,
    "file_path": "@file:/reports/sales_report_final.pdf",
    "status": "delivered"
  }
} 