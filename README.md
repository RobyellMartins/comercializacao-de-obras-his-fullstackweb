# Sistema de Obras HIS

Sistema para gerenciamento de empreendimentos habitacionais de interesse social (HIS), incluindo controle de obras, unidades e construtoras.

## Funcionalidades

- **Gestão de Empreendimentos**: Cadastro, edição, listagem e publicação de empreendimentos
- **Gestão de Construtoras**: Controle das empresas responsáveis pelos empreendimentos
- **Gestão de Obras**: Acompanhamento do progresso das obras
- **Gestão de Unidades**: Controle das unidades habitacionais
- **Upload de Planilhas**: Importação em massa via arquivos Excel
- **Filtros Avançados**: Busca por diversos critérios incluindo empreendimentos publicados
- **API REST**: Interface completa para integração
- **Documentação Swagger**: Documentação automática da API

## Tecnologias

### Backend
- Python 3.9+
- Flask
- SQLAlchemy
- Alembic (migrações)
- Marshmallow (validação)
- Flasgger (documentação Swagger)
- SQLite/PostgreSQL

### Frontend
- React.js
- Material-UI
- Axios

## Instalação e Configuração

### 1. Clonar o repositório
```bash
git clone <url-do-repositorio>
cd obras-his
```

### 2. Configurar ambiente Python
```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### 3. Configurar variáveis de ambiente
```bash
# Copiar arquivo de exemplo
cp .env.example .env

# Editar .env com suas configurações
```

### 4. Inicializar banco de dados
```bash
# Executar migrações
alembic upgrade head

# Ou simplesmente executar a aplicação (criará as tabelas automaticamente)
python app.py
```

### 5. Executar a aplicação
```bash
python app.py
```

A API estará disponível em: `http://localhost:5000`
Documentação Swagger: `http://localhost:5000/docs/`

### 6. Frontend (opcional)
```bash
cd obras-his-frontend
npm install
npm start
```

O frontend estará disponível em: `http://localhost:3000`

## Estrutura do Projeto

```
obras-his/
├── src/
│   ├── blueprints/          # Rotas da API
│   │   ├── empreendimentos.py
│   │   ├── construtoras.py
│   │   ├── obras.py
│   │   └── unidades.py
│   ├── models.py            # Modelos do banco de dados
│   ├── schemas.py           # Schemas de validação
│   ├── config.py            # Configurações
│   ├── db_sql.py           # Configuração do banco
│   ├── repositories/        # Camada de dados
│   └── services/           # Lógica de negócio
├── alembic/                # Migrações do banco
├── obras-his-frontend/     # Frontend React
├── uploads/                # Arquivos enviados
├── app.py                  # Aplicação principal
├── requirements.txt        # Dependências Python
└── README.md
```

## API Endpoints

### Empreendimentos
- `GET /empreendimentos` - Listar empreendimentos (com filtros)
- `POST /empreendimentos` - Criar empreendimento
- `GET /empreendimentos/{id}` - Buscar empreendimento
- `PUT /empreendimentos/{id}` - Atualizar empreendimento
- `DELETE /empreendimentos/{id}` - Deletar empreendimento
- `POST /empreendimentos/{id}/publicar` - Publicar empreendimento
- `POST /empreendimentos/upload` - Upload de planilha

### Construtoras
- `GET /api/construtoras` - Listar construtoras
- `POST /api/construtoras` - Criar construtora
- `GET /api/construtoras/{id}` - Buscar construtora
- `PUT /api/construtoras/{id}` - Atualizar construtora
- `DELETE /api/construtoras/{id}` - Deletar construtora

### Obras
- `GET /api/obras` - Listar obras (com filtros)
- `POST /api/obras` - Criar obra
- `GET /api/obras/{id}` - Buscar obra
- `PUT /api/obras/{id}` - Atualizar obra
- `DELETE /api/obras/{id}` - Deletar obra
- `POST /api/obras/{id}/publicar` - Publicar obra
- `PUT /api/obras/{id}/progresso` - Atualizar progresso

### Unidades
- `GET /api/unidades` - Listar unidades (com filtros)
- `POST /api/unidades` - Criar unidade
- `GET /api/unidades/{id}` - Buscar unidade
- `PUT /api/unidades/{id}` - Atualizar unidade
- `DELETE /api/unidades/{id}` - Deletar unidade
- `PUT /api/unidades/{id}/status` - Atualizar status
- `GET /api/unidades/empreendimento/{id}` - Unidades por empreendimento

## Filtros Disponíveis

### Empreendimentos
- `construtora_id` - Filtrar por construtora
- `nome` - Buscar por nome
- `cidade` - Filtrar por cidade
- `estado` - Filtrar por estado
- `status` - Filtrar por status
- `somente_publicadas=1` - Apenas empreendimentos publicados
- `dataInicio` - Data de início (formato: YYYY-MM-DD)
- `dataFim` - Data de fim (formato: YYYY-MM-DD)

### Obras
- `empreendimento_id` - Filtrar por empreendimento
- `nome` - Buscar por nome
- `status` - Filtrar por status
- `somente_publicadas=1` - Apenas obras publicadas

### Unidades
- `empreendimento_id` - Filtrar por empreendimento
- `status` - Filtrar por status (Disponível, Reservada, Vendida, Indisponível)
- `tipo` - Filtrar por tipo

## Upload de Planilhas

O sistema suporta upload de planilhas Excel (.xlsx, .xls) para importação em massa de empreendimentos.

### Formato da Planilha
A primeira linha deve conter os cabeçalhos. Colunas suportadas:
- `nome` / `empreendimento` / `projeto`
- `endereco` / `endereço` / `rua` / `logradouro`
- `cidade` / `municipio` / `município`
- `estado` / `uf`
- `cep`
- `tipo` / `categoria`
- `status` / `situacao` / `situação`
- `valor_total` / `valor total` / `investimento`
- `unidades` / `qtd_unidades` / `quantidade`

## Desenvolvimento

### Executar em modo de desenvolvimento
```bash
export DEBUG=True
python app.py
```

### Executar testes
```bash
python -m pytest tests/
```

### Criar nova migração
```bash
alembic revision --autogenerate -m "Descrição da migração"
alembic upgrade head
```

## Produção

### Configurações recomendadas para produção
```bash
# .env
DEBUG=False
SECRET_KEY=sua-chave-secreta-forte
DATABASE_URL=postgresql://user:pass@localhost/obras_his
ALLOWED_ORIGINS=https://seudominio.com
```

### Deploy com Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## Suporte

Para suporte, abra uma issue no repositório ou entre em contato com a equipe de desenvolvimento.
