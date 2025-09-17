# Guia para Executar o Projeto "Comercialização de Obras HIS - Fullstack Web" em Outro Sistema

Este guia fornece instruções passo a passo para configurar e executar o projeto "Comercialização de Obras HIS - Fullstack Web" em outro sistema ou PC. O projeto é uma aplicação fullstack composta por um backend em Flask (Python) e um frontend em React.

## Pré-requisitos

Antes de começar, certifique-se de que o seguinte software esteja instalado no seu sistema:

- **Python 3.8 ou superior**: Baixe e instale do site oficial [python.org](https://www.python.org/downloads/).
- **Node.js 16 ou superior**: Baixe e instale do site oficial [nodejs.org](https://nodejs.org/).
- **Git**: Para clonar o repositório. Baixe de [git-scm.com](https://git-scm.com/).
- **PostgreSQL**: Para o banco de dados. Baixe de [postgresql.org](https://www.postgresql.org/download/).
- **Virtualenv** (opcional, mas recomendado): Para criar um ambiente virtual Python. Instale com `pip install virtualenv`.

## Passo 1: Clonar o Repositório

Clone o repositório do GitHub para o seu sistema local:

```bash
git clone https://github.com/RobyellMartins/comercializacao-de-obras-his-fullstackweb.git
cd comercializacao-de-obras-his-fullstackweb
```

## Passo 2: Configurar o Backend (Flask)

1. Navegue para o diretório raiz do projeto (onde está o `requirements.txt`).

2. Crie e ative um ambiente virtual (recomendado):

   ```bash
   python -m venv venv
   # No Windows:
   venv\Scripts\activate
   # No Linux/Mac:
   source venv/bin/activate
   ```

3. Instale as dependências do Python:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure o banco de dados PostgreSQL:
   - Crie um banco de dados chamado `obras_his` (ou outro nome de sua escolha).
   - Atualize o arquivo `src/config.py` com as credenciais do seu banco de dados (usuário, senha, host, etc.).

5. Execute as migrações do banco de dados:

   ```bash
   alembic upgrade head
   ```

6. Execute o servidor backend:

   ```bash
   python src/app.py
   ```

   O backend estará rodando em `http://localhost:5000`.

## Passo 3: Configurar o Frontend (React)

1. Navegue para o diretório do frontend:

   ```bash
   cd obras-his-frontend
   ```

2. Instale as dependências do Node.js:

   ```bash
   npm install
   ```

3. Execute o servidor de desenvolvimento:

   ```bash
   npm start
   ```

   O frontend estará rodando em `http://localhost:3000`.

## Passo 4: Acessar a Aplicação

Abra o navegador e acesse `http://localhost:3000` para usar a aplicação. O frontend se comunicará com o backend em `http://localhost:5000`.

## Notas Adicionais

- Certifique-se de que o PostgreSQL esteja rodando antes de executar o backend.
- Se houver problemas com portas, ajuste as configurações nos arquivos `src/config.py` e `obras-his-frontend/src/services/api.js`.
- Para produção, considere usar um servidor como Gunicorn para o Flask e Nginx para servir o frontend.
- Execute os testes com `pytest` no diretório raiz para o backend e `npm test` no diretório do frontend.

## Suporte

Se encontrar problemas, verifique os logs do console ou consulte a documentação no repositório.
