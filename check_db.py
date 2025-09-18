from src.db_sql import get_db
from src.models import Empreendimento

with get_db() as db:
    empreendimentos = db.query(Empreendimento).all()
    print(f'Total empreendimentos: {len(empreendimentos)}')
    for e in empreendimentos:
        print(f'{e.id}: {e.nome}')
