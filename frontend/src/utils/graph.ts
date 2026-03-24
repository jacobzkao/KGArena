import { Triple } from '../types'

export function triplesToElements(triples: Triple[]) {
  const nodeSet = new Set<string>()
  const nodes = [] as Array<{ data: { id: string; label: string } }>
  const edges = triples.map((triple) => {
    if (!nodeSet.has(triple.subject)) {
      nodeSet.add(triple.subject)
      nodes.push({ data: { id: triple.subject, label: triple.subject } })
    }
    if (!nodeSet.has(triple.object)) {
      nodeSet.add(triple.object)
      nodes.push({ data: { id: triple.object, label: triple.object } })
    }
    return {
      data: {
        id: triple.id,
        source: triple.subject,
        target: triple.object,
        label: triple.relation,
      },
    }
  })

  return [...nodes, ...edges]
}
