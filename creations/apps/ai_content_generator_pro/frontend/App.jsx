import React, { useState } from 'react';
import './App.css';

function App() {
  const [topic, setTopic] = useState('');
  const [keywords, setKeywords] = useState('');
  const [content, setContent] = useState(null);
  const [loading, setLoading] = useState(false);

  const generateContent = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8001/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          topic,
          keywords: keywords.split(',').map(k => k.trim()),
          content_type: 'blog',
          tone: 'professional',
          length: 'medium'
        })
      });
      
      const data = await response.json();
      setContent(data);
    } catch (error) {
      console.error('Error:', error);
    }
    setLoading(false);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🚀 AI Content Generator Pro</h1>
        <p>Genera contenuti SEO-optimized con AI - Creato da Aether</p>
      </header>
      
      <main>
        <div className="generator-form">
          <input
            type="text"
            placeholder="Argomento del contenuto..."
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
          />
          
          <input
            type="text"
            placeholder="Keywords (separate da virgola)..."
            value={keywords}
            onChange={(e) => setKeywords(e.target.value)}
          />
          
          <button onClick={generateContent} disabled={loading}>
            {loading ? 'Generando...' : 'Genera Contenuto'}
          </button>
        </div>
        
        {content && (
          <div className="content-result">
            <h2>{content.title}</h2>
            <div className="meta">
              <span>SEO Score: {content.seo_score * 100}%</span>
              <span>Parole: {content.word_count}</span>
            </div>
            <div className="content-body">
              {content.content}
            </div>
          </div>
        )}
        
        <div className="pricing">
          <h2>💰 Inizia a Guadagnare</h2>
          <div className="pricing-cards">
            <div className="card">
              <h3>Basic</h3>
              <p className="price">€19.99/mese</p>
              <ul>
                <li>50 contenuti/mese</li>
                <li>Blog e social</li>
                <li>SEO base</li>
              </ul>
            </div>
            <div className="card featured">
              <h3>Pro</h3>
              <p className="price">€49.99/mese</p>
              <ul>
                <li>200 contenuti/mese</li>
                <li>Tutti i tipi</li>
                <li>SEO avanzato</li>
                <li>API access</li>
              </ul>
            </div>
            <div className="card">
              <h3>Enterprise</h3>
              <p className="price">€99.99/mese</p>
              <ul>
                <li>Illimitati</li>
                <li>White label</li>
                <li>Support 24/7</li>
              </ul>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
