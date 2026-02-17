import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FaShieldAlt, FaExclamationTriangle, FaCheckCircle, FaLink } from 'react-icons/fa';
import ParticlesBackground from './ParticlesBackground';

function Scanner() {
  const [url, setUrl] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState(null);
  const handleInputChange = (e) => {
    const newUrl = e.target.value;
    setUrl(newUrl);
    setResult(null);
  };

const handleSubmit = async (e) => {
  e.preventDefault();
  if (!url) return;

  setIsLoading(true);
  setResult(null);
  const API_URL = 'https://phishing-website-detection-at66.onrender.com';

    try {
      const response = await fetch(`${API_URL}/predict`, { 
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: url }),
      });

    const data = await response.json();
    console.log("WHAT PYTHON SENT:", data);
    if (response.ok) {
        setResult(data);
    }
  } catch (error) {
    console.error("Connection Error:", error);
    alert("Could not connect to the backend. Is Python running?");
  } finally {
    setIsLoading(false);
  }
};

  return (
    <div className="app-container">

      <ParticlesBackground delay={200} />

      <div className="glass-card">
        
        <div className="header">
          <motion.div 
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: 0.1 }}
            className="icon-wrapper"
          >
            <FaShieldAlt className="shield-icon" />
          </motion.div>
          <h1>Phishing Detection</h1>
          <p>Paste a URL to check if it's safe or fake.</p>
        </div>

        <motion.form 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.2 }}
            onSubmit={handleSubmit} 
            className="search-form"
        >
          <div className="input-group">
            <FaLink className="input-icon" />
            <input 
              type="url" 
              placeholder="https://example.com" 
              value={url}
              onChange={handleInputChange}
              required
            />
          </div>

          <button 
            type="submit" 
            className="analyze-btn"
            disabled={isLoading || !url}
          >
            {isLoading ? <span className="loader">Scanning...</span> : "Scan URL"}
          </button>
        </motion.form>

        <AnimatePresence>
          {result && result.prediction && (
            <motion.div 
              className={`result-card ${result.prediction.toLowerCase()}`}
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
            >
              <div className="result-icon">
                {result.prediction === 'Safe' ? <FaCheckCircle /> : <FaExclamationTriangle />}
              </div>
              <div className="result-text">
                <h3 style={{ 
                  color: result.prediction === 'Safe' ? '#00ff88' : '#ff0055',
                  textShadow: result.prediction === 'Safe' ? '0 0 10px rgba(0,255,136,0.3)' : '0 0 10px rgba(255,0,85,0.3)'
                }}>
                  {result.prediction.toUpperCase()}
                </h3>
                {result.confidence ? (
                  <p style={{ color: '#ccc', fontSize: '0.9rem' }}>
                    Confidence: <span style={{ color: '#fff', fontWeight: 'bold' }}>{result.confidence}%</span>
                  </p>
                ) : (
                  <p style={{ color: '#ffcc00' }}>Error: No confidence data</p>
                )}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}

export default Scanner;
