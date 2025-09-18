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
            Comercialização de Obras HIS
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
        <Box
          sx={{
            display: 'flex',
            flexDirection: 'row',
            gap: 3,
            justifyContent: 'center',
            alignItems: 'stretch',
            flexWrap: 'nowrap',
            maxWidth: '1000px',
            mx: 'auto'
          }}
        >
          {menuItems.map((item, index) => (
            <Card
              key={index}
              sx={{
                height: '280px',
                width: '220px',
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
                    p: 3,
                    height: '100%',
                    display: 'flex',
                    flexDirection: 'column',
                    justifyContent: 'space-between',
                  }}
                >
                  {/* Seção do ícone */}
                  <Box
                    sx={{
                      height: '60px',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      mb: 1,
                      color: item.color,
                    }}
                  >
                    {React.cloneElement(item.icon, { sx: { fontSize: 30 } })}
                  </Box>

                  {/* Seção do conteúdo */}
                  <Box sx={{ flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
                    <Typography
                      variant="h5"
                      component="h3"
                      sx={{
                        fontWeight: 600,
                        mb: 1,
                        color: theme.palette.text.primary,
                        fontSize: '1rem',
                      }}
                    >
                      {item.title}
                    </Typography>

                    <Typography
                      variant="body1"
                      sx={{
                        color: theme.palette.text.secondary,
                        lineHeight: 1.4,
                        mb: 2,
                        fontSize: '0.8rem',
                      }}
                    >
                      {item.description}
                    </Typography>
                  </Box>

                  {/* Seção do botão */}
                  <Box sx={{ mt: 1 }}>
                    <Button
                      variant="contained"
                      fullWidth
                      sx={{
                        backgroundColor: item.color,
                        '&:hover': {
                          backgroundColor: item.color,
                          filter: 'brightness(0.9)',
                        },
                        py: 1,
                        fontSize: '0.8rem',
                        fontWeight: 600,
                      }}
                    >
                      Acessar
                    </Button>
                  </Box>
                </CardContent>
              </Card>
          ))}
        </Box>

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


        </Paper>
      </Container>
    </Box>
  );
};

export default Home;
