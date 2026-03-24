from app.schemas import ModelOutput, Triple
from services.evaluation import compute_metrics


def _triple(id_: str, s: str, r: str, o: str, model_name: str) -> Triple:
    return Triple(
        id=id_,
        subject=s,
        relation=r,
        object=o,
        provenance_sentence='',
        provenance_char_start=0,
        provenance_char_end=0,
        confidence=None,
        model_name=model_name,
        raw_metadata={},
    )


def test_metrics_with_ground_truth() -> None:
    gt = [_triple('g1', 'Apollo 11', 'launched_by', 'NASA', 'ground_truth')]
    output = ModelOutput(
        model_name='REBEL',
        triples=[_triple('r1', 'Apollo 11', 'launched_by', 'NASA', 'REBEL')],
    )

    metrics = compute_metrics([output], gt)['REBEL']
    assert metrics.precision == 1.0
    assert metrics.recall == 1.0
    assert metrics.f1 == 1.0
