
TASK: Process purchase
ACTION: Validate user and stock
GOAL: Complete the order

# Exemplo de uso de referências @ para LLMs
@tool:google_drive {
  action: "list_files",
  folder: "1ABC123DEF456"
}

@file:"/meu-projeto/documentos/relatorio-vendas.pdf" {
  permission: "read",
  format: "text"
}

IF stock_available = true THEN
  TASK: Proceed to payment
  ACTION: Call payment API
  GOAL: Finish transaction
  
  @tool:payment_processor {
    operation: "charge",
    amount: 99.99
  }
ELSE
  TASK: Notify user
  ACTION: Send out-of-stock message
  GOAL: Inform and retain user
  
  @tool:email_service {
    template: "out_of_stock",
    recipient: user_email
  }
END

CALL API @tool:openai.chat WITH {
  model: "gpt-4",
  messages: [
    {
      role: "user",
      content: "Analise os dados de @db:analytics"
    }
  ]
}

ON ERROR
  TASK: Fallback to manual
  ACTION: Log the failed purchase
  GOAL: Prevent loss of order
  
  @tool:backup_storage {
    operation: "retrieve",
    fallback: true
  }
END

FOR EACH item IN cart
  TASK: Check availability
  ACTION: Query inventory system
  GOAL: Determine stock level

LOOPGUARD {
  max_depth: 3,
  allow_repeat: false
}
