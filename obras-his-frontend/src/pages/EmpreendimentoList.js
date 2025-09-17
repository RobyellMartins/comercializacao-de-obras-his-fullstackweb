import React, { useState, useEffect } from 'react';
import {
  Container,
  Paper,
  Typography,
  TextField,
  Button,
  Box,
  Alert,
  CircularProgress,
  Grid,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  FormControlLabel,
  Checkbox,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  IconButton,
  Card,
  CardContent,
} from '@mui/material';
import {
  List as ListIcon,
  Search as SearchIcon,
  Publish as PublishIcon,
  FilterList as FilterIcon,
  Business as BusinessIcon,
  Apartment as ApartmentIcon,
} from '@mui/icons-material';
import BackToHomeButton from '../components/BackToHomeButton';
import api from '../services/api';

const EmpreendimentoList = () => {
  const [empreendimentos, setEmpreendimentos] = useState([]);
  const [construtoras, setConstrutoras] = useState([]);
  const [filtros, setFiltros] = useState({
    construtoraId: '',
    nome: '',
    dataInicio: '',
    dataFim: '',
    publicados: false,
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [unidades, setUnidades] = useState([]);
  const [unidadesCount, setUnidadesCount] = useState(0);

  // Buscar construtoras para filtro
  useEffect(() => {
    const fetchConstrutoras = async () => {
      try {
        const res = await api.get('/api/construtoras');
        setConstrutoras(res.data);
      } catch (err) {
        console.error('Erro ao buscar construtoras', err);
      }
    };
    fetchConstrutoras();
  }, []);

  // Buscar unidades para dashboard
  useEffect(() => {
    const fetchUnidades = async () => {
      try {
        const res = await api.get('/unidades');
        setUnidades(res.data);
        setUnidadesCount(res.data.length);
      } catch (err) {
        console.error('Erro ao buscar unidades', err);
      }
    };
    fetchUnidades();
  }, []);

  // Buscar empreendimentos com filtros
  const buscarEmpreendimentos = async () => {
    setLoading(true);
    setError('');
    try {
      const params = {};

      if (filtros.construtoraId) params.construtora_id = filtros.construtoraId;
      if (filtros.nome) params.nome = filtros.nome;
      if (filtros.dataInicio) params.dataInicio = filtros.dataInicio;
      if (filtros.dataFim) params.dataFim = filtros.dataFim;
      if (filtros.publicados) params.somente_publicadas = '1';

      const res = await api.get('/empreendimentos', { params });
      setEmpreendimentos(res.data);
    } catch (err) {
      console.error('Erro ao buscar empreendimentos', err);
      setError('Erro ao buscar empreendimentos. Tente novamente.');
    } finally {
      setLoading(false);
    }
  };

  // Buscar empreendimentos ao carregar a página
  useEffect(() => {
    buscarEmpreendimentos();
  }, []);

  // Publicar empreendimento
  const handlePublicar = async (id) => {
    try {
      await api.post(`/empreendimentos/${id}/publicar`);
      // Recarregar lista após publicar
      buscarEmpreendimentos();
    } catch (err) {
      console.error('Erro ao publicar empreendimento', err);
      setError('Erro ao publicar empreendimento. Tente novamente.');
    }
  };

  // Limpar filtros
  const limparFiltros = () => {
    setFiltros({
      construtoraId: '',
      nome: '',
      dataInicio: '',
      dataFim: '',
      publicados: false,
    });
  };

  return (
    <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
      <BackToHomeButton />
      
      <Paper elevation={3} sx={{ p: 4 }}>
        <Box display="flex" alignItems="center" mb={3}>
          <ApartmentIcon sx={{ mr: 2, fontSize: 32, color: 'primary.main' }} />
          <Typography variant="h4" component="h1">
            Lista de Empreendimentos
          </Typography>
        </Box>

        {/* Dashboard Cards */}
        <Grid container spacing={3} sx={{ mb: 4 }}>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Box display="flex" alignItems="center">
                  <BusinessIcon sx={{ mr: 2, color: 'primary.main' }} />
                  <Box>
                    <Typography variant="h6">{empreendimentos.length}</Typography>
                    <Typography variant="body2" color="text.secondary">
                      Total de Empreendimentos
                    </Typography>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Box display="flex" alignItems="center">
                  <PublishIcon sx={{ mr: 2, color: 'success.main' }} />
                  <Box>
                    <Typography variant="h6">
                      {empreendimentos.filter(e => e.publicado_em).length}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Empreendimentos Publicados
                    </Typography>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Box display="flex" alignItems="center">
                  <ListIcon sx={{ mr: 2, color: 'info.main' }} />
                  <Box>
                    <Typography variant="h6">{unidadesCount}</Typography>
                    <Typography variant="body2" color="text.secondary">
                      Total de Unidades
                    </Typography>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        </Grid>

        {/* Filtros */}
        <Paper elevation={1} sx={{ p: 3, mb: 3, backgroundColor: 'grey.50' }}>
          <Box display="flex" alignItems="center" mb={2}>
            <FilterIcon sx={{ mr: 1 }} />
            <Typography variant="h6">Filtros</Typography>
          </Box>
          
          <Grid container spacing={2} alignItems="center">
            <Grid item xs={12} md={3}>
              <FormControl fullWidth size="small">
                <InputLabel>Construtora</InputLabel>
                <Select
                  value={filtros.construtoraId}
                  label="Construtora"
                  onChange={(e) => setFiltros({ ...filtros, construtoraId: e.target.value })}
                >
                  <MenuItem value="">Todas</MenuItem>
                  {construtoras.map((c) => (
                    <MenuItem key={c.id} value={c.id}>
                      {c.nome}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            
            <Grid item xs={12} md={3}>
              <TextField
                fullWidth
                size="small"
                label="Nome do Empreendimento"
                value={filtros.nome}
                onChange={(e) => setFiltros({ ...filtros, nome: e.target.value })}
              />
            </Grid>
            
            <Grid item xs={12} md={2}>
              <TextField
                fullWidth
                size="small"
                type="date"
                label="Data Início"
                InputLabelProps={{ shrink: true }}
                value={filtros.dataInicio}
                onChange={(e) => setFiltros({ ...filtros, dataInicio: e.target.value })}
              />
            </Grid>
            
            <Grid item xs={12} md={2}>
              <TextField
                fullWidth
                size="small"
                type="date"
                label="Data Fim"
                InputLabelProps={{ shrink: true }}
                value={filtros.dataFim}
                onChange={(e) => setFiltros({ ...filtros, dataFim: e.target.value })}
              />
            </Grid>
            
            <Grid item xs={12} md={2}>
              <FormControlLabel
                control={
                  <Checkbox
                    checked={filtros.publicados}
                    onChange={(e) => setFiltros({ ...filtros, publicados: e.target.checked })}
                  />
                }
                label="Apenas publicados"
              />
            </Grid>
          </Grid>
          
          <Box sx={{ mt: 2, display: 'flex', gap: 2 }}>
            <Button
              variant="contained"
              startIcon={<SearchIcon />}
              onClick={buscarEmpreendimentos}
              disabled={loading}
            >
              Buscar
            </Button>
            <Button
              variant="outlined"
              onClick={limparFiltros}
              disabled={loading}
            >
              Limpar Filtros
            </Button>
          </Box>
        </Paper>

        {/* Mensagem de erro */}
        {error && (
          <Alert severity="error" sx={{ mb: 3 }}>
            {error}
          </Alert>
        )}

        {/* Loading */}
        {loading && (
          <Box display="flex" justifyContent="center" my={4}>
            <CircularProgress />
          </Box>
        )}

        {/* Tabela de empreendimentos */}
        {!loading && empreendimentos.length === 0 && (
          <Alert severity="info">
            Nenhum empreendimento encontrado com os filtros aplicados.
          </Alert>
        )}

        {!loading && empreendimentos.length > 0 && (
          <TableContainer component={Paper} elevation={1}>
            <Table>
              <TableHead>
                <TableRow sx={{ backgroundColor: 'primary.light' }}>
                  <TableCell sx={{ fontWeight: 'bold', color: 'white' }}>Nome</TableCell>
                  <TableCell sx={{ fontWeight: 'bold', color: 'white' }}>Construtora</TableCell>
                  <TableCell sx={{ fontWeight: 'bold', color: 'white' }}>Endereço</TableCell>
                  <TableCell sx={{ fontWeight: 'bold', color: 'white' }}>Data Criação</TableCell>
                  <TableCell sx={{ fontWeight: 'bold', color: 'white' }}>Status</TableCell>
                  <TableCell sx={{ fontWeight: 'bold', color: 'white' }}>Ações</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {empreendimentos.map((e) => (
                  <TableRow
                    key={e.id}
                    sx={{
                      '&:hover': { backgroundColor: 'primary.light', opacity: 0.1 }
                    }}
                  >
                    <TableCell sx={{ fontWeight: 500 }}>{e.nome}</TableCell>
                    <TableCell>{e.construtora_nome || e.construtora_id}</TableCell>
                    <TableCell sx={{ maxWidth: 200, overflow: 'hidden', textOverflow: 'ellipsis' }}>
                      {e.endereco}
                    </TableCell>
                    <TableCell>
                      {e.created_at ? new Date(e.created_at).toLocaleDateString('pt-BR') : 'N/A'}
                    </TableCell>
                    <TableCell>
                      {e.publicado_em ? (
                        <Chip
                          label={`Publicado (${new Date(e.publicado_em).toLocaleDateString('pt-BR')})`}
                          color="success"
                          size="small"
                        />
                      ) : (
                        <Chip
                          label="Não publicado"
                          color="error"
                          size="small"
                        />
                      )}
                    </TableCell>
                    <TableCell>
                      {!e.publicado_em && (
                        <IconButton
                          onClick={() => handlePublicar(e.id)}
                          color="primary"
                          size="small"
                          sx={{
                            '&:hover': {
                              backgroundColor: 'primary.light',
                              color: 'white',
                            },
                          }}
                        >
                          <PublishIcon />
                        </IconButton>
                      )}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        )}

        {/* Resumo */}
        {empreendimentos.length > 0 && (
          <Box sx={{ mt: 3, p: 2, backgroundColor: 'grey.50', borderRadius: 2 }}>
            <Typography variant="body2" color="text.secondary">
              Total de empreendimentos encontrados: <strong>{empreendimentos.length}</strong>
            </Typography>
          </Box>
        )}
      </Paper>
    </Container>
  );
};

export default EmpreendimentoList;
