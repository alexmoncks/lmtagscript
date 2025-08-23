TASK: Testar funcionalidades do parser
ACTION: Executar exemplos de todas as estruturas
GOAL: Validar parsing completo

# Exemplo de referências @
@tool:test_tool {
  param1: "valor1",
  param2: 42,
  param3: true
}

@file:"/caminho/arquivo.txt" {
  permission: "read",
  encoding: "utf-8"
}

@project:meu_projeto {
  access: "read_write",
  components: ["core", "utils"]
}

@db:test_database {
  query: "SELECT * FROM users",
  limit: 100
}

# Exemplo de estrutura IF
IF status = "active" AND priority > 5 THEN
  TASK: Processar urgente
  ACTION: Notificar equipe
  GOAL: Resolver imediatamente
  
  @tool:notification {
    type: "urgent",
    recipients: ["admin@empresa.com"]
  }
ELSE
  TASK: Processar normal
  ACTION: Adicionar à fila
  GOAL: Processar quando possível
END

# Exemplo de chamada API
CALL API @tool:external_service WITH {
  endpoint: "/api/process",
  data: {
    user_id: 123,
    action: "update"
  }
}

# Exemplo de loop
FOR EACH item IN items DO
  TASK: Processar item
  ACTION: Validar dados
  GOAL: Garantir qualidade
END

# Exemplo de LOOPGUARD
LOOPGUARD {
  max_depth: 10,
  allow_repeat: false,
  timeout: 300
}

# Tratamento de erro
ON ERROR
  TASK: Fallback
  ACTION: Log error
  GOAL: Continuar operação
  
  @tool:logger {
    level: "error",
    message: "Erro detectado"
  }
END 