import os
import sys

# Configurar SQLite para teste
os.environ['DATABASE_URL'] = 'sqlite:///test_obras_his.db'

# Importar e testar a aplicação
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import create_app
import json

def test_basic_functionality():
    """Testa funcionalidades básicas do sistema"""
    app = create_app()
    
    with app.test_client() as client:
        print("Testando funcionalidades básicas...")
        
        # Teste 1: Health check
        print("\n1. Testando health check...")
        response = client.get('/health')
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.get_json()}")
        
        # Teste 2: Listar empreendimentos (deve estar vazio inicialmente)
        print("\n2. Testando listagem de empreendimentos...")
        response = client.get('/empreendimentos')
        print(f"   Status: {response.status_code}")
        data = response.get_json()
        print(f"   Empreendimentos encontrados: {len(data) if isinstance(data, list) else 'N/A'}")
        
        # Teste 3: Criar um empreendimento
        print("\n3. Testando criação de empreendimento...")
        empreendimento_data = {
            "nome": "Residencial Teste",
            "nome_empresa": "Construtora Teste Ltda",
            "cep": "70000-000",
            "endereco": "Rua Teste, 123 - Brasília/DF",
            "observacao": "Empreendimento de teste"
        }
        
        response = client.post('/empreendimentos', 
                             data=json.dumps(empreendimento_data),
                             content_type='application/json')
        print(f"   Status: {response.status_code}")
        if response.status_code == 201:
            created_emp = response.get_json()
            print(f"   Empreendimento criado com ID: {created_emp.get('id')}")
            
            # Teste 4: Publicar empreendimento
            print("\n4. Testando publicação de empreendimento...")
            emp_id = created_emp.get('id')
            response = client.post(f'/empreendimentos/{emp_id}/publicar')
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                pub_data = response.get_json()
                print(f"   Publicado em: {pub_data.get('publicado_em')}")
                print(f"   Expira em: {pub_data.get('expira_em')}")
            
            # Teste 5: Marcar para aguardar publicação
            print("\n5. Testando aguardar publicação...")
            response = client.post(f'/empreendimentos/{emp_id}/aguardar')
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                aguard_data = response.get_json()
                print(f"   Status: {aguard_data.get('status_publicacao')}")
        else:
            print(f"   Erro: {response.get_json()}")
        
        # Teste 6: Health check do serviço de empreendimentos
        print("\n6. Testando health check do serviço...")
        response = client.get('/empreendimentos/health')
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.get_json()}")
        
        print("\nTestes básicos concluídos!")

if __name__ == '__main__':
    test_basic_functionality()
