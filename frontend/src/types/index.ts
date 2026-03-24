export type Triple = {
  id: string
  subject: string
  relation: string
  object: string
  provenance_sentence: string
  provenance_char_start: number
  provenance_char_end: number
  confidence?: number | null
  model_name: string
  raw_metadata: Record<string, unknown>
}

export type ModelOutput = {
  model_name: string
  triples: Triple[]
  warning?: string | null
}

export type ExtractResponse = {
  text: string
  outputs: ModelOutput[]
  warnings: string[]
}

export type ExampleRecord = {
  id: string
  title: string
  description: string
}

export type ExampleDetail = ExampleRecord & {
  text: string
  ground_truth: Triple[]
}

export type Metrics = {
  triple_count: number
  unique_entities: number
  unique_relations: number
  overlap_count: number
  precision?: number | null
  recall?: number | null
  f1?: number | null
  exact_match_rate?: number | null
  relaxed_match_rate?: number | null
  hallucination_proxy?: number | null
}

export type DiffGroup = {
  label: string
  triples: Triple[]
}

export type EvaluationResponse = {
  metrics_by_model: Record<string, Metrics>
  diff: DiffGroup[]
}
