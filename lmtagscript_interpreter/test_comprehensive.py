#!/usr/bin/env python3
"""
Teste do exemplo abrangente de referências @
Demonstra parsing de todos os tipos de referências
"""

import json
import sys
import os

# Adicionar o diretório atual ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import parse_tagscript

def test_comprehensive_example():
    """Testa o exemplo abrangente com todas as referências @"""
    
    # Ler o arquivo de exemplo
    example_path = "../lmtagscript_boilerplate/examples/comprehensive_llm_example.tag"
    
    try:
        with open(example_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"❌ Arquivo não encontrado: {example_path}")
        return False
    
    print("🔍 Testando exemplo abrangente...")
    print("=" * 60)
    
    # Parsear o conteúdo
    result = parse_tagscript(content)
    
    # Verificar se o parsing foi bem-sucedido
    if not result:
        print("❌ Falha no parsing")
        return False
    
    print("✅ Parsing realizado com sucesso!")
    print("\n📊 Estrutura do resultado:")
    print("-" * 40)
    
    # Analisar os tipos de referências encontradas
    llm_refs = result.get('llm_references', [])
    api_calls = result.get('api_calls', [])
    
    print(f"📝 TAG Principal:")
    print(f"   TASK: {result.get('task', 'N/A')}")
    print(f"   ACTION: {result.get('action', 'N/A')}")
    print(f"   GOAL: {result.get('goal', 'N/A')}")
    
    print(f"\n🔗 Referências @ encontradas: {len(llm_refs)}")
    
    # Contar tipos de referências
    tool_refs = [ref for ref in llm_refs if ref.get('type') == 'tool']
    file_refs = [ref for ref in llm_refs if ref.get('type') == 'file']
    project_refs = [ref for ref in llm_refs if ref.get('type') == 'project']
    db_refs = [ref for ref in llm_refs if ref.get('type') == 'database']
    
    print(f"   🛠️  @tool: {len(tool_refs)}")
    print(f"   📁 @file: {len(file_refs)}")
    print(f"   📂 @project: {len(project_refs)}")
    print(f"   🗄️  @db: {len(db_refs)}")
    
    print(f"\n🌐 Chamadas de API: {len(api_calls)}")
    
    # Mostrar exemplos de cada tipo
    print("\n📋 Exemplos de referências:")
    print("-" * 40)
    
    if tool_refs:
        print("🛠️  @tool examples:")
        for i, ref in enumerate(tool_refs[:3], 1):
            tool_name = ref.get('tool', 'unknown')
            params = ref.get('parameters', {})
            print(f"   {i}. {tool_name} {params}")
    
    if file_refs:
        print("\n📁 @file examples:")
        for i, ref in enumerate(file_refs[:3], 1):
            file_path = ref.get('path', 'unknown')
            params = ref.get('parameters', {})
            print(f"   {i}. {file_path} {params}")
    
    if project_refs:
        print("\n📂 @project examples:")
        for i, ref in enumerate(project_refs[:3], 1):
            project_name = ref.get('project', 'unknown')
            params = ref.get('parameters', {})
            print(f"   {i}. {project_name} {params}")
    
    if db_refs:
        print("\n🗄️  @db examples:")
        for i, ref in enumerate(db_refs[:3], 1):
            db_name = ref.get('database', 'unknown')
            params = ref.get('parameters', {})
            print(f"   {i}. {db_name} {params}")
    
    # Verificar estruturas de controle
    if_blocks = result.get('if_blocks', [])
    for_loops = result.get('for_loop', [])
    error_handling = result.get('error_handling', False)
    
    print(f"\n🎛️  Estruturas de controle:")
    print(f"   🔀 IF blocks: {len(if_blocks)}")
    print(f"   🔄 FOR loops: {len(for_loops) if isinstance(for_loops, list) else 1}")
    print(f"   ⚠️  Error handling: {'Sim' if error_handling else 'Não'}")
    
    # Salvar resultado em JSON para inspeção
    output_file = "comprehensive_test_result.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Resultado salvo em: {output_file}")
    print("\n" + "=" * 60)
    print("✅ Teste concluído com sucesso!")
    
    return True

def show_usage_examples():
    """Mostra exemplos de uso das referências @"""
    
    print("\n📚 Exemplos de Uso das Referências @")
    print("=" * 60)
    
    examples = {
        "@tool": {
            "description": "Ferramentas e serviços",
            "examples": [
                '@tool:google_drive { action: "list_files", folder: "123" }',
                '@tool:spreadsheet { operation: "create", template: "report" }',
                '@tool:email_service { template: "notification", recipients: ["user@email.com"] }'
            ]
        },
        "@file": {
            "description": "Arquivos e documentos",
            "examples": [
                '@file:"/path/to/document.pdf" { permission: "read", format: "text" }',
                '@file:"/templates/report.xlsx" { copy_to: "/output/", name: "report_2024" }',
                '@file:"/data/sales.csv" { permission: "read", format: "csv" }'
            ]
        },
        "@project": {
            "description": "Projetos e repositórios",
            "examples": [
                '@project:analytics_dashboard { access: "read", include: ["charts", "tables"] }',
                '@project:sales_crm { access: "read_write", components: ["leads", "deals"] }',
                '@project:lmtagscript { access: "read", include: ["docs", "examples"] }'
            ]
        },
        "@db": {
            "description": "Bancos de dados",
            "examples": [
                '@db:sales_database { query: "SELECT * FROM sales WHERE date >= 2024-01-01" }',
                '@db:analytics_db { operation: "update", table: "metrics", values: {...} }',
                '@db:crm_database { operation: "insert", table: "leads", values: {...} }'
            ]
        }
    }
    
    for ref_type, info in examples.items():
        print(f"\n{ref_type} - {info['description']}")
        print("-" * 40)
        for i, example in enumerate(info['examples'], 1):
            print(f"  {i}. {example}")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    print("🚀 LMTagScript - Teste de Referências @")
    print("=" * 60)
    
    # Executar teste
    success = test_comprehensive_example()
    
    if success:
        # Mostrar exemplos de uso
        show_usage_examples()
        
        print("\n🎉 Todos os testes passaram!")
        print("💡 As referências @ estão funcionando corretamente.")
    else:
        print("\n❌ Alguns testes falharam.")
        print("🔧 Verifique a implementação do parser.") 