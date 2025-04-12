import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Footer from './components/Footer';
import Dashboard from './pages/Dashboard';
import QueryHistory from './pages/QueryHistory';
import About from './pages/About';

function App() {
  return (
    <div className="app-container">
      <Header />
      <main className="budget-assistant-container">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/history" element={<QueryHistory />} />
          <Route path="/about" element={<About />} />
        </Routes>
      </main>
      <Footer />
    </div>
  );
}

export default App;
