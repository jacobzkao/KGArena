import { useEffect, useMemo, useState } from 'react'
import { evaluate, extract, fetchExample, fetchExamples, parseFile } from './api/client'
import { DiffPanel } from './components/DiffPanel'
import { GraphPanel } from './components/GraphPanel'
import { MetricsPanel } from './components/MetricsPanel'
import { SourcePanel } from './components/SourcePanel'
import { EvaluationResponse, ExampleRecord, ExtractResponse, Triple } from './types'

export default function App() {
  const [text, setText] = useState('')
  const [examples, setExamples] = useState<ExampleRecord[]>([])
  const [selectedExampleId, setSelectedExampleId] = useState('')
  const [groundTruth, setGroundTruth] = useState<Triple[]>([])
  const [result, setResult] = useState<ExtractResponse | null>(null)
  const [evaluation, setEvaluation] = useState<EvaluationResponse | null>(null)
  const [selectedTriple, setSelectedTriple] = useState<Triple | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchExamples().then(setExamples).catch((err: Error) => setError(err.message))
  }, [])

  const modelOutputs = useMemo(() => result?.outputs ?? [], [result])

  async function handleExampleChange(id: string) {
    setSelectedExampleId(id)
    if (!id) return
    try {
      const detail = await fetchExample(id)
      setText(detail.text)
      setGroundTruth(detail.ground_truth)
    } catch (err) {
      setError((err as Error).message)
    }
  }

  async function handleFileUpload(file: File) {
    try {
      const parsedText = await parseFile(file)
      setText(parsedText)
    } catch (err) {
      setError((err as Error).message)
    }
  }

  async function handleGroundTruthUpload(file: File) {
    const raw = await file.text()
    const parsed = JSON.parse(raw) as Triple[]
    setGroundTruth(parsed)
  }

  async function runCompare() {
    if (!text.trim()) {
      setError('Please provide input text first.')
      return
    }
    setError(null)
    setLoading(true)
    setSelectedTriple(null)
    try {
      const extraction = await extract(text)
      setResult(extraction)
      const evalResult = await evaluate(extraction.outputs, groundTruth)
      setEvaluation(evalResult)
    } catch (err) {
      setError((err as Error).message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app-shell">
      <header><h1>KG Arena</h1></header>
      <main className="layout">
        <aside className="card left-panel">
          <h3>Input</h3>
          <label>Example library</label>
          <select value={selectedExampleId} onChange={(e) => handleExampleChange(e.target.value)}>
            <option value="">Select example</option>
            {examples.map((example) => (
              <option key={example.id} value={example.id}>{example.title}</option>
            ))}
          </select>
          <label>Paste text</label>
          <textarea rows={12} value={text} onChange={(e) => setText(e.target.value)} />
          <label>Upload source (.txt, .pdf, .docx)</label>
          <input type="file" accept=".txt,.pdf,.docx" onChange={(e) => e.target.files && handleFileUpload(e.target.files[0])} />
          <label>Upload ground truth (JSON Triple[])</label>
          <input type="file" accept=".json" onChange={(e) => e.target.files && handleGroundTruthUpload(e.target.files[0])} />
          <button onClick={runCompare} disabled={loading}>{loading ? 'Running...' : 'Run Comparison'}</button>
          {result?.warnings?.length ? <div className="warning">{result.warnings.join('; ')}</div> : null}
          {error ? <div className="error">{error}</div> : null}
        </aside>

        <section className="center-panel">
          <div className="graph-grid">
            {['LUKE', 'REBEL', 'KnowGL'].map((modelName) => (
              <GraphPanel
                key={modelName}
                title={modelName}
                triples={modelOutputs.find((output) => output.model_name === modelName)?.triples ?? []}
                onSelectTriple={setSelectedTriple}
              />
            ))}
          </div>
          <div className="bottom-grid">
            <MetricsPanel evaluation={evaluation} />
            <DiffPanel evaluation={evaluation} />
          </div>
        </section>

        <aside className="right-panel">
          <SourcePanel sourceText={text} selectedTriple={selectedTriple} />
        </aside>
      </main>
    </div>
  )
}
