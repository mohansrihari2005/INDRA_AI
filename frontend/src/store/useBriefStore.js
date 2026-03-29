import { create } from 'zustand'

export const useBriefStore = create((set) => ({
  brief: null,
  loading: false,
  error: null,
  agentProgress: {
    hazard: 'pending',
    risk: 'pending',
    resource: 'pending',
    evacuation: 'pending',
    recovery: 'pending',
  },
  agentOutputs: {},

  setBrief: (brief) => set({ brief }),
  setLoading: (loading) => set({ loading }),
  setError: (error) => set({ error }),

  updateAgentProgress: (agent, status) =>
    set((state) => ({
      agentProgress: { ...state.agentProgress, [agent]: status },
    })),

  setAgentOutput: (agent, output) =>
    set((state) => ({
      agentOutputs: { ...state.agentOutputs, [agent]: output },
    })),

  resetBrief: () =>
    set({
      brief: null,
      loading: false,
      error: null,
      agentProgress: {
        hazard: 'pending',
        risk: 'pending',
        resource: 'pending',
        evacuation: 'pending',
        recovery: 'pending',
      },
      agentOutputs: {},
    }),
}))
