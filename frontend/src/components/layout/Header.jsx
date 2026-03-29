import React from 'react'
import { Info } from 'lucide-react'

export default function Header() {
  return (
    <header className="border-b border-border">
      <div className="tricolor"></div>
      <div className="bg-surface px-6 py-4">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-xl font-serif text-accent mb-1">INDRA AI v2</h1>
            <p className="text-sm text-text-muted font-sans">
              Intelligent National Disaster Response Agents
            </p>
          </div>
          <div className="flex items-center gap-2 text-text-muted">
            <Info size={16} strokeWidth={1.5} />
            <span className="text-xs font-sans">Production System</span>
          </div>
        </div>
      </div>
    </header>
  )
}
