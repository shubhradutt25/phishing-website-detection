import React from 'react';
import { HashRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './Home';
import Scanner from './Scanner'; // We import the scanner here
import './App.css';

// This function MUST be named App, not Scanner
function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/scan" element={<Scanner />} />
      </Routes>
    </Router>
  );
}

export default App;
