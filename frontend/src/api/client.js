import axios from 'axios'

const API_BASE = 'http://localhost:8000'

export const apiClient = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const healthCheck = async () => {
  return apiClient.get('/api/health')
}

export const generateBrief = async (place, openaiApiKey) => {
  return apiClient.post('/api/generate/stream', {
    place,
    openai_api_key: openaiApiKey,
  })
}

export const getIMDLive = async () => {
  return apiClient.get('/api/imd/live')
}

export const getWeather = async (place) => {
  return apiClient.get('/api/weather', { params: { place } })
}

export const resolvePlace = async (q) => {
  return apiClient.get('/api/place/resolve', { params: { q } })
}

export const generateVoice = async (text, lang) => {
  return apiClient.post('/api/voice', { text, lang })
}

export const generatePDF = async (brief) => {
  return apiClient.post('/api/pdf', { brief }, {
    responseType: 'blob',
  })
}
