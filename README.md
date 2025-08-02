# LMTagScript

**LMTagScript** é uma linguagem de domínio específico (DSL) projetada para orquestrar interações com IA com precisão, estrutura e modularidade. Inspirada em linguagens de programação e frameworks de automação como n8n, ela preenche a lacuna entre engenharia de prompts e workflows do mundo real.

## 🚀 Propósito

Definir uma linguagem universal para prompts de IA, orquestração de processos e integração de ferramentas — permitindo que desenvolvedores e não-desenvolvedores construam fluxos inteligentes com clareza e controle.

## 🧱 Princípios Fundamentais

- **TAG**: Task, Action, Goal
- **Modularidade**: Funções e classes reutilizáveis
- **Controle**: Condicionais, loops, triggers, tratamento de erros
- **Conectividade**: Sintaxe nativa para APIs, n8n, webhooks, bancos de dados
- **Segurança**: Loopguard, validação, retry/fallback

## 🔤 Visão Geral da Sintaxe

```tagscript
TASK: Gerar descrição do produto
ACTION: Usar linguagem persuasiva e mencionar benefícios
GOAL: Ajudar clientes a tomar decisões de compra informadas

CLASS Product
  name: string
  price: float
  description: string

DEFINE FUNCTION summarize(product)
  TASK: Resumir produto
  ACTION: Destacar características principais
  GOAL: Preparar para uso em marketing

CALL summarize(prod1)
```

## 🔌 Exemplo de Integração Externa

```tagscript
CONNECT TO api AS stock_checker {
  url: "https://api.example.com/check",
  token: ENV("API_KEY")
}

CALL API stock_checker.check_stock WITH {
  sku: "ABC-123"
}
ON ERROR
  TASK: Registrar falha
  ACTION: Notificar administrador
  GOAL: Manter confiabilidade
```

## 🔐 Segurança e Confiabilidade

```tagscript
LOOPGUARD {
  max_depth: 3,
  allow_repeat: false
}
```

## 📁 Estrutura do Projeto

```
lmtagscript/
├── lmtagscript_boilerplate/     # Especificação da linguagem
│   ├── grammar/                 # Gramática EBNF
│   ├── examples/                # Exemplos de uso
│   └── README.md               # Documentação da especificação
├── lmtagscript_interpreter/     # Interpretador Python
│   ├── main.py                 # Parser principal
│   ├── input.tag               # Arquivo de exemplo
│   └── README.md               # Documentação do interpretador
└── README.md                   # Este arquivo
```

## 🛠️ Como Usar

### Interpretador Python

1. Navegue para o diretório do interpretador:
   ```bash
   cd lmtagscript_interpreter
   ```

2. Edite o arquivo `input.tag` com seu código TagScript

3. Execute o interpretador:
   ```bash
   python main.py
   ```

4. O resultado será exibido em JSON estruturado

### Exemplo de Saída

```json
{
  "task": "Process purchase",
  "action": "Validate user and stock",
  "goal": "Complete the order",
  "api_call": {
    "service": "purchase_api",
    "endpoint": "finalize",
    "payload": {
      "user_id": "12345"
    }
  },
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
  ]
}
```

## 🛠️ Roadmap de Ferramentas

- [ ] Interpretador em Node.js
- [ ] Playground com parsing em tempo real
- [ ] Compilador TagScript → JSON de prompts
- [ ] Sistema de plugins para ferramentas (n8n, OpenAI, ElevenLabs)
- [ ] CLI runner para execução em lote
- [ ] Integração com Supabase, Vercel, Cloudflare Workers

## 🤝 Contribuindo

Aceitamos contribuições, ideias de funcionalidades, relatórios de problemas e casos de uso.
Comece abrindo uma issue ou pull request.

### Como Contribuir

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📘 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 📚 Recursos Adicionais

- [Especificação da Gramática](lmtagscript_boilerplate/grammar/LMtagscript.ebnf)
- [Exemplos de Uso](lmtagscript_boilerplate/examples/)
- [Documentação do Interpretador](lmtagscript_interpreter/README.md)

## ⭐ Estrelas e Apoio

Se este projeto foi útil para você, considere dar uma estrela ⭐ no GitHub!

---

**LMTagScript** - Orquestrando IA com clareza e controle. 