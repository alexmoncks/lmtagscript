# Arquitetura do LMTagScript Parser

## 🏗️ Visão Geral da Arquitetura

O LMTagScript Parser foi completamente refatorado de uma arquitetura procedural para uma arquitetura orientada a objetos robusta e extensível. Esta documentação descreve a estrutura interna, os padrões de design e as decisões arquiteturais tomadas.

## 🎯 Princípios de Design

### **1. Single Responsibility Principle (SRP)**
Cada método tem uma responsabilidade única e bem definida:
- `_parse_line()`: Parse de uma única linha
- `_parse_if_statement()`: Parse de declarações IF
- `_parse_function_definition()`: Parse de definições de função

### **2. Open/Closed Principle (OCP)**
A arquitetura é aberta para extensão mas fechada para modificação:
- Novos tipos de estruturas podem ser adicionados facilmente
- Métodos existentes não precisam ser modificados para novas funcionalidades

### **3. Dependency Inversion Principle (DIP)**
O parser depende de abstrações (interfaces) não de implementações concretas:
- Uso de tipos genéricos (`Dict[str, Any]`, `List[str]`)
- Métodos que retornam estruturas padronizadas

## 🏛️ Estrutura de Classes

### **Classe Principal: `TagScriptParser`**

```python
class TagScriptParser:
    """Parser principal para TagScript com suporte a estruturas complexas"""
    
    def __init__(self):
        # Estado interno do parser
        self.result = {}           # Resultado final do parsing
        self.current_block = None  # Bloco atual sendo processado
        self.block_stack = []      # Stack de blocos aninhados
        self.if_blocks = []        # Blocos IF/ELSE/END
        self.api_calls = []        # Chamadas de API
        self.llm_references = []   # Referências @
        self.loop_guards = []      # Declarações LOOPGUARD
        self.variables = {}        # Variáveis encontradas
        self.functions = []        # Funções definidas
        self.classes = []          # Classes definidas
        self.calls = []            # Chamadas de função
```

## 🔧 Métodos Principais

### **1. Métodos de Interface Pública**

#### **`parse(content: str) -> Dict[str, Any]`**
- **Responsabilidade**: Ponto de entrada principal do parser
- **Fluxo**: 
  1. Divide o conteúdo em linhas
  2. Chama `_parse_lines()` para processar cada linha
  3. Chama `_finalize_result()` para finalizar o resultado
  4. Retorna o JSON estruturado

#### **`_parse_lines(lines: List[str]) -> None`**
- **Responsabilidade**: Coordena o parsing de todas as linhas
- **Fluxo**:
  1. Itera sobre cada linha
  2. Chama `_parse_line()` para cada linha
  3. Gerencia o índice de linha e linhas consumidas
  4. Trata erros de parsing com fallback graceful

### **2. Métodos de Parsing de Linha**

#### **`_parse_line(line: str, lines: List[str], line_index: int) -> int`**
- **Responsabilidade**: Parse de uma única linha e roteamento para métodos específicos
- **Retorno**: Número de linhas consumidas
- **Padrão**: Command Pattern - cada tipo de linha é roteado para um método específico

#### **`_add_tag(tag_type: str, value: str) -> None`**
- **Responsabilidade**: Adiciona TAGs ao resultado, suportando múltiplas
- **Implementação**: Mantém arrays para cada tipo de TAG
- **Benefício**: Preserva todas as TAGs encontradas, não apenas a última

### **3. Métodos de Parsing de Estruturas**

#### **`_parse_if_statement(line: str, lines: List[str], line_index: int) -> int`**
- **Responsabilidade**: Parse de declarações IF/THEN
- **Funcionalidades**:
  - Extrai condição usando regex
  - Cria estrutura de bloco IF
  - Gerencia stack de blocos
  - Suporta condições complexas (AND, OR, NOT)

#### **`_parse_function_definition(line: str, lines: List[str], line_index: int) -> int`**
- **Responsabilidade**: Parse de DEFINE FUNCTION
- **Funcionalidades**:
  - Extrai nome da função
  - Parse TASK, ACTION, GOAL dentro da função
  - Suporta funções multilinha
  - Registra número da linha para debugging

#### **`_parse_class_definition(line: str, lines: List[str], line_index: int) -> int`**
- **Responsabilidade**: Parse de CLASS declarations
- **Funcionalidades**:
  - Extrai nome da classe
  - Parse propriedades (key: value)
  - Suporta propriedades multilinha
  - Estrutura preparada para métodos futuros

#### **`_parse_call_statement(line: str, lines: List[str], line_index: int) -> int`**
- **Responsabilidade**: Parse de CALL statements
- **Funcionalidades**:
  - Extrai nome da função chamada
  - Parse argumentos se presentes
  - Suporta diferentes formatos de argumentos

#### **`_parse_loopguard(line: str, lines: List[str], line_index: int) -> int`**
- **Responsabilidade**: Parse de LOOPGUARD com múltiplos formatos
- **Formatos suportados**:
  - JSON: `LOOPGUARD { max_depth: 3, allow_repeat: false }`
  - Simples: `LOOPGUARD max_depth: 5, allow_repeat: true`
  - Booleanos: `LOOPGUARD debug: true, verbose: false`

### **4. Métodos de Parsing de Referências**

#### **`_parse_llm_reference_multiline(lines: List[str], start_index: int) -> int`**
- **Responsabilidade**: Parse de referências @ que podem abranger múltiplas linhas
- **Tipos suportados**:
  - `@tool:` - Ferramentas e serviços
  - `@file:` - Arquivos e documentos
  - `@project:` - Projetos e repositórios
  - `@db:` - Bancos de dados

#### **`_parse_multiline_json(lines: List[str], start_index: int, brace_start: int) -> Tuple[Dict, int]`**
- **Responsabilidade**: Parse de JSON multilinha com suporte a chaves e colchetes aninhados
- **Funcionalidades**:
  - Conta chaves `{}` e colchetes `[]` aninhados
  - Suporta estruturas que abrangem múltiplas linhas
  - Parse robusto de parâmetros complexos

### **5. Métodos de Parsing de Dados**

#### **`_parse_json_like(json_str: str) -> Any`**
- **Responsabilidade**: Parse de strings JSON-like para Python
- **Funcionalidades**:
  - Remove chaves externas se presentes
  - Detecta arrays e objetos
  - Parse de pares chave-valor
  - Conversão automática de tipos (int, float, bool)

#### **`_parse_array_like(array_str: str) -> List[Any]`**
- **Responsabilidade**: Parse de arrays JSON-like
- **Funcionalidades**:
  - Suporte a arrays aninhados
  - Parse de elementos complexos (objetos, arrays)
  - Conversão automática de tipos
  - Tratamento de vírgulas e espaços

#### **`_parse_condition(condition_str: str) -> Dict[str, Any]`**
- **Responsabilidade**: Parse de condições complexas em estruturas IF
- **Operadores suportados**:
  - Lógicos: `AND`, `OR`, `NOT`
  - Comparação: `=`, `!=`, `<`, `>`, `<=`, `>=`, `IN`, `CONTAINS`
  - Funções: `function_name(arg1, arg2)`

### **6. Métodos de Finalização**

#### **`_finalize_result() -> None`**
- **Responsabilidade**: Finaliza o resultado adicionando todas as estruturas parseadas
- **Funcionalidades**:
  - Adiciona arrays não vazios ao resultado
  - Mantém estrutura consistente
  - Prepara resultado para serialização JSON

## 🔄 Fluxo de Parsing

### **1. Inicialização**
```python
parser = TagScriptParser()
```

### **2. Parsing Principal**
```python
result = parser.parse(content)
```

### **3. Fluxo Interno**
```
parse() → _parse_lines() → _parse_line() → métodos específicos → _finalize_result()
```

### **4. Roteamento de Linhas**
```
Linha → _parse_line() → Roteamento baseado no prefixo:
├── TASK: → _add_tag('task', value)
├── ACTION: → _add_tag('action', value)
├── GOAL: → _add_tag('goal', value)
├── CLASS → _parse_class_definition()
├── DEFINE FUNCTION → _parse_function_definition()
├── CALL → _parse_call_statement()
├── IF → _parse_if_statement()
├── ELSE → current_block = 'if_else'
├── END → _parse_end_statement()
├── CALL API → _parse_api_call()
├── @ → _parse_llm_reference_multiline()
├── FOR EACH → _parse_for_loop()
├── LOOPGUARD → _parse_loopguard()
├── ON ERROR → error_handling = True
└── Outros → processamento de bloco atual
```

## 🧩 Padrões de Design Utilizados

### **1. Command Pattern**
Cada tipo de linha é roteado para um método específico:
```python
elif line.startswith('IF'):
    return self._parse_if_statement(line, lines, line_index)
elif line.startswith('DEFINE FUNCTION'):
    return self._parse_function_definition(line, lines, line_index)
```

### **2. State Pattern**
O parser mantém estado interno para gerenciar blocos:
```python
self.current_block = 'if_then'  # Estado atual
self.block_stack.append('if')    # Stack de blocos
```

### **3. Template Method Pattern**
O método `parse()` define o template, métodos específicos implementam detalhes:
```python
def parse(self, content: str) -> Dict[str, Any]:
    lines = content.split('\n')
    self._parse_lines(lines)        # Template
    self._finalize_result()         # Template
    return self.result
```

### **4. Strategy Pattern**
Diferentes estratégias de parsing para diferentes tipos de conteúdo:
```python
if content.startswith('tool:'):
    return self._parse_tool_reference_multiline(lines, start_index)
elif content.startswith('file:'):
    return self._parse_file_reference_multiline(lines, start_index)
```

## 📊 Estrutura de Dados

### **1. Estado Interno**
```python
{
    'result': {},           # Resultado final
    'current_block': None,  # Bloco atual
    'block_stack': [],      # Stack de blocos
    'if_blocks': [],        # Blocos IF
    'api_calls': [],        # Chamadas API
    'llm_references': [],   # Referências @
    'loop_guards': [],      # LOOPGUARDs
    'variables': {},        # Variáveis
    'functions': [],        # Funções
    'classes': [],          # Classes
    'calls': []             # Chamadas
}
```

### **2. Estrutura de Saída**
```python
{
    'task': ['TASK1', 'TASK2'],
    'action': ['ACTION1', 'ACTION2'],
    'goal': ['GOAL1', 'GOAL2'],
    'if_blocks': [...],
    'functions': [...],
    'classes': [...],
    'calls': [...],
    'llm_references': [...],
    'loop_guards': [...],
    'api_calls': [...],
    'error_handling': true
}
```

## 🔍 Tratamento de Erros

### **1. Estratégia de Fallback**
```python
try:
    consumed_lines = self._parse_line(line, lines, i)
    i += consumed_lines
except Exception as e:
    logger.warning(f"Erro ao processar linha {i+1}: {e}")
    i += 1  # Continua com a próxima linha
```

### **2. Logging Estruturado**
```python
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.error(f"Erro durante o parsing: {e}")
```

### **3. Validação de Entrada**
```python
if not os.path.exists(args.input):
    logger.error(f"Arquivo de entrada não encontrado: {args.input}")
    sys.exit(1)
```

## 🚀 Extensibilidade

### **1. Adicionar Novos Tipos de Estrutura**
```python
elif line.startswith('NEW_STRUCTURE'):
    return self._parse_new_structure(line, lines, line_index)

def _parse_new_structure(self, line: str, lines: List[str], line_index: int) -> int:
    # Implementação do novo parser
    return consumed_lines
```

### **2. Adicionar Novos Tipos de Referência @**
```python
elif content.startswith('new_type:'):
    return self._parse_new_type_reference_multiline(lines, start_index)

def _parse_new_type_reference_multiline(self, lines: List[str], start_index: int) -> Tuple[Dict, int]:
    # Implementação do novo tipo
    return reference, consumed_lines
```

### **3. Adicionar Novos Operadores de Condição**
```python
# Em _parse_condition()
new_operators = ['NEW_OP1', 'NEW_OP2']
for op in new_operators:
    if op in condition_str:
        # Implementação do novo operador
        pass
```

## 📈 Métricas de Performance

### **1. Complexidade Temporal**
- **Parsing de linha**: O(1) - constante
- **Parsing de arquivo**: O(n) - linear no número de linhas
- **Parsing de JSON multilinha**: O(m) - onde m é o número de linhas do JSON

### **2. Complexidade Espacial**
- **Estado interno**: O(1) - constante
- **Resultado**: O(n) - proporcional ao tamanho do arquivo
- **Arrays de estruturas**: O(s) - onde s é o número de estruturas

### **3. Otimizações Implementadas**
- **Parsing incremental**: Processa linha por linha
- **Early exit**: Para em estruturas malformadas
- **Cache de regex**: Padrões compilados uma vez
- **Streaming de saída**: Para arquivos grandes

## 🔮 Roadmap de Melhorias

### **Versão 2.1**
- [ ] Validação de sintaxe mais rigorosa
- [ ] Cache de estruturas parseadas
- [ ] Otimização de regex patterns

### **Versão 2.2**
- [ ] Parsing paralelo para arquivos grandes
- [ ] Sistema de plugins
- [ ] API REST

### **Versão 3.0**
- [ ] Suporte a múltiplas linguagens
- [ ] Sistema de templates
- [ ] Integração com IDEs

## 📝 Conclusão

A arquitetura do LMTagScript Parser foi projetada para ser:

1. **Robusta**: Tratamento de erros abrangente
2. **Extensível**: Fácil adição de novas funcionalidades
3. **Manutenível**: Código bem organizado e documentado
4. **Performática**: Otimizada para arquivos de diferentes tamanhos
5. **Testável**: Métodos isolados e bem definidos

Esta arquitetura fornece uma base sólida para o crescimento futuro do parser, permitindo que ele evolua para atender às necessidades crescentes da comunidade TagScript.

---

**Arquitetura LMTagScript Parser** - Construída para crescer e evoluir! 🚀

*Documentação técnica v2.0 - 2025-08-23* 