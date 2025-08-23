TASK: Testar LOOPGUARD
ACTION: Verificar parsing
GOAL: Validar detecção

# Teste de LOOPGUARD com formato JSON
LOOPGUARD {
  max_depth: 10,
  allow_repeat: false,
  timeout: 300
}

# Teste de LOOPGUARD com formato simples
LOOPGUARD max_depth: 5, allow_repeat: true

# Teste de LOOPGUARD com valores booleanos
LOOPGUARD max_depth: 3, allow_repeat: false, debug: true 