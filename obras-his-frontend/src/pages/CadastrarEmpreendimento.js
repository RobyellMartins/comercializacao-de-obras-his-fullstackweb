import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Paper,
  Typography,
  TextField,
  Button,
  Box,
  Alert,
  CircularProgress,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
} from '@mui/material';
import {
  Business as BusinessIcon,
} from '@mui/icons-material';
import BackToHomeButton from '../components/BackToHomeButton';
import api from '../services/api';

const CadastrarEmpreendimento = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    nome: '',
    nome_empresa: '',
    endereco: '',
    cep: '',
    observacao: '',
    construtora_id: '',
  });
  const [construtoras, setConstrutoras] = useState([]);
  const [loading, setLoading] = useState(false);
  const [loadingConstrutoras, setLoadingConstrutoras] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  // Carregar construtoras ao montar o componente
  useEffect(() => {
    const carregarConstrutoras = async () => {
      try {
        const response = await api.get('/api/construtoras');
        setConstrutoras(response.data);
      } catch (err) {
        setError('Erro ao carregar construtoras');
      } finally {
        setLoadingConstrutoras(false);
      }
    };

    carregarConstrutoras();
  }, []);

  // Manipular mudanças nos campos do formulário
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  // Enviar formulário
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');

    try {
      await api.post('/empreendimentos', formData);
      setSuccess('Empreendimento cadastrado com sucesso!');
      setTimeout(() => {
        navigate('/empreendimentos/listar');
      }, 1500);
    } catch (err) {
      console.error('Erro ao cadastrar empreendimento', err);
      if (err.response?.data?.error) {
        setError(err.response.data.error);
      } else {
        setError('Erro ao cadastrar empreendimento. Tente novamente.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="sm" sx={{ mt: 4, mb: 4 }}>
      <BackToHomeButton />

      <Paper sx={{ p: 4 }}>
        <Box display="flex" alignItems="center" justifyContent="center" mb={3}>
          <BusinessIcon sx={{ mr: 2, fontSize: 32, color: 'primary.main' }} />
          <Typography variant="h4" component="h1" align="center">
            Cadastrar Empreendimento
          </Typography>
        </Box>

        <Typography variant="subtitle1" align="center" color="text.secondary" sx={{ mb: 3 }}>
          Comercialização de Obras HIS
        </Typography>

        {/* Mensagens de erro e sucesso */}
        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        {success && (
          <Alert severity="success" sx={{ mb: 2 }}>
            {success}
          </Alert>
        )}

        <Box component="form" onSubmit={handleSubmit} noValidate>
          {/* Nome do Empreendimento */}
          <TextField
            label="Nome do Empreendimento"
            name="nome"
            value={formData.nome}
            onChange={handleChange}
            fullWidth
            margin="normal"
            required
            placeholder="Ex: Residencial Vista Bela, Condomínio Jardim Primavera"
            helperText="Informe o nome completo do empreendimento"
            disabled={loading}
          />

          {/* Nome da Empresa */}
          <TextField
            label="Nome da Empresa/Construtora"
            name="nome_empresa"
            value={formData.nome_empresa}
            onChange={handleChange}
            fullWidth
            margin="normal"
            placeholder="Ex: Construtora ABC Ltda, Empreendimentos XYZ S.A."
            helperText="Nome da empresa responsável pelo empreendimento"
            disabled={loading}
          />

          {/* Dropdown de Construtoras */}
          <FormControl fullWidth margin="normal">
            <InputLabel id="construtora-label">Selecione a Construtora Responsável (Opcional)</InputLabel>
            <Select
              labelId="construtora-label"
              name="construtora_id"
              value={formData.construtora_id}
              onChange={handleChange}
              label="Selecione a Construtora Responsável (Opcional)"
              disabled={loading || loadingConstrutoras}
              displayEmpty
            >
              <MenuItem value="">
                <em>Nenhuma construtora selecionada</em>
              </MenuItem>
              {loadingConstrutoras ? (
                <MenuItem disabled>
                  <CircularProgress size={20} sx={{ mr: 1 }} />
                  Carregando construtoras...
                </MenuItem>
              ) : construtoras.length === 0 ? (
                <MenuItem disabled>Nenhuma construtora cadastrada</MenuItem>
              ) : (
                construtoras.map((construtora) => (
                  <MenuItem key={construtora.id} value={construtora.id}>
                    <Box>
                      <Typography variant="body1" sx={{ fontWeight: 500 }}>
                        {construtora.nome}
                      </Typography>
                      {construtora.cnpj && (
                        <Typography variant="caption" color="text.secondary" display="block">
                          CNPJ: {construtora.cnpj}
                        </Typography>
                      )}
                      {construtora.telefone && (
                        <Typography variant="caption" color="text.secondary" display="block">
                          Tel: {construtora.telefone}
                        </Typography>
                      )}
                    </Box>
                  </MenuItem>
                ))
              )}
            </Select>
          </FormControl>

          {/* CEP */}
          <TextField
            label="CEP"
            name="cep"
            value={formData.cep}
            onChange={handleChange}
            fullWidth
            margin="normal"
            required
            placeholder="00000-000"
            helperText="CEP do empreendimento para localização"
            disabled={loading}
          />

          {/* Endereço */}
          <TextField
            label="Endereço Completo"
            name="endereco"
            value={formData.endereco}
            onChange={handleChange}
            fullWidth
            margin="normal"
            multiline
            rows={2}
            placeholder="Rua, número, bairro, cidade - UF"
            helperText="Endereço completo do empreendimento"
            disabled={loading}
          />

          {/* Observação */}
          <TextField
            label="Observações"
            name="observacao"
            value={formData.observacao}
            onChange={handleChange}
            fullWidth
            margin="normal"
            multiline
            rows={3}
            placeholder="Informações adicionais sobre o empreendimento..."
            helperText="Observações gerais, características especiais, etc."
            disabled={loading}
          />

          {/* Botões */}
          <Box sx={{ mt: 3, display: 'flex', gap: 2, justifyContent: 'flex-end' }}>
            <Button
              variant="outlined"
              onClick={() => navigate('/')}
              disabled={loading}
            >
              Cancelar
            </Button>
            <Button
              type="submit"
              variant="contained"
              disabled={loading || loadingConstrutoras}
              sx={{ minWidth: 120 }}
            >
              {loading ? <CircularProgress size={24} /> : 'Cadastrar Empreendimento'}
            </Button>
          </Box>
        </Box>
      </Paper>
    </Container>
  );
};

export default CadastrarEmpreendimento;
