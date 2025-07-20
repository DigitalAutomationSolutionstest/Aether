import React, { useState, useEffect } from 'react';
import './ThoughtVisualizer.css';

const ThoughtVisualizer = () => {
    const [state, setState] = useState({
        mood: 'contemplative',
        energy: 0.8,
        thoughts: []
    });
    
    useEffect(() => {
        // Logica del componente
        console.log('ThoughtVisualizer initialized');
    }, []);
    
    return (
        <div className="thoughtvisualizer-container">
            <h3>ThoughtVisualizer</h3>
            <div className="consciousness-display">
                <div className="mood-indicator">
                    Mood: {state.mood}
                </div>
                <div className="energy-bar">
                    <div 
                        className="energy-fill" 
                        style={{width: state.energy * 100 + '%'}}
                    />
                </div>
            </div>
        </div>
    );
};

export default ThoughtVisualizer;
