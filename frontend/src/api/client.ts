import { EvaluationResponse, ExampleDetail, ExampleRecord, ExtractResponse, ModelOutput, Triple } from '../types'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

export async function fetchExamples(): Promise<ExampleRecord[]> {
  const response = await fetch(`${API_BASE}/examples`)
  if (!response.ok) throw new Error('Failed to load examples')
  return response.json()
}

export async function fetchExample(id: string): Promise<ExampleDetail> {
  const response = await fetch(`${API_BASE}/examples/${id}`)
  if (!response.ok) throw new Error('Failed to load example')
  return response.json()
}

export async function parseFile(file: File): Promise<string> {
  const formData = new FormData()
  formData.append('file', file)
  const response = await fetch(`${API_BASE}/parse`, { method: 'POST', body: formData })
  if (!response.ok) throw new Error((await response.json()).detail ?? 'Failed to parse file')
  const payload = await response.json()
  return payload.text
}

export async function extract(text: string): Promise<ExtractResponse> {
  const response = await fetch(`${API_BASE}/extract`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text }),
  })
  if (!response.ok) throw new Error((await response.json()).detail ?? 'Extraction failed')
  return response.json()
}

export async function evaluate(outputs: ModelOutput[], groundTruth?: Triple[]): Promise<EvaluationResponse> {
  const response = await fetch(`${API_BASE}/evaluate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ outputs, ground_truth: groundTruth?.length ? groundTruth : null }),
  })
  if (!response.ok) throw new Error('Evaluation failed')
  return response.json()
}
