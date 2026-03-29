import React, { useEffect } from 'react'
import { MapContainer, TileLayer, Marker, Popup, CircleMarker } from 'react-leaflet'
import L from 'leaflet'

const DEFAULT_CENTER = [20.5937, 78.9629]
const IMPACT_RADIUS_KM = 100

export default function MapPanel({ brief }) {
  const hazard = brief?.hazard || {}
  const risk = brief?.risk || {}

  const center = brief?.lat && brief?.lon
    ? [brief.lat, brief.lon]
    : DEFAULT_CENTER

  const warningColor = hazard.warning_color || 'GREEN'
  const colorMap = {
    RED: '#C0392B',
    ORANGE: '#D35400',
    YELLOW: '#B7950B',
    GREEN: '#1A5A1A',
  }
  const ringColor = colorMap[warningColor] || '#1A5A1A'

  return (
    <div className="card h-96 relative">
      <h3 className="font-serif text-base font-semibold text-accent mb-3">
        Impact Assessment Map
      </h3>

      {brief ? (
        <MapContainer
          center={center}
          zoom={8}
          style={{ height: '320px', borderRadius: '4px' }}
          className="border border-border"
        >
          <TileLayer
            url="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png"
            attribution='&copy; OpenStreetMap contributors &copy; CartoDB'
          />

          {brief.lat && brief.lon && (
            <>
              <Marker position={[brief.lat, brief.lon]}>
                <Popup>
                  <div className="font-sans text-xs">
                    <div className="font-semibold">{brief.district}</div>
                    <div className="text-text-muted">{brief.state}</div>
                  </div>
                </Popup>
              </Marker>

              <CircleMarker
                center={[brief.lat, brief.lon]}
                radius={IMPACT_RADIUS_KM / 10}
                pathOptions={{
                  color: ringColor,
                  weight: 2,
                  opacity: 0.6,
                  fill: false,
                }}
              />
            </>
          )}
        </MapContainer>
      ) : (
        <div className="h-80 bg-surface-secondary border border-border rounded flex items-center justify-center">
          <p className="text-text-muted text-sm font-sans">Map will display after generating brief</p>
        </div>
      )}

      {brief && risk.high_risk_areas && risk.high_risk_areas.length > 0 && (
        <div className="mt-3 pt-3 border-t border-border">
          <h4 className="text-xs font-mono font-semibold text-text-secondary mb-2 uppercase tracking-widest">
            High Risk Areas
          </h4>
          <div className="space-y-1">
            {risk.high_risk_areas.map((area, idx) => (
              <div key={idx} className="text-xs font-sans text-text-muted">
                <div className="font-semibold text-text-primary">{area.name}</div>
                <div className="text-text-muted">{area.reason}</div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
