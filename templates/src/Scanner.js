import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FaShieldAlt, FaExclamationTriangle, FaCheckCircle, FaLink } from 'react-icons/fa';
import ParticlesBackground from './ParticlesBackground';
// Note: We do NOT import App.css here if it's already imported in index.js or App.js, 
// but it is safe to leave it if your styles rely on it.

function Scanner() {
  const [url, setUrl] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleSubmit = async (e) => {
  e.preventDefault();
  if (!url) return;

  setIsLoading(true);
  setResult(null);

  try {
    const response = await fetch("http://127.0.0.1:5000/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ url: url }),
    });

    const data = await response.json();

    setResult({
      status: data.prediction === 1 ? "phishing" : "safe",
      message: data.prediction === 1 
        ? "Phishing Detected!" 
        : "Website is Safe",
      confidence: data.confidence || "95%"
    });

  } catch (error) {
    console.error("Error:", error);
    setResult({
      status: "phishing",
      message: "Server Error",
      confidence: "-"
    });
  }

  setIsLoading(false);
};


  return (
    <div className="app-container">
      <ParticlesBackground />

      <motion.div 
        className="glass-card"
        initial={{ opacity: 0, y: 50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <div className="header">
          <motion.div 
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: 0.2, type: "spring", stiffness: 150 }}
            className="icon-wrapper"
          >
            <FaShieldAlt className="shield-icon" />
          </motion.div>
          <h1>Phishing Detection</h1>
          <p>Paste a URL to check if it's safe or fake.</p>
        </div>

        <form onSubmit={handleSubmit} className="search-form">
          <div className="input-group">
            <FaLink className="input-icon" />
            <input 
              type="url" 
              placeholder="https://example.com" 
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              required
            />
          </div>

          <motion.button 
            type="submit" 
            className="analyze-btn"
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            disabled={isLoading || !url}
          >
            {isLoading ? <span className="loader">Scanning...</span> : "Scan URL"}
          </motion.button>
        </form>

        <AnimatePresence>
          {result && (
            <motion.div 
              className={`result-card ${result.status}`}
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
            >
              <div className="result-icon">
                {result.status === 'safe' ? <FaCheckCircle /> : <FaExclamationTriangle />}
              </div>
              <div className="result-text">
                <h3>{result.message}</h3>
                <p>Confidence: {result.confidence}</p>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </motion.div>
    </div>
  );
}

export default Scanner;