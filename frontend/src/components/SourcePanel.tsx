import { Triple } from '../types'

type Props = {
  sourceText: string
  selectedTriple: Triple | null
}

function highlightText(text: string, start: number, end: number): JSX.Element {
  return (
    <>
      {text.slice(0, start)}
      <mark>{text.slice(start, end)}</mark>
      {text.slice(end)}
    </>
  )
}

export function SourcePanel({ sourceText, selectedTriple }: Props) {
  return (
    <section className="card source-panel">
      <h3>Source & Triple Detail</h3>
      {selectedTriple ? (
        <div className="triple-detail">
          <p><strong>{selectedTriple.subject}</strong> — <em>{selectedTriple.relation}</em> — <strong>{selectedTriple.object}</strong></p>
          <p className="muted">Model: {selectedTriple.model_name}</p>
          <p className="muted">Provenance sentence: {selectedTriple.provenance_sentence}</p>
        </div>
      ) : (
        <p className="muted">Select a graph edge to inspect provenance.</p>
      )}
      <div className="source-viewer">
        {selectedTriple
          ? highlightText(sourceText, selectedTriple.provenance_char_start, selectedTriple.provenance_char_end)
          : sourceText}
      </div>
    </section>
  )
}
