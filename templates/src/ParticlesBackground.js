import React, { useRef, useEffect } from 'react';

const ParticlesBackground = () => {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    let animationFrameId;

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const fontSize = 14;
    const columns = canvas.width / fontSize;
    const drops = [];
    for (let x = 0; x < columns; x++) {
      drops[x] = 1;
    }

    // Mouse Tracking
    let mouse = { x: -1000, y: -1000 };
    const handleMouseMove = (e) => {
      mouse.x = e.clientX;
      mouse.y = e.clientY;
    };
    window.addEventListener('mousemove', handleMouseMove);

    // ONLY BINARY CHARACTERS NOW
    const chars = "01";
    const charArray = chars.split("");

    const draw = () => {
      // 1. CLEAR: Low opacity black for trail effect
      ctx.fillStyle = 'rgba(0, 4, 40, 0.1)'; 
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      ctx.font = fontSize + "px monospace";

      for (let i = 0; i < drops.length; i++) {
        const x = i * fontSize;
        const y = drops[i] * fontSize;

        // Interaction
        const dist = Math.hypot(x - mouse.x, y - mouse.y);
        const isHovered = dist < 100;

        // Pick character (0 or 1)
        const text = charArray[Math.floor(Math.random() * charArray.length)];

        // Colors
        if (isHovered) {
            ctx.fillStyle = '#ffffff'; // White hot on hover
            ctx.shadowBlur = 10;
            ctx.shadowColor = '#ffffff';
        } else {
            ctx.fillStyle = '#00f3ff'; // CYAN text
            ctx.shadowBlur = 0;
        }

        ctx.fillText(text, x, y);

        // Reset
        if (drops[i] * fontSize > canvas.height && Math.random() > 0.98) {
          drops[i] = 0;
        }

        // Speed
        drops[i] += isHovered ? 0.5 : 0.1;
      }
    };

    const animate = () => {
      draw();
      animationFrameId = requestAnimationFrame(animate);
    };

    const handleResize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };

    window.addEventListener('resize', handleResize);
    animate();

    return () => {
      window.removeEventListener('resize', handleResize);
      window.removeEventListener('mousemove', handleMouseMove);
      cancelAnimationFrame(animationFrameId);
    };
  }, []);

  return (
    <canvas 
      ref={canvasRef} 
      style={{ 
        position: 'absolute', 
        top: 0, 
        left: 0, 
        zIndex: 0,
      }} 
    />
  );
};

export default ParticlesBackground;
