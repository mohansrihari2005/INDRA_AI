import React, { useState } from 'react'
import { ChevronDown, ChevronUp } from 'lucide-react'

const ROLES = {
  police: 'Police Department',
  revenue: 'Revenue/District Admin',
  health: 'Health Department',
  panchayat: 'Panchayati Raj',
  ngos: 'NGOs & Community',
  fishermen: 'Fishermen Community',
}

export default function RolePlans({ brief }) {
  const [expandedRole, setExpandedRole] = useState('police')
  const evacuation = brief?.evacuation || {}
  const rolePlans = evacuation.role_plans || {}

  if (!brief || !Object.keys(rolePlans).length) {
    return (
      <div className="card">
        <h3 className="font-serif text-base font-semibold text-accent mb-3">
          Role-Based Action Checklists
        </h3>
        <p className="text-text-muted text-sm font-sans">
          Generate a brief to view role-specific action items
        </p>
      </div>
    )
  }

  return (
    <div className="card">
      <h3 className="font-serif text-base font-semibold text-accent mb-3">
        Role-Based Action Checklists
      </h3>

      <div className="space-y-2">
        {Object.entries(ROLES).map(([roleKey, roleName]) => {
          const isExpanded = expandedRole === roleKey
          const items = rolePlans[roleKey] || []

          return (
            <div key={roleKey} className="border border-border rounded overflow-hidden">
              <button
                onClick={() =>
                  setExpandedRole(isExpanded ? null : roleKey)
                }
                className="w-full px-3 py-2 flex items-center justify-between bg-surface-secondary hover:bg-page transition"
              >
                <span className="font-mono font-semibold text-xs uppercase tracking-widest text-text-secondary">
                  {roleName}
                </span>
                {isExpanded ? (
                  <ChevronUp size={16} className="text-text-muted" strokeWidth={1.5} />
                ) : (
                  <ChevronDown size={16} className="text-text-muted" strokeWidth={1.5} />
                )}
              </button>

              {isExpanded && (
                <div className="p-3 space-y-2 border-t border-border">
                  {items.map((item, idx) => (
                    <div key={idx} className="flex gap-3">
                      <div className="text-xs font-mono font-semibold text-text-secondary min-w-fit mt-0.5">
                        {idx + 1}.
                      </div>
                      <p className="text-xs font-sans text-text-primary leading-relaxed">
                        {item}
                      </p>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )
        })}
      </div>

      {evacuation.do_not_list && evacuation.do_not_list.length > 0 && (
        <div className="mt-4 pt-4 border-t border-border">
          <h4 className="text-xs font-mono font-semibold text-warn-red mb-2 uppercase tracking-widest">
            Critical DO NOTs
          </h4>
          <div className="space-y-1">
            {evacuation.do_not_list.map((item, idx) => (
              <div key={idx} className="text-xs font-sans text-warn-red">
                • {item}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
