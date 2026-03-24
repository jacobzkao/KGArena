import CytoscapeComponent from 'react-cytoscapejs'
import { Triple } from '../types'
import { triplesToElements } from '../utils/graph'

type Props = {
  title: string
  triples: Triple[]
  onSelectTriple: (triple: Triple | null) => void
}

export function GraphPanel({ title, triples, onSelectTriple }: Props) {
  return (
    <section className="card graph-card">
      <h3>{title}</h3>
      {triples.length === 0 ? (
        <p className="muted">No triples available.</p>
      ) : (
        <CytoscapeComponent
          elements={triplesToElements(triples)}
          style={{ width: '100%', height: '280px', border: '1px solid #d7dbe2' }}
          layout={{ name: 'cose' }}
          stylesheet={[
            { selector: 'node', style: { label: 'data(label)', 'font-size': '10px', 'background-color': '#4c6ef5' } },
            { selector: 'edge', style: { label: 'data(label)', 'font-size': '9px', 'curve-style': 'bezier', width: 2, 'line-color': '#7f8ea3', 'target-arrow-shape': 'triangle', 'target-arrow-color': '#7f8ea3' } },
            { selector: ':selected', style: { 'background-color': '#e8590c', 'line-color': '#e8590c', 'target-arrow-color': '#e8590c' } },
          ]}
          cy={(cy) => {
            cy.on('tap', 'edge', (evt) => {
              const id = evt.target.id()
              onSelectTriple(triples.find((triple) => triple.id === id) ?? null)
            })
            cy.on('tap', (evt) => {
              if (evt.target === cy) {
                onSelectTriple(null)
              }
            })
          }}
        />
      )}
    </section>
  )
}
