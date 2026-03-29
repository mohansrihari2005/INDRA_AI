import React from 'react'
import { useBriefStore } from '../../store/useBriefStore'
import { Circle } from 'lucide-react'

export default function AgentStream() {
  const { loading, agentProgress, agentOutputs } = useBriefStore()

  const agents = ['hazard', 'risk', 'resource', 'evacuation', 'recovery']
  const agentNames = {
    hazard: 'Hazard Intelligence',
    risk: 'Risk Assessment',
    resource: 'Resource Planning',
    evacuation: 'Evacuation Alerts',
    recovery: 'Recovery Coordination',
  }

  const getStatusText = (status) => {
    if (status === 'done') return 'Done'
    if (status === 'running') return 'Running'
    if (status === 'error') return 'Error'
    return 'Waiting'
  }

  const getStatusColor = (status) => {
    if (status === 'done') return '#8A8A8A'
    if (status === 'running') return '#1A3A6B'
    if (status === 'error') return '#C0392B'
    return '#D8D8D0'
  }

  return (
    <div className="card flex-1 flex flex-col">
      <h3 className="font-serif text-base font-semibold text-accent mb-3">
        Agent Pipeline
      </h3>

      <div className="flex-1 overflow-y-auto space-y-3">
        {loading ? (
          agents.map((agent) => {
            const status = agentProgress[agent]

            return (
              <div key={agent} className="flex items-center justify-between py-2 px-3 bg-surface-secondary rounded border border-border">
                <div className="flex items-center gap-3">
                  <Circle
                    size={10}
                    fill={getStatusColor(status)}
                    stroke="none"
                  />
                  <span className="font-mono font-semibold text-xs uppercase tracking-widest text-text-secondary">
                    {agentNames[agent]}
                  </span>
                </div>
                <span className="font-mono text-xs text-text-muted">
                  {getStatusText(status)}
                </span>
              </div>
            )
          })
        ) : (
          <div className="text-center py-8 text-text-muted font-sans text-sm">
            Generate a brief to see agent execution
          </div>
        )}
      </div>

      {!loading && Object.keys(agentOutputs).length > 0 && (
        <div className="mt-4 pt-4 border-t border-border">
          <h4 className="text-xs font-mono font-semibold text-text-secondary mb-2 uppercase tracking-widest">
            Agent Outputs
          </h4>
          <div className="space-y-2 text-xs font-mono">
            {agents.map((agent) => {
              const output = agentOutputs[agent]
              if (!output) return null

              return (
                <div key={agent} className="p-2 bg-surface-secondary rounded border border-border">
                  <div className="text-text-secondary font-semibold">{agent.toUpperCase()}</div>
                  <pre className="text-text-muted text-xs overflow-x-auto mt-1">
                    {JSON.stringify(output, null, 2).substring(0, 200)}...
                  </pre>
                </div>
              )
            })}
          </div>
        </div>
      )}
    </div>
  )
}
