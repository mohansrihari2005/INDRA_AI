import React from 'react'
import { AlertTriangle, Wind, Droplets, MapPin } from 'lucide-react'

export default function SummaryStrip({ brief }) {
  if (!brief) {
    return (
      <div className="bg-surface border-b border-border p-4 text-text-muted text-sm font-sans">
        Generate a brief to view summary
      </div>
    )
  }

  const hazard = brief.hazard || {}
  const risk = brief.risk || {}
  const warningColor = hazard.warning_color || 'GREEN'

  const colorMap = {
    RED: { bg: '#FDF2F2', border: '#E8C0BC', text: '#C0392B' },
    ORANGE: { bg: '#FDF8F3', border: '#F4D5B9', text: '#D35400' },
    YELLOW: { bg: '#FFFEF3', border: '#EFE5B9', text: '#B7950B' },
    GREEN: { bg: '#F1F8F1', border: '#C8E6C9', text: '#1A5A1A' },
  }

  const colors = colorMap[warningColor] || colorMap.GREEN

  return (
    <div
      className="border-b border-border p-4"
      style={{ backgroundColor: colors.bg, borderColor: colors.border }}
    >
      <div className="grid grid-cols-4 gap-4 text-sm font-sans">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <AlertTriangle size={16} strokeWidth={1.5} style={{ color: colors.text }} />
            <span className="font-mono font-semibold uppercase tracking-widest" style={{ color: colors.text, fontSize: '11px' }}>
              Warning
            </span>
          </div>
          <div className="font-mono font-semibold text-base" style={{ color: colors.text }}>
            {warningColor}
          </div>
        </div>

        <div>
          <div className="flex items-center gap-2 mb-1">
            <Wind size={16} strokeWidth={1.5} style={{ color: colors.text }} />
            <span className="font-mono font-semibold uppercase tracking-widest" style={{ color: colors.text, fontSize: '11px' }}>
              Wind
            </span>
          </div>
          <div className="font-mono font-semibold text-base" style={{ color: colors.text }}>
            {hazard.wind_speed_kmh || 0} km/h
          </div>
        </div>

        <div>
          <div className="flex items-center gap-2 mb-1">
            <Droplets size={16} strokeWidth={1.5} style={{ color: colors.text }} />
            <span className="font-mono font-semibold uppercase tracking-widest" style={{ color: colors.text, fontSize: '11px' }}>
              Risk
            </span>
          </div>
          <div className="font-mono font-semibold text-base" style={{ color: colors.text }}>
            {risk.indra_risk_score || 0}/100
          </div>
        </div>

        <div>
          <div className="flex items-center gap-2 mb-1">
            <MapPin size={16} strokeWidth={1.5} style={{ color: colors.text }} />
            <span className="font-mono font-semibold uppercase tracking-widest" style={{ color: colors.text, fontSize: '11px' }}>
              Location
            </span>
          </div>
          <div className="font-mono font-semibold text-base" style={{ color: colors.text }}>
            {brief.district || 'N/A'}
          </div>
        </div>
      </div>

      <div className="mt-4 pt-4 border-t" style={{ borderColor: colors.border }}>
        <p className="font-sans text-xs" style={{ color: colors.text }}>
          {brief.executive_summary || 'Generating summary...'}
        </p>
      </div>
    </div>
  )
}
