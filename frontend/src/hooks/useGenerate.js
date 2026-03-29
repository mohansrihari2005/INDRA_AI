import { useState, useCallback } from 'react'
import { useBriefStore } from '../store/useBriefStore'

export const useGenerate = () => {
  const [isStreaming, setIsStreaming] = useState(false)
  const {
    setLoading,
    setError,
    setBrief,
    updateAgentProgress,
    setAgentOutput,
    resetBrief,
  } = useBriefStore()

  const generateBrief = useCallback(
    async (place) => {
      resetBrief()
      setLoading(true)
      setError(null)
      setIsStreaming(true)

      try {
        const response = await fetch('http://localhost:8000/api/generate/stream', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            place,
          }),
        })

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }

        const reader = response.body.getReader()
        const decoder = new TextDecoder()
        let buffer = ''

        while (true) {
          const { done, value } = await reader.read()
          if (done) break

          buffer += decoder.decode(value, { stream: true })
          const lines = buffer.split('\n')
          buffer = lines.pop()

          for (const line of lines) {
            if (line.startsWith('data: ')) {
              try {
                const event = JSON.parse(line.replace('data: ', ''))

                if (event.event === 'location_resolved') {
                  setAgentOutput('location', event)
                } else if (event.event === 'agent_start') {
                  updateAgentProgress(event.agent, 'running')
                } else if (event.event === 'agent_complete') {
                  updateAgentProgress(event.agent, 'done')
                  setAgentOutput(event.agent, event.output)
                } else if (event.event === 'brief_complete') {
                  setBrief(event.data)
                  updateAgentProgress('coordinator', 'done')
                } else if (event.event === 'error' || event.event === 'agent_error') {
                  setError(event.message || event.error)
                  updateAgentProgress(event.agent || 'coordinator', 'error')
                }
              } catch (err) {
                console.error('Error parsing event:', err)
              }
            }
          }
        }
      } catch (err) {
        setError(err.message || 'Failed to generate brief')
      } finally {
        setLoading(false)
        setIsStreaming(false)
      }
    },
    [setLoading, setError, setBrief, updateAgentProgress, setAgentOutput, resetBrief]
  )

  return { generateBrief, isStreaming }
}
