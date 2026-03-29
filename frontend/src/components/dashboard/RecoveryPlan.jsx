import React, { useState } from 'react'
import { ChevronDown, ChevronUp } from 'lucide-react'

export default function RecoveryPlan({ brief }) {
  const [expandedDay, setExpandedDay] = useState(0)
  const recovery = brief?.recovery || {}
  const days = recovery.days || []
  const compensation = recovery.ndrf_compensation || {}

  if (!brief || !days.length) {
    return (
      <div className="card">
        <h3 className="font-serif text-base font-semibold text-accent mb-3">
          7-Day Recovery Timeline
        </h3>
        <p className="text-text-muted text-sm font-sans">
          Generate a brief to view recovery plan
        </p>
      </div>
    )
  }

  return (
    <div className="card">
      <h3 className="font-serif text-base font-semibold text-accent mb-3">
        7-Day Recovery Timeline
      </h3>

      <div className="space-y-2 mb-4">
        {days.map((day, idx) => {
          const isExpanded = expandedDay === idx

          return (
            <div key={idx} className="border border-border rounded overflow-hidden">
              <button
                onClick={() => setExpandedDay(isExpanded ? null : idx)}
                className="w-full px-3 py-2 flex items-center justify-between bg-surface-secondary hover:bg-page transition"
              >
                <div className="flex items-center gap-3 flex-1 text-left">
                  <span className="font-mono font-semibold text-sm text-accent w-8">
                    Day {day.day_number}
                  </span>
                  <span className="font-sans font-medium text-xs text-text-secondary">
                    {day.phase_name}
                  </span>
                  <span className="text-xs text-text-muted font-mono">
                    {day.day_range}
                  </span>
                </div>
                {isExpanded ? (
                  <ChevronUp size={16} className="text-text-muted" strokeWidth={1.5} />
                ) : (
                  <ChevronDown size={16} className="text-text-muted" strokeWidth={1.5} />
                )}
              </button>

              {isExpanded && (
                <div className="p-3 space-y-3 border-t border-border bg-surface">
                  <div>
                    <h5 className="text-xs font-mono font-semibold text-text-secondary mb-2 uppercase tracking-widest">
                      Priority Tasks
                    </h5>
                    <ul className="space-y-1">
                      {day.priority_tasks.map((task, taskIdx) => (
                        <li key={taskIdx} className="text-xs font-sans text-text-primary flex gap-2">
                          <span className="text-text-muted">•</span>
                          <span>{task}</span>
                        </li>
                      ))}
                    </ul>
                  </div>

                  <div className="pt-2 border-t border-border">
                    <h5 className="text-xs font-mono font-semibold text-text-secondary mb-2 uppercase tracking-widest">
                      Collector Action
                    </h5>
                    <p className="text-xs font-sans text-text-primary leading-relaxed">
                      {day.collector_action}
                    </p>
                  </div>

                  {day.schemes_activated && day.schemes_activated.length > 0 && (
                    <div className="pt-2 border-t border-border">
                      <h5 className="text-xs font-mono font-semibold text-text-secondary mb-2 uppercase tracking-widest">
                        Schemes Activated
                      </h5>
                      <div className="space-y-1">
                        {day.schemes_activated.map((scheme, schemeIdx) => (
                          <div key={schemeIdx} className="text-xs font-sans text-text-primary flex gap-2">
                            <span className="text-accent">✓</span>
                            <span>{scheme}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          )
        })}
      </div>

      {Object.keys(compensation).length > 0 && (
        <div className="mt-4 pt-4 border-t border-border">
          <h4 className="text-xs font-mono font-semibold text-text-secondary mb-3 uppercase tracking-widest">
            NDMA Compensation Norms (2024)
          </h4>
          <div className="grid grid-cols-2 gap-2">
            {Object.entries(compensation).map(([key, value]) => (
              <div key={key} className="text-xs font-sans">
                <div className="text-text-muted capitalize">{key.replace(/_/g, ' ')}</div>
                <div className="font-mono font-semibold text-text-primary">{value}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {recovery.closing_statement && (
        <div className="mt-4 pt-4 border-t border-border">
          <p className="text-xs font-sans italic text-text-primary leading-relaxed">
            {recovery.closing_statement}
          </p>
        </div>
      )}
    </div>
  )
}
