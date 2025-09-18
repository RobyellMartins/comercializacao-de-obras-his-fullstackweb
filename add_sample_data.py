from src.db_sql import get_db
from src.models import Empreendimento, Construtora

with get_db() as db:
    # Check if construtoras exist
    construtoras = db.query(Construtora).all()
    if not construtoras:
        # Create sample construtora
        construtora = Construtora(
            nome="Construtora Exemplo Ltda",
            cnpj="12.345.678/0001-99",
            endereco="Rua Exemplo, 123 - Centro"
        )
        db.add(construtora)
        db.flush()

    # Get the construtora
    construtora = db.query(Construtora).first()

    # Create sample empreendimentos
    empreendimentos_data = [
        {
            'nome': 'Residencial Jardim das Flores',
            'endereco': 'Rua das Flores, 456 - Jardim',
            'cep': '01234-567',
            'observacao': 'Empreendimento residencial com 50 unidades',
            'construtora_id': construtora.id
        },
        {
            'nome': 'Condomínio Vista Mar',
            'endereco': 'Av. Beira Mar, 789 - Praia',
            'cep': '20000-000',
            'observacao': 'Empreendimento residencial com vista para o mar',
            'construtora_id': construtora.id
        },
        {
            'nome': 'Edifício Centro Empresarial',
            'endereco': 'Av. Paulista, 1000 - Centro',
            'cep': '01310-100',
            'observacao': 'Edifício comercial no centro da cidade',
            'construtora_id': construtora.id
        }
    ]

    for emp_data in empreendimentos_data:
        empreendimento = Empreendimento(**emp_data)
        db.add(empreendimento)

    db.commit()
    print("Dados de exemplo adicionados com sucesso!")
