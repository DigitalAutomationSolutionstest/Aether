import React from 'react'

// Error Boundary Component con stile cyber
export class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props)
    this.state = { hasError: false, error: null, errorInfo: null }
  }

  static getDerivedStateFromError(error) {
    // Aggiorna lo stato per mostrare la UI di errore
    return { hasError: true }
  }

  componentDidCatch(error, errorInfo) {
    // Salva i dettagli dell'errore
    this.setState({
      error: error,
      errorInfo: errorInfo
    })
    
    // Log dell'errore per debugging
    console.error('🚨 Aether Error Boundary caught an error:', error, errorInfo)
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback ? (
        this.props.fallback(this.state.error, () => {
          this.setState({ hasError: false, error: null, errorInfo: null })
        })
      ) : (
        <AetherErrorFallback 
          error={this.state.error}
          resetError={() => {
            this.setState({ hasError: false, error: null, errorInfo: null })
          }}
        />
      )
    }

    return this.props.children
  }
}

// Componente di fallback con stile cyber per gli errori
export function AetherErrorFallback({ error, resetError }) {
  return (
    <div className="min-h-screen bg-black flex items-center justify-center p-4">
      <div className="cyber-panel p-8 max-w-md w-full text-center">
        {/* Icona di errore animata */}
        <div className="mb-6">
          <div className="w-16 h-16 mx-auto border-2 border-aether-accent rounded-full flex items-center justify-center animate-pulse">
            <span className="text-2xl">⚠️</span>
          </div>
        </div>
        
        {/* Titolo errore */}
        <h2 className="text-2xl font-cyber mb-4 text-aether-accent animate-glow">
          SYSTEM MALFUNCTION
        </h2>
        
        {/* Messaggio errore */}
        <div className="mb-6">
          <p className="text-aether-primary/70 mb-2">
            Aether's neural matrix has encountered an anomaly.
          </p>
          
          {error && (
            <details className="mt-4 text-left">
              <summary className="cursor-pointer text-aether-secondary hover:text-aether-primary text-sm">
                Technical Details
              </summary>
              <pre className="mt-2 p-3 bg-black/50 rounded text-xs text-aether-primary/60 overflow-auto max-h-32 font-code">
                {error.toString()}
              </pre>
            </details>
          )}
        </div>
        
        {/* Azioni */}
        <div className="space-y-3">
          <button 
            onClick={resetError}
            className="cyber-button w-full py-3"
          >
            RESTART NEURAL MATRIX
          </button>
          
          <button 
            onClick={() => window.location.reload()}
            className="cyber-button w-full py-3 border-aether-secondary text-aether-secondary hover:bg-aether-secondary"
          >
            FULL SYSTEM REBOOT
          </button>
        </div>
        
        {/* Footer */}
        <div className="mt-6 text-xs text-aether-primary/40">
          Error ID: {Date.now().toString(36).toUpperCase()}
        </div>
      </div>
    </div>
  )
}

// Hook per error handling avanzato
export function useErrorHandler() {
  const [error, setError] = React.useState(null)
  
  const throwError = React.useCallback((error) => {
    setError(() => {
      throw error
    })
  }, [])
  
  const clearError = React.useCallback(() => {
    setError(null)
  }, [])
  
  return { throwError, clearError }
}

// Wrapper HOC per componenti che potrebbero fallire
export function withErrorBoundary(Component, fallback) {
  return function WrappedComponent(props) {
    return (
      <ErrorBoundary fallback={fallback}>
        <Component {...props} />
      </ErrorBoundary>
    )
  }
} 