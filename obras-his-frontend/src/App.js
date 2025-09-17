import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, CssBaseline } from '@mui/material';
import theme from './themes/theme';
import Header from './components/Header';
import Home from './pages/Home';
import EmpreendimentoList from './pages/EmpreendimentoList';
import UploadPlanilha from './pages/UploadPlanilha';
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
          <Route path="/upload" element={<UploadPlanilha />} />
        </Routes>
      </Router>
    </ThemeProvider>
  );
}

export default App;
