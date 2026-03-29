import React, { useEffect } from 'react'
import { Toaster } from 'react-hot-toast'
import Header from './components/layout/Header'
import Sidebar from './components/layout/Sidebar'
import SummaryStrip from './components/dashboard/SummaryStrip'
import MapPanel from './components/dashboard/MapPanel'
import AgentStream from './components/dashboard/AgentStream'
import RolePlans from './components/dashboard/RolePlans'
import AlertPanel from './components/dashboard/AlertPanel'
import VoicePanel from './components/dashboard/VoicePanel'
import RecoveryPlan from './components/dashboard/RecoveryPlan'
import { useBriefStore } from './store/useBriefStore'
import { healthCheck } from './api/client'

export default function App() {
  const brief = useBriefStore((state) => state.brief)

  useEffect(() => {
    healthCheck().catch(err => {
      console.error('Backend health check failed:', err)
    })
  }, [])

  return (
    <div className="flex h-screen bg-page">
      <Sidebar />

      <div className="flex-1 flex flex-col overflow-hidden">
        <Header />

        <div className="flex-1 overflow-y-auto">
          <SummaryStrip brief={brief} />

          <div className="p-4 space-y-4">
            {/* Top row: Map and Agent Stream */}
            <div className="grid grid-cols-3 gap-4">
              <div className="col-span-2">
                <MapPanel brief={brief} />
              </div>
              <div>
                <AgentStream />
              </div>
            </div>

            {/* Second row: Role Plans and Alerts */}
            <div className="grid grid-cols-2 gap-4">
              <div>
                <RolePlans brief={brief} />
              </div>
              <div>
                <AlertPanel brief={brief} />
              </div>
            </div>

            {/* Third row: Voice and Recovery */}
            <div className="grid grid-cols-2 gap-4">
              <div>
                <VoicePanel brief={brief} />
              </div>
              <div>
                <RecoveryPlan brief={brief} />
              </div>
            </div>
          </div>
        </div>
      </div>

      <Toaster position="bottom-right" />
    </div>
  )
}
