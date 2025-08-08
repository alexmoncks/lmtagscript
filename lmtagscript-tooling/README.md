# LMTagScript Tooling

Este monorepo adiciona quatro pacotes essenciais para o ecossistema LMTagScript:
- **@lmtagscript/core**: valida, compila e (opcionalmente) executa `.tag` com contexto simulado.
- **@lmtagscript/api**: microserviço HTTP (Actions do GPT) expondo `/validate`, `/compile`, `/run`.
- **@lmtagscript/mcp**: servidor MCP remoto (STDIO/JSON-RPC) com os mesmos comandos.
- **@lmtagscript/cli**: CLI para uso local e CI.

Também inclui **OpenAPI 3.1** em `openapi/lmtagscript.yml` e um workflow de **release** que publica a spec no GitHub Pages.

## 🚀 Casos de Uso

### MCP (Model Context Protocol)
O servidor MCP permite integração direta com LLMs e editores através do protocolo JSON-RPC via STDIO:

```bash
# Executar servidor MCP
node dist/server.js

# Métodos disponíveis:
# - lmtagscript/validate: Valida código .tag
# - lmtagscript/compile: Compila para JSON/AST
# - lmtagscript/run: Executa com contexto
```

### API HTTP
Microserviço para integração com sistemas externos:

```bash
# Subir API
pnpm --filter @lmtagscript/api dev

# Endpoints:
# POST /validate - Validação de código
# POST /compile - Compilação para JSON
# POST /run - Execução com contexto
```

### CLI Local
Ferramenta de linha de comando para desenvolvimento:

```bash
# Instalar CLI
npm install -g @lmtagscript/cli

# Comandos:
lmtag validate input.tag
lmtag compile input.tag
lmtag run input.tag --ctx context.json
```

## Como rodar localmente
```bash
pnpm i
pnpm -r build
pnpm --filter @lmtagscript/api dev  # sobe a API em localhost:3000
```

## 🔧 Integração com LMTagScript

Este tooling complementa perfeitamente o ecossistema LMTagScript:

- **Boilerplate**: Define a linguagem (gramática EBNF, documentação)
- **Interpreter**: Implementa o parser funcional (Python)
- **Tooling**: Fornece interfaces de acesso (TypeScript)

### Arquitetura de Integração

```
LMTagScript Boilerplate (EBNF)
         ↓
LMTagScript Interpreter (Python Parser)
         ↓
LMTagScript Tooling (TypeScript Wrappers)
         ↓
APIs, CLIs, MCPs
```

## 📋 Roadmap de Integração

- [ ] Migrar parser Python para TypeScript
- [ ] Implementar validação baseada na gramática EBNF real
- [ ] Adicionar suporte completo às referências @ (@tool, @file, @project, @db)
- [ ] Criar testes com exemplos existentes
- [ ] Implementar execução real (não simulada)

> Parser/AST são placeholders para permitir o bootstrap. Troque por sua implementação do LMTagScript.
