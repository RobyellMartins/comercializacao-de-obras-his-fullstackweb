import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Typography,
  Box,
  Grid,
  Card,
  CardContent,
  Button,
  Paper,
  useTheme,
  useMediaQuery
} from '@mui/material';
import {
  Business as BusinessIcon,
  Home as HomeIcon,
  List as ListIcon,
  CloudUpload as UploadIcon,
  Construction as ConstructionIcon
} from '@mui/icons-material';

const Home = () => {
  const navigate = useNavigate();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));

  const menuItems = [
    {
      title: 'Cadastrar Empreendimento',
      description: 'Registre novos empreendimentos habitacionais',
      icon: <BusinessIcon sx={{ fontSize: 40 }} />,
      path: '/empreendimentos/cadastrar',
      color: theme.palette.primary.main,
    },
    {
      title: 'Cadastrar Unidade',
      description: 'Adicione unidades aos empreendimentos',
      icon: <HomeIcon sx={{ fontSize: 40 }} />,
      path: '/unidades/cadastrar',
      color: theme.palette.secondary.main,
    },
    {
      title: 'Listar Empreendimentos',
      description: 'Visualize todos os empreendimentos cadastrados',
      icon: <ListIcon sx={{ fontSize: 40 }} />,
      path: '/empreendimentos/listar',
      color: theme.palette.success.main,
    },
    {
      title: 'Upload de Planilha',
      description: 'Importe dados através de planilhas',
      icon: <UploadIcon sx={{ fontSize: 40 }} />,
      path: '/upload',
      color: theme.palette.warning.main,
    },
  ];

  return (
    <Box
      sx={{
        minHeight: 'calc(100vh - 64px)',
        background: `linear-gradient(135deg, ${theme.palette.primary.light}15 0%, ${theme.palette.secondary.light}15 100%)`,
        py: 4,
      }}
    >
      <Container maxWidth="lg">
        {/* Título centralizado */}
        <Box
          sx={{
            textAlign: 'center',
            mb: 6,
            pt: 4,
          }}
        >
          <Typography
            variant="h1"
            component="h1"
            sx={{
              background: `linear-gradient(135deg, ${theme.palette.primary.main} 0%, ${theme.palette.secondary.main} 100%)`,
              backgroundClip: 'text',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              fontSize: isMobile ? '2rem' : '3rem',
              fontWeight: 800,
              textAlign: 'center',
              mb: 3,
            }}
          >
            Publicização de Obras HIS
          </Typography>
          
          <Typography
            variant="h5"
            component="p"
            sx={{
              color: theme.palette.text.secondary,
              fontWeight: 400,
              maxWidth: 600,
              mx: 'auto',
              fontSize: isMobile ? '1.1rem' : '1.25rem',
            }}
          >
            Sistema de gestão e acompanhamento de obras de habitação de interesse social
          </Typography>
        </Box>

        {/* Cards de navegação */}
        <Grid 
          container 
          spacing={3} 
          justifyContent="center" 
          alignItems="stretch"
          sx={{ maxWidth: '1000px', mx: 'auto' }}
        >
          {menuItems.map((item, index) => (
            <Grid 
              item 
              xs={12} 
              sm={6} 
              md={6} 
              lg={6}
              key={index} 
              sx={{ 
                display: 'flex',
                justifyContent: 'center',
              }}
            >
              <Card
                sx={{
                  height: '280px',
                  width: '100%',
                  maxWidth: '450px',
                  cursor: 'pointer',
                  transition: 'all 0.3s ease-in-out',
                  display: 'flex',
                  flexDirection: 'column',
                  '&:hover': {
                    transform: 'translateY(-8px)',
                    boxShadow: theme.shadows[8],
                  },
                }}
                onClick={() => navigate(item.path)}
              >
                <CardContent
                  sx={{
                    textAlign: 'center',
                    p: 4,
                    height: '100%',
                    display: 'flex',
                    flexDirection: 'column',
                    justifyContent: 'space-between',
                  }}
                >
                  {/* Seção do ícone */}
                  <Box 
                    sx={{ 
                      height: '80px',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      mb: 2,
                      color: item.color,
                    }}
                  >
                    {item.icon}
                  </Box>
                  
                  {/* Seção do conteúdo */}
                  <Box sx={{ flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
                    <Typography
                      variant="h5"
                      component="h3"
                      sx={{
                        fontWeight: 600,
                        mb: 2,
                        color: theme.palette.text.primary,
                        fontSize: '1.25rem',
                      }}
                    >
                      {item.title}
                    </Typography>
                    
                    <Typography
                      variant="body1"
                      sx={{
                        color: theme.palette.text.secondary,
                        lineHeight: 1.6,
                        mb: 3,
                      }}
                    >
                      {item.description}
                    </Typography>
                  </Box>
                  
                  {/* Seção do botão */}
                  <Box sx={{ mt: 2 }}>
                    <Button
                      variant="contained"
                      fullWidth
                      sx={{
                        backgroundColor: item.color,
                        '&:hover': {
                          backgroundColor: item.color,
                          filter: 'brightness(0.9)',
                        },
                        py: 1.5,
                        fontSize: '1rem',
                        fontWeight: 600,
                      }}
                    >
                      Acessar
                    </Button>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>

        {/* Seção informativa */}
        <Paper
          elevation={2}
          sx={{
            mt: 6,
            p: 4,
            textAlign: 'center',
            background: `linear-gradient(135deg, ${theme.palette.background.paper} 0%, ${theme.palette.primary.light}08 100%)`,
          }}
        >
          <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', mb: 3 }}>
            <ConstructionIcon sx={{ fontSize: 32, color: theme.palette.primary.main, mr: 2 }} />
            <Typography
              variant="h5"
              sx={{
                color: theme.palette.text.primary,
                fontWeight: 600,
              }}
            >
              Sistema de Gestão Habitacional
            </Typography>
          </Box>
          
          <Typography
            variant="body1"
            sx={{
              color: theme.palette.text.secondary,
              maxWidth: 800,
              mx: 'auto',
              lineHeight: 1.7,
              fontSize: '1.1rem',
            }}
          >
            Plataforma integrada para o gerenciamento completo de empreendimentos habitacionais de interesse social,
            proporcionando transparência e eficiência na gestão pública.
          </Typography>

          <Box sx={{ mt: 4 }}>
            <Grid container spacing={3} justifyContent="center">
              <Grid item xs={12} sm={4}>
                <Typography variant="h6" sx={{ color: theme.palette.primary.main, fontWeight: 600, mb: 1 }}>
                  Gestão Completa
                </Typography>
                <Typography variant="body2" sx={{ color: theme.palette.text.secondary }}>
                  Controle total dos empreendimentos e suas informações
                </Typography>
              </Grid>
              <Grid item xs={12} sm={4}>
                <Typography variant="h6" sx={{ color: theme.palette.secondary.main, fontWeight: 600, mb: 1 }}>
                  Importação Fácil
                </Typography>
                <Typography variant="body2" sx={{ color: theme.palette.text.secondary }}>
                  Upload de planilhas para cadastro em lote
                </Typography>
              </Grid>
              <Grid item xs={12} sm={4}>
                <Typography variant="h6" sx={{ color: theme.palette.success.main, fontWeight: 600, mb: 1 }}>
                  Interface Moderna
                </Typography>
                <Typography variant="body2" sx={{ color: theme.palette.text.secondary }}>
                  Design responsivo e intuitivo para todos os usuários
                </Typography>
              </Grid>
            </Grid>
          </Box>
        </Paper>
      </Container>
    </Box>
  );
};

export default Home;
