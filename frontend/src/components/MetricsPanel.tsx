import { EvaluationResponse } from '../types'

type Props = {
  evaluation?: EvaluationResponse | null
}

export function MetricsPanel({ evaluation }: Props) {
  if (!evaluation) return <section className="card"><h3>Metrics</h3><p className="muted">Run extraction to see metrics.</p></section>

  return (
    <section className="card">
      <h3>Metrics</h3>
      <table>
        <thead>
          <tr>
            <th>Model</th>
            <th>Triples</th>
            <th>Entities</th>
            <th>Relations</th>
            <th>Overlap</th>
            <th>P</th>
            <th>R</th>
            <th>F1</th>
          </tr>
        </thead>
        <tbody>
          {Object.entries(evaluation.metrics_by_model).map(([model, m]) => (
            <tr key={model}>
              <td>{model}</td>
              <td>{m.triple_count}</td>
              <td>{m.unique_entities}</td>
              <td>{m.unique_relations}</td>
              <td>{m.overlap_count}</td>
              <td>{m.precision?.toFixed(2) ?? '-'}</td>
              <td>{m.recall?.toFixed(2) ?? '-'}</td>
              <td>{m.f1?.toFixed(2) ?? '-'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  )
}
