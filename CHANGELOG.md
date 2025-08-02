# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [Unreleased]

### Adicionado
- Documentação completa em português
- Guia de contribuição detalhado
- Exemplos avançados de uso
- Arquivo de licença MIT
- Estrutura de projeto organizada

## [0.1.0] - 2024-01-XX

### Adicionado
- Especificação inicial da linguagem LMTagScript
- Gramática EBNF completa
- Interpretador Python básico
- Suporte a elementos TAG (Task, Action, Goal)
- Parser para estruturas de controle (IF/ELSE, FOR EACH)
- Suporte a definição de classes e funções
- Tratamento de erros com ON ERROR
- Sistema de segurança com LOOPGUARD
- Integração com APIs externas
- Conversão para JSON estruturado

### Funcionalidades Suportadas
- ✅ **TAG**: Task, Action, Goal
- ✅ **Classes**: Definição de estruturas de dados
- ✅ **Funções**: DEFINE FUNCTION e CALL
- ✅ **Condicionais**: IF/ELSE
- ✅ **Loops**: FOR EACH
- ✅ **APIs**: CALL API
- ✅ **Erros**: ON ERROR
- ✅ **Segurança**: LOOPGUARD

### Estrutura do Projeto
- `lmtagscript_boilerplate/`: Especificação da linguagem
  - `grammar/LMtagscript.ebnf`: Gramática EBNF
  - `examples/`: Exemplos de uso
- `lmtagscript_interpreter/`: Interpretador Python
  - `main.py`: Parser principal
  - `input.tag`: Arquivo de exemplo

## [Planejado]

### Próximas Versões
- [ ] Validação de sintaxe mais robusta
- [ ] Suporte a mais tipos de dados
- [ ] Integração com APIs reais
- [ ] Interface de linha de comando
- [ ] Playground web
- [ ] Sistema de plugins
- [ ] Debugger e ferramentas de desenvolvimento
- [ ] Suporte a módulos e imports
- [ ] Validação de tipos em tempo de execução

---

## Notas de Versão

### Versionamento Semântico
- **MAJOR**: Mudanças incompatíveis na API
- **MINOR**: Adição de funcionalidades compatíveis
- **PATCH**: Correções de bugs compatíveis

### Convenções de Commit
- `feat:` Nova funcionalidade
- `fix:` Correção de bug
- `docs:` Documentação
- `style:` Formatação
- `refactor:` Refatoração
- `test:` Testes
- `chore:` Manutenção 