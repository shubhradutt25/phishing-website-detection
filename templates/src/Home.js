import React from 'react';
import { useNavigate } from 'react-router-dom';
import ParticlesBackground from './ParticlesBackground'; // Re-using your cool background
import { motion } from 'framer-motion';
import { FaCode, FaLock, FaUserSecret } from 'react-icons/fa';
import './Home.css'; // We will create this next

const Home = () => {
  const navigate = useNavigate();

  return (
    <div className="home-container">
      {/* Background Animation */}
      <ParticlesBackground />

      <div className="content-wrapper">
        
        {/* Hero Section */}
        <motion.div 
          className="hero-section"
          initial={{ opacity: 0, y: -50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          <div className="glitch-wrapper">
            <h1 className="glitch" data-text="PHISHING DETECTION">PHISHING DETECTION</h1>
          </div>
          <p className="subtitle">Advanced AI-driven security to protect you from malicious URLs.</p>
          
          <motion.button 
            className="cta-btn"
            whileHover={{ scale: 1.05, boxShadow: "0 0 20px #00f3ff" }}
            whileTap={{ scale: 0.95 }}
            onClick={() => navigate('/scan')}
          >
            LAUNCH SCANNER
          </motion.button>
        </motion.div>

        {/* Features Grid */}
        <div className="features-grid">
          <FeatureCard 
            icon={<FaCode />} 
            title="AI Analysis" 
            desc="Uses Machine Learning algorithms to detect patterns in fake URLs." 
            delay={0.2}
          />
          <FeatureCard 
            icon={<FaLock />} 
            title="Real-Time Protection" 
            desc="Instant scanning provides immediate feedback on link safety." 
            delay={0.4}
          />
          <FeatureCard 
            icon={<FaUserSecret />} 
            title="Anti-Fraud" 
            desc="Identifies social engineering attacks before you click." 
            delay={0.6}
          />
        </div>

      </div>
    </div>
  );
};

// Small helper component for cards
const FeatureCard = ({ icon, title, desc, delay }) => (
  <motion.div 
    className="feature-card"
    initial={{ opacity: 0, y: 30 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ delay: delay, duration: 0.6 }}
  >
    <div className="card-icon">{icon}</div>
    <h3>{title}</h3>
    <p>{desc}</p>
  </motion.div>
);

export default Home;