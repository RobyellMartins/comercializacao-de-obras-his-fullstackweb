import pytest
import json
import sys
import os
import pytest
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


import random

def test_criar_unidade_sucesso(client):
    data = {
        "empreendimento_id": 1,
        "numero_unidade": str(random.randint(10000, 99999)),
        "status": "Ativa"
    }
    response = client.post('/api/unidades', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 201
    json_data = response.get_json()
    assert json_data['status'] == "Ativa"




def test_criar_unidade_sem_dados(client):
    response = client.post('/api/unidades', data=json.dumps({}), content_type='application/json')
    assert response.status_code == 400

def test_criar_unidade_empreendimento_invalido(client):
    data = {
        "empreendimento_id": 9999,
        "numero_unidade": "102",
        "status": "Ativa"
    }
    response = client.post('/api/unidades', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 404



def test_listar_unidades(client):
    response = client.get('/api/unidades')
    assert response.status_code == 200
    json_data = response.get_json()
    assert isinstance(json_data, list)
