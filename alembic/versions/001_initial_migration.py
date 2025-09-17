"""Initial migration - Create all tables

Revision ID: 001_initial_migration
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision = '001_initial_migration'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create construtoras table
    op.create_table('construtoras',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nome', sa.String(length=255), nullable=False),
        sa.Column('cnpj', sa.String(length=18), nullable=True),
        sa.Column('telefone', sa.String(length=20), nullable=True),
        sa.Column('email', sa.String(length=255), nullable=True),
        sa.Column('endereco', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True, default=datetime.utcnow),
        sa.Column('updated_at', sa.DateTime(), nullable=True, default=datetime.utcnow),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create empreendimentos table
    op.create_table('empreendimentos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nome', sa.String(length=255), nullable=False),
        sa.Column('endereco', sa.Text(), nullable=True),
        sa.Column('cidade', sa.String(length=100), nullable=True),
        sa.Column('estado', sa.String(length=2), nullable=True),
        sa.Column('cep', sa.String(length=10), nullable=True),
        sa.Column('tipo', sa.String(length=100), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=True, default='Em planejamento'),
        sa.Column('valor_total', sa.Float(), nullable=True),
        sa.Column('unidades', sa.Integer(), nullable=True),
        sa.Column('construtora_id', sa.Integer(), nullable=True),
        sa.Column('publicado_em', sa.DateTime(), nullable=True),
        sa.Column('expira_em', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True, default=datetime.utcnow),
        sa.Column('updated_at', sa.DateTime(), nullable=True, default=datetime.utcnow),
        sa.ForeignKeyConstraint(['construtora_id'], ['construtoras.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create obras table
    op.create_table('obras',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nome', sa.String(length=255), nullable=False),
        sa.Column('descricao', sa.Text(), nullable=True),
        sa.Column('empreendimento_id', sa.Integer(), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=True, default='Não iniciada'),
        sa.Column('data_inicio', sa.DateTime(), nullable=True),
        sa.Column('data_fim_prevista', sa.DateTime(), nullable=True),
        sa.Column('data_fim_real', sa.DateTime(), nullable=True),
        sa.Column('valor_orcado', sa.Float(), nullable=True),
        sa.Column('valor_executado', sa.Float(), nullable=True),
        sa.Column('percentual_concluido', sa.Float(), nullable=True, default=0.0),
        sa.Column('publicado_em', sa.DateTime(), nullable=True),
        sa.Column('expira_em', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True, default=datetime.utcnow),
        sa.Column('updated_at', sa.DateTime(), nullable=True, default=datetime.utcnow),
        sa.ForeignKeyConstraint(['empreendimento_id'], ['empreendimentos.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create unidades table
    op.create_table('unidades',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('numero_unidade', sa.String(length=50), nullable=False),
        sa.Column('empreendimento_id', sa.Integer(), nullable=True),
        sa.Column('tipo', sa.String(length=50), nullable=True),
        sa.Column('area_m2', sa.Float(), nullable=True),
        sa.Column('quartos', sa.Integer(), nullable=True),
        sa.Column('banheiros', sa.Integer(), nullable=True),
        sa.Column('vagas_garagem', sa.Integer(), nullable=True),
        sa.Column('preco_venda', sa.Float(), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=True, default='Disponível'),
        sa.Column('created_at', sa.DateTime(), nullable=True, default=datetime.utcnow),
        sa.Column('updated_at', sa.DateTime(), nullable=True, default=datetime.utcnow),
        sa.ForeignKeyConstraint(['empreendimento_id'], ['empreendimentos.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes
    op.create_index('ix_empreendimentos_publicados', 'empreendimentos', ['expira_em', 'publicado_em'], unique=False)
    op.create_index('ix_empreendimentos_cep', 'empreendimentos', ['cep'], unique=False)
    op.create_index('ix_obras_publicadas', 'obras', ['expira_em', 'publicado_em'], unique=False)
    op.create_index('ix_unidades_empreendimento', 'unidades', ['empreendimento_id', 'numero_unidade'], unique=True)

def downgrade():
    # Drop indexes
    op.drop_index('ix_unidades_empreendimento', table_name='unidades')
    op.drop_index('ix_obras_publicadas', table_name='obras')
    op.drop_index('ix_empreendimentos_cep', table_name='empreendimentos')
    op.drop_index('ix_empreendimentos_publicados', table_name='empreendimentos')
    
    # Drop tables
    op.drop_table('unidades')
    op.drop_table('obras')
    op.drop_table('empreendimentos')
    op.drop_table('construtoras')
