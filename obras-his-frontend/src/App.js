import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, CssBaseline } from '@mui/material';
import theme from './themes/theme';
import Header from './components/Header';
import Home from './pages/Home';
import EmpreendimentoList from './pages/EmpreendimentoList';
import CadastrarEmpreendimento from './pages/CadastrarEmpreendimento';
import UploadPlanilha from './pages/UploadPlanilha';
import CadastrarUnidade from './pages/CadastrarUnidade';
import './styles/modern.css';

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Header />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/empreendimentos" element={<EmpreendimentoList />} />
          <Route path="/empreendimentos/listar" element={<EmpreendimentoList />} />
          <Route path="/empreendimentos/cadastrar" element={<CadastrarEmpreendimento />} />
          <Route path="/unidades/cadastrar" element={<CadastrarUnidade />} />
          <Route path="/upload" element={<UploadPlanilha />} />
        </Routes>
      </Router>
    </ThemeProvider>
  );
}

export default App;
