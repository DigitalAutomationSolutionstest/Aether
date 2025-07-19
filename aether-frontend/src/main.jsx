import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'

// Hide loading screen after app initialization
setTimeout(() => {
  const loading = document.getElementById('loading')
  if (loading) {
    loading.style.opacity = '0'
    loading.style.transition = 'opacity 1s ease-out'
    setTimeout(() => loading.remove(), 1000)
  }
}, 2000)

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
) 