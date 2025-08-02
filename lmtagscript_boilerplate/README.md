# LMTagScript - Especificação da Linguagem

Este diretório contém a especificação completa da linguagem LMTagScript, incluindo gramática, documentação e exemplos.

## 📚 Conteúdo

- **`grammar/`**: Definição formal da sintaxe em EBNF
- **`examples/`**: Exemplos práticos de uso da linguagem
- **`README.md`**: Esta documentação

## 🔤 Gramática EBNF

A gramática completa está definida em `grammar/LMtagscript.ebnf` e inclui:

### Elementos Básicos
- **TAG**: Task, Action, Goal
- **Identificadores**: Nomes de variáveis e funções
- **Tipos**: string, int, float, bool
- **Valores**: Strings, números, identificadores

### Estruturas de Controle
- **Condicionais**: IF/ELSE
- **Loops**: FOR EACH
- **Funções**: DEFINE FUNCTION e CALL
- **Classes**: CLASS com propriedades

### Integrações
- **APIs**: CALL API
- **Webhooks**: TRIGGER WEBHOOK
- **Conexões**: CONNECT TO
- **Tratamento de Erros**: ON ERROR

### Segurança
- **Loopguard**: Prevenção de loops infinitos
- **Validação**: Verificação de tipos e sintaxe

## 📖 Exemplos

### Exemplo Básico
```tagscript
TASK: Greet the user
ACTION: Use a friendly and concise tone
GOAL: Make a good first impression

CALL API welcome_service.send WITH {
  name: "Alex",
  language: "en"
}
```

### Exemplo com Controle de Fluxo
```tagscript
TASK: Process user input
ACTION: Validate and respond
GOAL: Provide helpful feedback

IF user_type = "premium" THEN
  TASK: Provide premium features
  ACTION: Enable advanced options
  GOAL: Enhance user experience
ELSE
  TASK: Show basic features
  ACTION: Display standard options
  GOAL: Guide to upgrade
```

### Exemplo com Classes e Funções
```tagscript
CLASS User
  name: string
  email: string
  is_premium: bool

DEFINE FUNCTION send_welcome(user)
  TASK: Send welcome message
  ACTION: Generate personalized greeting
  GOAL: Create positive first impression

CALL send_welcome(new_user)
```

## 🛠️ Como Usar a Especificação

### Para Desenvolvedores
1. Leia a gramática EBNF em `grammar/LMtagscript.ebnf`
2. Estude os exemplos em `examples/`
3. Implemente um parser seguindo a especificação
4. Teste com os exemplos fornecidos

### Para Usuários
1. Familiarize-se com a sintaxe básica
2. Experimente com os exemplos
3. Use o interpretador Python para testar código
4. Consulte a documentação para recursos avançados

## 🔮 Roadmap da Linguagem

### Funcionalidades Planejadas
- [ ] Suporte a módulos e imports
- [ ] Sistema de plugins
- [ ] Integração com mais ferramentas
- [ ] Validação de tipos em tempo de execução
- [ ] Debugger e ferramentas de desenvolvimento

### Melhorias de Sintaxe
- [ ] Suporte a comentários
- [ ] Strings multi-linha
- [ ] Expressões mais complexas
- [ ] Macros e templates

## 📋 Convenções

### Nomenclatura
- **Palavras-chave**: Maiúsculas (TASK, ACTION, GOAL)
- **Identificadores**: snake_case
- **Classes**: PascalCase
- **Constantes**: UPPER_SNAKE_CASE

### Formatação
- Indentação consistente
- Espaçamento adequado
- Comentários quando necessário
- Quebras de linha para legibilidade

## 🤝 Contribuindo

Para contribuir com a especificação:

1. **Proponha melhorias**: Abra uma issue discutindo a mudança
2. **Atualize a gramática**: Modifique o arquivo EBNF
3. **Adicione exemplos**: Crie exemplos para novas funcionalidades
4. **Teste a compatibilidade**: Verifique se os exemplos existentes ainda funcionam

## 📚 Recursos Adicionais

- [Interpretador Python](../lmtagscript_interpreter/)
- [README Principal](../../README.md)
- [Guia de Contribuição](../../CONTRIBUTING.md)

---

**LMTagScript Specification** - Definindo a linguagem universal para orquestração de IA.
