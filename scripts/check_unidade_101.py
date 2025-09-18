import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.db_sql import get_db
from src.models import Unidade

with get_db() as db:
    unidades = db.query(Unidade).filter(Unidade.numero_unidade == '101').all()
    print(f'Unidades existentes com número 101: {len(unidades)}')
