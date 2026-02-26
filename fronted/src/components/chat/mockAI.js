// src/components/chat/mockAI.js
// ─────────────────────────────────────────────────────────────────
//  Live backend connection.
//  Backend must return this shape:
//  {
//    intent:             string,
//    mode:               "calculation" | "advisory" | "general" | "onboarding",
//    data:               {},
//    message:            string,
//    missing_parameters: string[],
//    profile_data:       {},
//    advisory_insights:  [{ tag: string, text: string }]
//  }
// ─────────────────────────────────────────────────────────────────

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export async function mockRespond(userText) {
  const res = await fetch(`${API_URL}/api/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: userText }),
  })

  if (!res.ok) throw new Error(`Server error: ${res.status}`)

  return res.json()
}