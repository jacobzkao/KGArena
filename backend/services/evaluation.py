from __future__ import annotations

from collections import defaultdict
from itertools import combinations

from app.schemas import DiffGroup, Metrics, ModelOutput, Triple
from services.normalization import triple_key


def _triple_set(triples: list[Triple], relaxed: bool = False) -> set[str]:
    return {triple_key(t.subject, t.relation, t.object, relaxed=relaxed) for t in triples}


def compute_metrics(outputs: list[ModelOutput], ground_truth: list[Triple] | None) -> dict[str, Metrics]:
    metrics: dict[str, Metrics] = {}
    exact_truth = _triple_set(ground_truth or [], relaxed=False)
    relaxed_truth = _triple_set(ground_truth or [], relaxed=True)

    all_sets = {output.model_name: _triple_set(output.triples, relaxed=False) for output in outputs}

    for output in outputs:
        entities = {t.subject for t in output.triples} | {t.object for t in output.triples}
        relations = {t.relation for t in output.triples}
        model_set = all_sets[output.model_name]
        overlap_count = sum(len(model_set & other_set) for model, other_set in all_sets.items() if model != output.model_name)

        base = Metrics(
            triple_count=len(output.triples),
            unique_entities=len(entities),
            unique_relations=len(relations),
            overlap_count=overlap_count,
        )

        if ground_truth:
            tp_exact = len(model_set & exact_truth)
            tp_relaxed = len(_triple_set(output.triples, relaxed=True) & relaxed_truth)
            precision = tp_exact / len(model_set) if model_set else 0.0
            recall = tp_exact / len(exact_truth) if exact_truth else 0.0
            f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0
            base.precision = precision
            base.recall = recall
            base.f1 = f1
            base.exact_match_rate = tp_exact / len(exact_truth) if exact_truth else 0.0
            base.relaxed_match_rate = tp_relaxed / len(relaxed_truth) if relaxed_truth else 0.0
            base.hallucination_proxy = (len(model_set - exact_truth) / len(model_set)) if model_set else 0.0

        metrics[output.model_name] = base

    return metrics


def compute_diff(outputs: list[ModelOutput], ground_truth: list[Triple] | None = None) -> list[DiffGroup]:
    name_to_triples = {output.model_name: output.triples for output in outputs}
    key_to_triple: dict[str, Triple] = {}
    sets: dict[str, set[str]] = {}

    for name, triples in name_to_triples.items():
        sets[name] = set()
        for triple in triples:
            key = triple_key(triple.subject, triple.relation, triple.object)
            sets[name].add(key)
            key_to_triple.setdefault(key, triple)

    groups: list[DiffGroup] = []

    if len(outputs) >= 3:
        common = set.intersection(*sets.values())
        groups.append(DiffGroup(label='Common to all', triples=[key_to_triple[k] for k in sorted(common)]))

    for name, triple_set in sets.items():
        others = set().union(*(v for k, v in sets.items() if k != name))
        unique = triple_set - others
        groups.append(DiffGroup(label=f'Unique to {name}', triples=[key_to_triple[k] for k in sorted(unique)]))

    for left, right in combinations(sets.keys(), 2):
        shared = (sets[left] & sets[right]) - set().union(*(sets[n] for n in sets if n not in {left, right}))
        groups.append(DiffGroup(label=f'Shared by {left} + {right}', triples=[key_to_triple[k] for k in sorted(shared)]))

    if ground_truth:
        truth_keys = _triple_set(ground_truth)
        for name, triple_set in sets.items():
            missing = truth_keys - triple_set
            hallucinated = triple_set - truth_keys
            groups.append(DiffGroup(label=f'{name} missing vs ground truth', triples=[t for t in ground_truth if triple_key(t.subject, t.relation, t.object) in missing]))
            groups.append(DiffGroup(label=f'{name} extra vs ground truth', triples=[key_to_triple[k] for k in sorted(hallucinated)]))

    return groups
