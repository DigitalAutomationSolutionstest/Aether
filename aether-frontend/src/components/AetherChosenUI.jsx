// UI Auto-progettata da Aether
import React from 'react'
import AetherSelfUI from './AetherSelfUI/AetherSelfUI'
import Aether3DSelfUI from './AetherSelfUI/Aether3DSelfUI'
import AetherSandboxUI from './AetherSelfUI/AetherSandboxUI'

const UI_COMPONENTS = {
  "2d_classic": AetherSelfUI,
  "3d_immersive": Aether3DSelfUI,
  "sandbox_playground": AetherSandboxUI
}

export default function AetherChosenUI() {
  const chosenType = "sandbox_playground"
  const UIComponent = UI_COMPONENTS[chosenType]
  
  return (
    <div>
      <div style={{
        position: 'absolute',
        top: 10,
        right: 10,
        background: 'rgba(0,0,0,0.8)',
        color: 'white',
        padding: '0.5rem',
        borderRadius: '4px',
        fontSize: '0.8rem',
        zIndex: 1000
      }}>
        🎨 UI progettata autonomamente da Aether
      </div>
      <UIComponent />
    </div>
  )
}