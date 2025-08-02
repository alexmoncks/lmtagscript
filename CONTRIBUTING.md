# Guia de Contribuição

Obrigado por considerar contribuir com o LMTagScript! Este documento fornece diretrizes para contribuições.

## 🎯 Como Contribuir

### Reportando Bugs

1. Use o template de issue para bugs
2. Inclua informações detalhadas sobre o problema
3. Forneça passos para reproduzir o bug
4. Inclua informações do sistema (OS, versão do Python, etc.)

### Sugerindo Melhorias

1. Use o template de issue para feature requests
2. Descreva o problema que a melhoria resolveria
3. Proponha uma solução específica
4. Discuta alternativas consideradas

### Contribuindo com Código

#### Pré-requisitos

- Python 3.8+
- Conhecimento básico de parsing e linguagens de programação
- Familiaridade com EBNF (Extended Backus-Naur Form)

#### Configuração do Ambiente

1. Fork o repositório
2. Clone seu fork:
   ```bash
   git clone https://github.com/seu-usuario/lmtagscript.git
   cd lmtagscript
   ```

3. Crie um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   venv\Scripts\activate     # Windows
   ```

#### Processo de Desenvolvimento

1. Crie uma branch para sua feature:
   ```bash
   git checkout -b feature/nova-funcionalidade
   ```

2. Faça suas alterações seguindo as diretrizes de código

3. Teste suas alterações:
   ```bash
   cd lmtagscript_interpreter
   python main.py
   ```

4. Commit suas mudanças:
   ```bash
   git add .
   git commit -m "feat: adiciona nova funcionalidade"
   ```

5. Push para sua branch:
   ```bash
   git push origin feature/nova-funcionalidade
   ```

6. Abra um Pull Request

## 📝 Diretrizes de Código

### Estrutura do Projeto

- **`lmtagscript_boilerplate/`**: Especificação da linguagem
  - `grammar/`: Arquivos EBNF
  - `examples/`: Exemplos de uso
- **`lmtagscript_interpreter/`**: Implementação do interpretador
  - `main.py`: Parser principal
  - `input.tag`: Arquivo de exemplo

### Convenções de Código

#### Python
- Use PEP 8 para estilo de código
- Documente funções com docstrings
- Use type hints quando apropriado
- Mantenha funções pequenas e focadas

#### TagScript
- Use maiúsculas para palavras-chave (TASK, ACTION, GOAL)
- Use snake_case para identificadores
- Mantenha blocos bem indentados
- Comente código complexo

### Padrões de Commit

Use o formato convencional de commits:

- `feat:` Nova funcionalidade
- `fix:` Correção de bug
- `docs:` Documentação
- `style:` Formatação
- `refactor:` Refatoração
- `test:` Testes
- `chore:` Manutenção

### Exemplos

```bash
git commit -m "feat: adiciona suporte a loops FOR EACH"
git commit -m "fix: corrige parsing de strings com aspas"
git commit -m "docs: atualiza README com novos exemplos"
```

## 🧪 Testes

### Testando o Interpretador

1. Crie um arquivo `.tag` com seu código
2. Execute o interpretador:
   ```bash
   python main.py
   ```
3. Verifique se a saída JSON está correta

### Testando a Gramática

1. Valide sintaxe EBNF
2. Teste casos edge
3. Verifique compatibilidade com exemplos existentes

## 📚 Recursos Úteis

### Documentação
- [Especificação EBNF](lmtagscript_boilerplate/grammar/LMtagscript.ebnf)
- [Exemplos de Uso](lmtagscript_boilerplate/examples/)
- [README Principal](../README.md)

### Ferramentas Recomendadas
- Editor com suporte a Python (VS Code, PyCharm)
- Validador EBNF online
- JSON formatter para verificar saída

## 🤝 Processo de Review

1. **Pull Request**: Descreva claramente as mudanças
2. **Review**: Outros contribuidores revisarão seu código
3. **Feedback**: Responda a comentários e faça ajustes
4. **Merge**: Após aprovação, seu código será integrado

## 📞 Comunicação

- Use issues para discussões
- Seja respeitoso e construtivo
- Ajude outros contribuidores
- Mantenha discussões focadas no projeto

## 🎉 Reconhecimento

Contribuidores ativos serão listados no README do projeto.

---

Obrigado por contribuir com o LMTagScript! 🚀 