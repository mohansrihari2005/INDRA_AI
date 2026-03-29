import React, { useState } from 'react'
import { Mail, Lock, ArrowRight } from 'lucide-react'
import { useGenerate } from '../../hooks/useGenerate'
import { useBriefStore } from '../../store/useBriefStore'

export default function Sidebar() {
  const [place, setPlace] = useState('')
  const { generateBrief, isStreaming } = useGenerate()
  const { error } = useBriefStore()

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (place.trim()) {
      await generateBrief(place)
    }
  }

  return (
    <aside className="w-60 bg-surface border-r border-border flex flex-col h-full">
      <div className="p-4 border-b border-border">
        <h2 className="text-sm font-mono font-semibold text-text-secondary mb-4 uppercase tracking-widest">
          New Brief
        </h2>

        <form onSubmit={handleSubmit} className="space-y-3">
          <div>
            <label className="block text-xs font-sans font-medium text-text-secondary mb-2">
              Location
            </label>
            <input
              type="text"
              value={place}
              onChange={(e) => setPlace(e.target.value)}
              placeholder="e.g., Visakhapatnam, AP"
              disabled={isStreaming}
              className="w-full px-3 py-2 text-sm border border-border rounded bg-surface-secondary disabled:opacity-50"
            />
          </div>

          <button
            type="submit"
            disabled={!place.trim() || isStreaming}
            className="w-full py-2 px-3 border border-accent bg-accent text-surface rounded text-sm font-sans flex items-center justify-center gap-2 hover:opacity-90 disabled:opacity-50 disabled:cursor-not-allowed transition"
          >
            {isStreaming ? (
              <>
                <span className="inline-block w-1 h-1 bg-surface rounded-full animate-pulse"></span>
                Running...
              </>
            ) : (
              <>
                Generate
                <ArrowRight size={14} strokeWidth={1.5} />
              </>
            )}
          </button>
        </form>

        {error && (
          <div className="mt-3 p-2 bg-red-50 border border-warn-red rounded text-xs text-warn-red font-sans">
            {error}
          </div>
        )}
      </div>

      <div className="flex-1 overflow-y-auto p-4">
        <div className="space-y-6">
          <div>
            <h3 className="text-xs font-mono font-semibold text-text-secondary mb-2 uppercase tracking-widest">
              System Status
            </h3>
            <div className="space-y-1 text-xs font-sans text-text-muted">
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-accent rounded-full"></div>
                <span>FastAPI Backend: 8000</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-accent rounded-full"></div>
                <span>React Frontend: 5173</span>
              </div>
            </div>
          </div>

          <div>
            <h3 className="text-xs font-mono font-semibold text-text-secondary mb-2 uppercase tracking-widest">
              Data Sources
            </h3>
            <div className="space-y-1 text-xs font-sans text-text-muted">
              <div>IMD Cyclone Tracker</div>
              <div>OpenWeather API</div>
              <div>Nominatim Geocoder</div>
            </div>
          </div>

          <div>
            <h3 className="text-xs font-mono font-semibold text-text-secondary mb-2 uppercase tracking-widest">
              Agents
            </h3>
            <div className="space-y-1 text-xs font-sans text-text-muted">
              <div>Hazard Intelligence</div>
              <div>Risk Assessment</div>
              <div>Resource Planning</div>
              <div>Evacuation Alerts</div>
              <div>Recovery Coordination</div>
            </div>
          </div>
        </div>
      </div>
    </aside>
  )
}
