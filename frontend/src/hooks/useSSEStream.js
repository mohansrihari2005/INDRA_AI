import { useEffect, useRef, useCallback } from 'react'

export const useSSEStream = (url, onEvent, onError) => {
  const eventSourceRef = useRef(null)

  const connect = useCallback(() => {
    if (eventSourceRef.current) {
      eventSourceRef.current.close()
    }

    eventSourceRef.current = new EventSource(url)

    eventSourceRef.current.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        onEvent(data)
      } catch (err) {
        console.error('Failed to parse SSE event:', err)
      }
    }

    eventSourceRef.current.onerror = (error) => {
      console.error('SSE connection error:', error)
      eventSourceRef.current.close()
      if (onError) onError(error)
    }
  }, [url, onEvent, onError])

  useEffect(() => {
    connect()

    return () => {
      if (eventSourceRef.current) {
        eventSourceRef.current.close()
      }
    }
  }, [connect])

  const close = useCallback(() => {
    if (eventSourceRef.current) {
      eventSourceRef.current.close()
      eventSourceRef.current = null
    }
  }, [])

  return { close }
}
