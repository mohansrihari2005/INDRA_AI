import React from 'react'
import { Volume2 } from 'lucide-react'

export default function VoicePanel({ brief }) {
  const evacuation = brief?.evacuation || {}

  if (!brief || !evacuation.english_sms) {
    return (
      <div className="card">
        <h3 className="font-serif text-base font-semibold text-accent mb-3">
          Voice Broadcast
        </h3>
        <p className="text-text-muted text-sm font-sans">
          Generate a brief to enable voice alert generation
        </p>
      </div>
    )
  }

  return (
    <div className="card">
      <h3 className="font-serif text-base font-semibold text-accent mb-4 flex items-center gap-2">
        <Volume2 size={18} className="text-accent" strokeWidth={1.5} />
        Voice Broadcast Status
      </h3>

      <div className="space-y-3">
        <div className="p-3 bg-surface-secondary border border-border rounded">
          <div className="text-xs font-mono font-semibold text-text-secondary mb-2 uppercase tracking-widest">
            SMS Alert (English)
          </div>
          <p className="text-xs font-sans text-text-primary leading-relaxed">
            {evacuation.english_sms}
          </p>
          <div className="mt-2 text-xs font-mono text-text-muted">
            Length: {evacuation.english_sms.length} characters
          </div>
        </div>

        <div className="p-3 bg-surface-secondary border border-border rounded">
          <div className="text-xs font-mono font-semibold text-text-secondary mb-2 uppercase tracking-widest">
            Broadcast Languages
          </div>
          <div className="grid grid-cols-2 gap-2 text-xs font-sans">
            <div className="flex items-center gap-1">
              <span className="w-2 h-2 bg-accent rounded-full"></span>
              <span>English (SMS)</span>
            </div>
            <div className="flex items-center gap-1">
              <span className="w-2 h-2 bg-accent rounded-full"></span>
              <span>Hindi (Devanagari)</span>
            </div>
            <div className="flex items-center gap-1">
              <span className="w-2 h-2 bg-accent rounded-full"></span>
              <span>Telugu (Script)</span>
            </div>
            {brief.state === 'Odisha' && (
              <div className="flex items-center gap-1">
                <span className="w-2 h-2 bg-accent rounded-full"></span>
                <span>Odia (Script)</span>
              </div>
            )}
            {['Tamil Nadu', 'Puducherry'].includes(brief.state) && (
              <div className="flex items-center gap-1">
                <span className="w-2 h-2 bg-accent rounded-full"></span>
                <span>Tamil (Script)</span>
              </div>
            )}
          </div>
        </div>

        <div className="p-3 bg-surface-secondary border border-border rounded">
          <div className="text-xs font-mono font-semibold text-text-secondary mb-2 uppercase tracking-widest">
            Distribution Channels
          </div>
          <div className="space-y-1 text-xs font-sans text-text-muted">
            <div>✓ SMS Gateway (160 chars)</div>
            <div>✓ TV Broadcast (Full Advisory)</div>
            <div>✓ Radio Loudspeakers (Regional)</div>
            <div>✓ Mobile Alerts (Push Notifications)</div>
          </div>
        </div>
      </div>
    </div>
  )
}
