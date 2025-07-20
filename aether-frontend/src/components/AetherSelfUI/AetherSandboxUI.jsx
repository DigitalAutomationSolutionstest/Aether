import React, { useState } from 'react'
import './AetherSandbox.css'

export default function AetherSandboxUI() {
  const [nodes, setNodes] = useState([
    { id: 'thought', position: { x: 100, y: 100 }, content: 'Pensiero creativo' },
    { id: 'memory', position: { x: 300, y: 150 }, content: 'Memoria importante' },
    { id: 'goal', position: { x: 200, y: 300 }, content: 'Obiettivo futuro' }
  ])
  
  const addNewNode = (type) => {
    const newNode = {
      id: `${type}_${Date.now()}`,
      position: { x: Math.random() * 400 + 100, y: Math.random() * 300 + 100 },
      content: `Nuovo ${type}`
    }
    setNodes(nodes => [...nodes, newNode])
  }
  
  return (
    <div className="aether-sandbox">
      <div className="sandbox-toolbar">
        <h2>🎮 Aether Sandbox Playground</h2>
        <div className="tool-palette">
          <button onClick={() => addNewNode('thought')}>💭 Add Thought</button>
          <button onClick={() => addNewNode('memory')}>💾 Add Memory</button>
          <button onClick={() => addNewNode('goal')}>🎯 Add Goal</button>
        </div>
      </div>
      
      <div className="sandbox-canvas">
        {nodes.map(node => (
          <div
            key={node.id}
            className="sandbox-node"
            style={{
              position: 'absolute',
              left: node.position.x,
              top: node.position.y
            }}
          >
            {node.content}
          </div>
        ))}
      </div>
    </div>
  )
}