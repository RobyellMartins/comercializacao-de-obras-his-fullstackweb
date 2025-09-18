from marshmallow import Schema, fields, validate, post_load
from datetime import datetime

class ConstrutorSchema(Schema):
    id = fields.Int(dump_only=True)
    nome = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    cnpj = fields.Str(validate=validate.Length(max=18))
    telefone = fields.Str(validate=validate.Length(max=20))
    email = fields.Email(validate=validate.Length(max=255))
    endereco = fields.Str()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

class EmpreendimentoSchema(Schema):
    id = fields.Int(dump_only=True)
    nome = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    nome_empresa = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    endereco = fields.Str()
    cep = fields.Str(required=True, validate=validate.Length(max=10))
    observacao = fields.Str()
    construtora_id = fields.Int(allow_none=True)  # Agora opcional
    construtora_nome = fields.Str(dump_only=True)
    publicado_em = fields.DateTime(dump_only=True)
    expira_em = fields.DateTime(dump_only=True)
    status_publicacao = fields.Str(validate=validate.OneOf(['aguardando', 'publicado', 'expirado']), dump_default='aguardando')
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

class ObraSchema(Schema):
    id = fields.Int(dump_only=True)
    nome = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    descricao = fields.Str()
    empreendimento_id = fields.Int(required=True)
    status = fields.Str(validate=validate.Length(max=50))
    data_inicio = fields.DateTime()
    data_fim_prevista = fields.DateTime()
    data_fim_real = fields.DateTime()
    valor_orcado = fields.Float(validate=validate.Range(min=0))
    valor_executado = fields.Float(validate=validate.Range(min=0))
    percentual_concluido = fields.Float(validate=validate.Range(min=0, max=100))
    publicado_em = fields.DateTime(dump_only=True)
    expira_em = fields.DateTime(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

class UnidadeSchema(Schema):
    id = fields.Int(dump_only=True)
    numero_unidade = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    empreendimento_id = fields.Int(required=True)
    tamanho_m2 = fields.Float(validate=validate.Range(min=0))
    preco_venda = fields.Float(validate=validate.Range(min=0))
    mecanismo_pagamento = fields.Str(required=True, validate=validate.Length(max=32))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

# Schemas para filtros e buscas
class EmpreendimentoFiltroSchema(Schema):
    nome = fields.Str()
    cep = fields.Str()
    construtora_id = fields.Int()
    somente_publicadas = fields.Bool()
    data_inicio = fields.DateTime()
    data_fim = fields.DateTime()
    
class ObraFiltroSchema(Schema):
    nome = fields.Str()
    empreendimento_id = fields.Int()
    status = fields.Str()
    somente_publicadas = fields.Bool()
    data_inicio = fields.DateTime()
    data_fim = fields.DateTime()

# Schema para upload de planilha
class UploadResponseSchema(Schema):
    empreendimentos_processados = fields.Int()
    unidades_processadas = fields.Int()
    erros = fields.Int()
    detalhes_erros = fields.List(fields.Str())
    empreendimentos = fields.List(fields.Nested(EmpreendimentoSchema))
    unidades = fields.List(fields.Nested(UnidadeSchema))

# Schema para resposta de erro
class ErrorSchema(Schema):
    error = fields.Str(required=True)
    message = fields.Str()
    details = fields.Raw()

# Schema para resposta de sucesso
class SuccessSchema(Schema):
    message = fields.Str(required=True)
    data = fields.Raw()
