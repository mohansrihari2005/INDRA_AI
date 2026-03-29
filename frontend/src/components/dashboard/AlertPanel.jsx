import React, { useState } from 'react'
import { Copy, Check } from 'lucide-react'
import { generateVoice } from '../../api/client'

export default function AlertPanel({ brief }) {
  const [copiedAlert, setCopiedAlert] = useState(null)
  const [loadingAudio, setLoadingAudio] = useState(null)
  const evacuation = brief?.evacuation || {}

  const languages = [
    { code: 'en', name: 'English', text: evacuation.english_sms },
    { code: 'hi', name: 'हिंदी', text: evacuation.hindi },
    { code: 'te', name: 'తెలుగు', text: evacuation.telugu },
    { code: 'or', name: 'ଓଡିଆ', text: evacuation.odia },
    { code: 'ta', name: 'தமிழ்', text: evacuation.tamil },
  ]

  const handleCopy = (text, alertId) => {
    if (!text) return
    navigator.clipboard.writeText(text)
    setCopiedAlert(alertId)
    setTimeout(() => setCopiedAlert(null), 1500)
  }

  const handleGenerateAudio = async (text, lang) => {
    if (!text) return
    setLoadingAudio(lang)
    try {
      const response = await generateVoice(text, lang)
      const audioUrl = `data:audio/mpeg;base64,${response.data.audio_base64}`
      const audio = new Audio(audioUrl)
      audio.play()
    } catch (err) {
      console.error('Failed to generate audio:', err)
    } finally {
      setLoadingAudio(null)
    }
  }

  if (!brief || !evacuation.english_sms) {
    return (
      <div className="card">
        <h3 className="font-serif text-base font-semibold text-accent mb-3">
          Multilingual Alerts
        </h3>
        <p className="text-text-muted text-sm font-sans">
          Generate a brief to view alerts in multiple languages
        </p>
      </div>
    )
  }

  return (
    <div className="card">
      <h3 className="font-serif text-base font-semibold text-accent mb-4">
        Multilingual Alerts
      </h3>

      <div className="space-y-3">
        {languages.map(({ code, name, text }) => {
          if (!text) return null

          const alertId = `alert-${code}`
          const isCopied = copiedAlert === alertId

          return (
            <div
              key={code}
              className="border-l-2 border-accent bg-surface-secondary p-3 rounded"
            >
              <div className="flex items-center justify-between mb-2">
                <span className="font-mono text-xs font-semibold text-text-secondary uppercase tracking-widest">
                  {name}
                </span>
                <div className="flex gap-1">
                  <button
                    onClick={() => handleCopy(text, alertId)}
                    className="p-1 hover:bg-surface rounded transition"
                    title="Copy alert"
                  >
                    {isCopied ? (
                      <Check size={14} className="text-text-secondary" strokeWidth={2} />
                    ) : (
                      <Copy size={14} className="text-text-muted" strokeWidth={1.5} />
                    )}
                  </button>
                  <button
                    onClick={() => handleGenerateAudio(text, code)}
                    disabled={loadingAudio === code}
                    className="px-2 py-1 text-xs border border-border rounded hover:bg-surface transition disabled:opacity-50"
                    title="Play audio"
                  >
                    {loadingAudio === code ? '...' : '🔊'}
                  </button>
                </div>
              </div>
              <p className="font-sans text-xs leading-relaxed text-text-primary break-words">
                {text}
              </p>
            </div>
          )
        })}
      </div>

      {evacuation.english_full && (
        <div className="mt-4 pt-4 border-t border-border">
          <h4 className="text-xs font-mono font-semibold text-text-secondary mb-2 uppercase tracking-widest">
            Full Advisory
          </h4>
          <p className="text-xs font-sans text-text-primary leading-relaxed">
            {evacuation.english_full}
          </p>
        </div>
      )}
    </div>
  )
}
