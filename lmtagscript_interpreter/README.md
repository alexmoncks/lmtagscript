# TagScript Interpreter

Este é o interpretador oficial inicial da linguagem TagScript, implementado em Python.

## 🚀 Funcionalidades

- **Parser TagScript**: Converte código TagScript em JSON estruturado
- **Suporte a TAG**: Task, Action, Goal
- **Controle de Fluxo**: IF/ELSE, FOR EACH
- **Chamadas de API**: Sintaxe nativa para integrações
- **Tratamento de Erros**: Blocos ON ERROR
- **Segurança**: Loopguard para prevenir loops infinitos

## 📋 Pré-requisitos

- Python 3.8+
- Apenas bibliotecas padrão do Python (sem dependências externas)

## 🛠️ Como Usar

### Execução Básica

1. Edite o arquivo `input.tag` com seu código TagScript
2. Execute o interpretador:
   ```bash
   python main.py
   ```
3. O resultado será exibido em JSON estruturado

### Exemplo de Código TagScript

```tagscript
TASK: Process purchase
ACTION: Validate user and stock
GOAL: Complete the order

IF stock_available = true THEN
  TASK: Proceed to payment
  ACTION: Call payment API
  GOAL: Finish transaction
ELSE
  TASK: Notify user
  ACTION: Send out-of-stock message
  GOAL: Inform and retain user

CALL API purchase_api.finalize WITH {
  user_id: "12345"
}
ON ERROR
  TASK: Fallback to manual
  ACTION: Log the failed purchase
  GOAL: Prevent loss of order
```

### Exemplo de Saída JSON

```json
{
  "task": "Process purchase",
  "action": "Validate user and stock",
  "goal": "Complete the order",
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
  ],
  "api_call": {
    "service": "purchase_api",
    "endpoint": "finalize",
    "payload": {
      "user_id": "12345"
    }
  },
  "on_error": "TASK: Fallback to manual..."
}
```

## 🔧 Estrutura do Código

### main.py

O arquivo principal contém:

- **Patterns de Regex**: Para identificar elementos TagScript
- **Função parse_tags()**: Converte código em estrutura de dados
- **Extração de Elementos**: TAG, classes, funções, condicionais, etc.

### Elementos Suportados

- ✅ **TAG**: Task, Action, Goal
- ✅ **Classes**: Definição de estruturas de dados
- ✅ **Funções**: DEFINE FUNCTION e CALL
- ✅ **Condicionais**: IF/ELSE
- ✅ **Loops**: FOR EACH
- ✅ **APIs**: CALL API
- ✅ **Erros**: ON ERROR
- ✅ **Segurança**: LOOPGUARD

## 🧪 Testando

1. Crie um arquivo `.tag` com seu código
2. Execute o interpretador
3. Verifique se a saída JSON está correta
4. Teste diferentes estruturas da linguagem

## 🔮 Próximos Passos

- [ ] Validação de sintaxe mais robusta
- [ ] Suporte a mais tipos de dados
- [ ] Integração com APIs reais
- [ ] Interface de linha de comando
- [ ] Playground web

## 📚 Recursos

- [Especificação da Gramática](../lmtagscript_boilerplate/grammar/LMtagscript.ebnf)
- [Exemplos de Uso](../lmtagscript_boilerplate/examples/)
- [README Principal](../README.md)

---

**TagScript Interpreter** - Transformando código TagScript em JSON estruturado.
