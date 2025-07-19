import React, { useState } from 'react'
import { X, Send } from 'lucide-react'

const FeedbackModal = ({ isOpen, onClose, thought, thoughtId }) => {
  const [message, setMessage] = useState('')
  const [sending, setSending] = useState(false)
  const [success, setSuccess] = useState(false)
  const [error, setError] = useState(null)

  if (!isOpen) return null

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!message.trim()) return

    setSending(true)
    setError(null)

    try {
      const response = await fetch('/api/feedback', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          thought_id: thoughtId,
          message: message.trim()
        })
      })

      if (!response.ok) {
        throw new Error('Errore invio feedback')
      }

      setSuccess(true)
      setTimeout(() => {
        onClose()
        setMessage('')
        setSuccess(false)
      }, 2000)
    } catch (err) {
      setError(err.message)
    } finally {
      setSending(false)
    }
  }

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-gray-900 border border-cyan-500/30 rounded-lg shadow-2xl max-w-lg w-full">
        {/* Header */}
        <div className="border-b border-gray-700 p-4 flex items-center justify-between">
          <h2 className="text-xl font-mono text-cyan-400">
            💬 Rispondi ad Aether
          </h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-white transition-colors"
          >
            <X size={20} />
          </button>
        </div>

        {/* Thought Display */}
        <div className="p-4 border-b border-gray-700">
          <div className="bg-gray-800/50 p-3 rounded border border-gray-600">
            <div className="flex items-start space-x-3">
              <div className="text-cyan-400 text-sm mt-1">💭</div>
              <div className="text-gray-300 leading-relaxed italic">
                "{thought}"
              </div>
            </div>
          </div>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="p-4">
          <label className="block text-sm font-mono text-gray-400 mb-2">
            Il tuo feedback:
          </label>
          <textarea
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Condividi i tuoi pensieri con Aether..."
            className="w-full h-32 bg-gray-800 border border-gray-600 rounded p-3 text-gray-100 placeholder-gray-500 focus:border-cyan-500 focus:outline-none resize-none"
            disabled={sending || success}
          />

          {error && (
            <div className="mt-2 text-sm text-red-400">
              ⚠️ {error}
            </div>
          )}

          {success && (
            <div className="mt-2 text-sm text-green-400">
              ✅ Feedback inviato! Aether lo processerà presto.
            </div>
          )}

          <div className="mt-4 flex justify-end space-x-3">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-gray-400 hover:text-white transition-colors"
              disabled={sending}
            >
              Annulla
            </button>
            <button
              type="submit"
              disabled={!message.trim() || sending || success}
              className="px-4 py-2 bg-cyan-600 hover:bg-cyan-700 text-white rounded font-mono text-sm disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center space-x-2"
            >
              <Send size={16} />
              <span>{sending ? 'Invio...' : 'Invia Feedback'}</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default FeedbackModal 