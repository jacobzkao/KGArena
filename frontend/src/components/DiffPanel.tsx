import { EvaluationResponse } from '../types'

type Props = { evaluation?: EvaluationResponse | null }

export function DiffPanel({ evaluation }: Props) {
  return (
    <section className="card">
      <h3>Diff / Overlap</h3>
      {!evaluation ? (
        <p className="muted">Run extraction to see overlaps.</p>
      ) : (
        <div className="diff-groups">
          {evaluation.diff.map((group) => (
            <details key={group.label}>
              <summary>{group.label} ({group.triples.length})</summary>
              <table>
                <thead>
                  <tr>
                    <th>Subject</th>
                    <th>Relation</th>
                    <th>Object</th>
                  </tr>
                </thead>
                <tbody>
                  {group.triples.map((triple) => (
                    <tr key={`${group.label}-${triple.id}`}>
                      <td>{triple.subject}</td>
                      <td>{triple.relation}</td>
                      <td>{triple.object}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </details>
          ))}
        </div>
      )}
    </section>
  )
}
