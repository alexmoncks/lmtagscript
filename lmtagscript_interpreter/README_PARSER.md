# LMTagScript Parser - Guia de Uso Completo

## 🚀 Visão Geral

O LMTagScript Parser é uma ferramenta robusta e avançada para converter arquivos TagScript em JSON estruturado. Ele suporta todas as estruturas TagScript incluindo referências @, estruturas de controle, loops, funções, classes e muito mais.

## 📋 Funcionalidades Completas

### ✅ **Funcionalidades Básicas**
- **Parsing completo** de arquivos TagScript
- **Suporte a referências @** (@tool, @file, @project, @db)
- **Estruturas de controle** (IF/ELSE/END)
- **Loops** (FOR EACH)
- **LOOPGUARD** com parâmetros
- **Chamadas de API** (CALL API)
- **Tratamento de erros** (ON ERROR)

### 🆕 **Novas Funcionalidades Implementadas**
- **Suporte a múltiplas TAGs** (TASK, ACTION, GOAL)
- **Detecção de DEFINE FUNCTION** com parsing completo
- **Suporte a CLASS declarations** com propriedades
- **Detecção de CALL statements** (chamadas de função)
- **LOOPGUARD melhorado** com suporte a múltiplos formatos
- **Parsing de JSON multilinha** com suporte a arrays
- **Suporte a arrays e objetos aninhados**
- **Logging detalhado** (modo verbose)
- **Múltiplos formatos de saída**

## 🛠️ Instalação

```bash
# Clonar o repositório
git clone <repository-url>
cd lmtagscript_interpreter

# Instalar dependências (se necessário)
pip install -r requirements.txt
```

## 💻 Uso Básico

### Comando Simples
```bash
python main.py
```
- **Entrada**: `input.tag` (padrão)
- **Saída**: `output.json` (padrão)

### Comando com Arquivos Customizados
```bash
python main.py -i meu_script.tag -o resultado.json
```

### Comando com Formatação
```bash
python main.py -i script.tag -o saida.json --pretty
```

## 📚 Parâmetros de Linha de Comando

| Parâmetro | Forma Curta | Descrição | Padrão |
|-----------|-------------|-----------|---------|
| `--input` | `-i` | Arquivo TagScript de entrada | `input.tag` |
| `--output` | `-o` | Arquivo JSON de saída | `output.json` |
| `--verbose` | `-v` | Modo verbose com logging detalhado | `False` |
| `--pretty` | | Formata JSON com indentação | `False` |
| `--stdout` | | Envia saída para stdout | `False` |
| `--encoding` | | Encoding dos arquivos | `utf-8` |
| `--help` | `-h` | Mostra ajuda | - |

## 🔍 Exemplos de Uso

### 1. Parsing Básico
```bash
# Usar arquivos padrão
python main.py

# Arquivo de entrada customizado
python main.py -i script.tag

# Arquivo de saída customizado
python main.py -o resultado.json
```

### 2. Modo Verbose
```bash
# Ativar logging detalhado
python main.py -v

# Combinar com outros parâmetros
python main.py -i script.tag -o saida.json -v
```

### 3. Formatação de Saída
```bash
# JSON formatado (indentado)
python main.py --pretty

# Saída para stdout (terminal)
python main.py --stdout

# Combinar formatação e stdout
python main.py --pretty --stdout
```

### 4. Encoding Customizado
```bash
# Especificar encoding
python main.py --encoding latin-1

# Para arquivos com caracteres especiais
python main.py -i script_pt.tag --encoding iso-8859-1
```

### 5. Uso Avançado
```bash
# Pipeline completo com formatação
python main.py -i script.tag -o resultado.json --pretty -v

# Processar e enviar para stdout
python main.py -i script.tag --stdout --pretty

# Salvar com encoding específico
python main.py -i script.tag -o saida.json --encoding utf-8-sig
```

## 📊 Estrutura de Saída Completa

O parser gera um JSON estruturado com as seguintes seções principais:

### **TAGs Principais (Múltiplas)**
```json
{
  "task": [
    "Descrição da tarefa 1",
    "Descrição da tarefa 2"
  ],
  "action": [
    "Ação a ser executada 1",
    "Ação a ser executada 2"
  ],
  "goal": [
    "Objetivo 1",
    "Objetivo 2",
    "Objetivo 3"
  ]
}
```

### **Estruturas de Controle**
```json
{
  "if_blocks": [
    {
      "condition": {
        "type": "logical",
        "operator": "AND",
        "left": {
          "type": "comparison",
          "left": "status",
          "operator": "=",
          "right": "\"active\""
        },
        "right": {
          "type": "comparison",
          "left": "priority",
          "operator": ">",
          "right": "5"
        }
      },
      "then": "conteúdo do bloco then",
      "else": "conteúdo do bloco else",
      "line_number": 28
    }
  ]
}
```

### **Funções Definidas**
```json
{
  "functions": [
    {
      "name": "visualNarrativeDesign",
      "task": "Design a sequential visual story",
      "action": "Identify core message and emotional arc",
      "goal": "A storyboard ready for illustration",
      "line_number": 55
    }
  ]
}
```

### **Classes**
```json
{
  "classes": [
    {
      "name": "Agent",
      "properties": {
        "name": "\"visual-storyteller\"",
        "description": "\"Create visual narratives...\"",
        "color": "\"cyan\"",
        "tools": "[\"Write\", \"Read\", \"MultiEdit\"]"
      },
      "methods": [],
      "line_number": 8
    }
  ]
}
```

### **Chamadas de Função**
```json
{
  "calls": [
    {
      "function": "accessibilityChecklist",
      "arguments": "",
      "line_number": 238
    }
  ]
}
```

### **Referências @**
```json
{
  "llm_references": [
    {
      "type": "tool",
      "tool": "WebSearch",
      "parameters": {
        "query": "visual metaphor examples",
        "limit": 5
      }
    }
  ]
}
```

### **LOOPGUARD**
```json
{
  "loop_guards": [
    {
      "max_depth": 3,
      "allow_repeat": false
    }
  ]
}
```

### **Chamadas de API**
```json
{
  "api_calls": [
    {
      "type": "llm_api",
      "reference": {
        "type": "tool",
        "tool": "openai.chat"
      },
      "payload": {}
    }
  ]
}
```

### **Loops e Tratamento de Erro**
```json
{
  "for_loop": {
    "variable": "item",
    "collection": "items"
  },
  "error_handling": true
}
```

## 🔧 Casos de Uso Avançados

### 1. **Desenvolvimento e Debugging**
```bash
# Modo verbose para debugging
python main.py -v --pretty

# Saída para stdout para análise rápida
python main.py --stdout
```

### 2. **Integração com Sistemas**
```bash
# Salvar em arquivo específico
python main.py -i script.tag -o /path/to/output.json

# Usar encoding específico para compatibilidade
python main.py --encoding ascii
```

### 3. **Processamento em Lote**
```bash
# Script para processar múltiplos arquivos
for file in *.tag; do
  python main.py -i "$file" -o "${file%.tag}.json" --pretty
done
```

### 4. **Pipeline de Dados**
```bash
# Processar e enviar para outro comando
python main.py -i script.tag --stdout | jq '.llm_references'

# Filtrar apenas referências específicas
python main.py -i script.tag --stdout | jq '.llm_references[] | select(.type == "tool")'
```

### 5. **Análise de Estruturas Complexas**
```bash
# Contar funções definidas
python main.py -i script.tag --stdout | jq '.functions | length'

# Listar nomes de todas as funções
python main.py -i script.tag --stdout | jq '.functions[].name'

# Verificar classes e suas propriedades
python main.py -i script.tag --stdout | jq '.classes[] | {name, properties}'
```

## 🆕 **Novas Funcionalidades em Detalhe**

### **1. Suporte a Múltiplas TAGs**
**Antes**: O parser capturava apenas a última TAG encontrada
**Depois**: Agora captura todas as TAGs em arrays

```bash
# Antes: apenas 1 TASK
"task": "Última tarefa encontrada"

# Depois: todas as TASKs
"task": [
  "Primeira tarefa",
  "Segunda tarefa", 
  "Terceira tarefa"
]
```

### **2. Detecção de DEFINE FUNCTION**
**Novo**: Parse completo de funções definidas no TagScript

```tagscript
DEFINE FUNCTION minhaFuncao(context)
  TASK: Processar dados
  ACTION: Validar e transformar
  GOAL: Dados limpos e estruturados
```

**Resultado**:
```json
{
  "functions": [
    {
      "name": "minhaFuncao",
      "task": "Processar dados",
      "action": "Validar e transformar",
      "goal": "Dados limpos e estruturados",
      "line_number": 10
    }
  ]
}
```

### **3. Suporte a CLASS declarations**
**Novo**: Parse de definições de classe

```tagscript
CLASS Agent
  name: "visual-storyteller"
  description: "Create visual narratives"
  color: "cyan"
  tools: ["Write", "Read", "MultiEdit"]
```

**Resultado**:
```json
{
  "classes": [
    {
      "name": "Agent",
      "properties": {
        "name": "\"visual-storyteller\"",
        "description": "\"Create visual narratives\"",
        "color": "\"cyan\"",
        "tools": "[\"Write\", \"Read\", \"MultiEdit\"]"
      },
      "methods": [],
      "line_number": 8
    }
  ]
}
```

### **4. Detecção de CALL statements**
**Novo**: Parse de chamadas de função

```tagscript
CALL accessibilityChecklist()
CALL testVisualStory()
```

**Resultado**:
```json
{
  "calls": [
    {
      "function": "accessibilityChecklist",
      "arguments": "",
      "line_number": 238
    },
    {
      "function": "testVisualStory",
      "arguments": "",
      "line_number": 239
    }
  ]
}
```

### **5. LOOPGUARD Melhorado**
**Antes**: Apenas suporte a formato JSON `{}`
**Depois**: Suporte a múltiplos formatos

```tagscript
# Formato JSON
LOOPGUARD {
  max_depth: 10,
  allow_repeat: false,
  timeout: 300
}

# Formato simples
LOOPGUARD max_depth: 5, allow_repeat: true

# Com valores booleanos
LOOPGUARD max_depth: 3, allow_repeat: false, debug: true
```

**Resultado**:
```json
{
  "loop_guards": [
    {
      "max_depth": 10,
      "allow_repeat": "false",
      "timeout": 300
    },
    {
      "max_depth": 5,
      "allow_repeat": true
    },
    {
      "max_depth": 3,
      "allow_repeat": false,
      "debug": true
    }
  ]
}
```

## ⚠️ Tratamento de Erros

O parser inclui tratamento robusto de erros:

- **Arquivo não encontrado**: Mensagem clara com sugestões
- **Erro de encoding**: Dicas para resolver problemas de caracteres
- **Erro de parsing**: Logging detalhado para debugging
- **Fallback graceful**: Continua processando mesmo com erros parciais

## 📝 Logs e Debugging

### Modo Verbose
```bash
python main.py -v
```
- Mostra cada etapa do parsing
- Logs detalhados de cada operação
- Útil para debugging e desenvolvimento

### Níveis de Log
- **INFO**: Operações normais
- **WARNING**: Problemas não críticos
- **ERROR**: Erros que impedem o parsing
- **DEBUG**: Informações detalhadas (modo verbose)

## 🚀 Performance

- **Parsing otimizado** para arquivos grandes
- **Suporte a multilinha** sem impacto na performance
- **Streaming de saída** para arquivos grandes
- **Cache inteligente** para estruturas repetitivas

## 🔮 Recursos Futuros

- [ ] **Validação de sintaxe** mais rigorosa
- [ ] **Suporte a plugins** para extensões
- [ ] **Parsing paralelo** para arquivos muito grandes
- [ ] **Cache persistente** entre execuções
- [ ] **API REST** para uso via HTTP
- [ ] **Interface gráfica** (GUI)

## 📞 Suporte

Para dúvidas, bugs ou sugestões:
- Abra uma issue no repositório
- Consulte a documentação completa
- Verifique os exemplos incluídos

## 📄 Licença

Este projeto está sob a licença especificada no arquivo LICENSE.

---

**LMTagScript Parser** - Transformando TagScript em JSON estruturado de forma robusta e eficiente! 🎉

*Versão: 2.0 - Com todas as melhorias implementadas* 