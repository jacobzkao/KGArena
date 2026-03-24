from services.normalization import normalize_for_matching, triple_key


def test_normalize_for_matching() -> None:
    value = '  NASA,  Inc. '
    assert normalize_for_matching(value) == 'nasa, inc'


def test_triple_key_relaxed() -> None:
    k1 = triple_key('NASA', 'Launched_By', 'Apollo 11', relaxed=True)
    k2 = triple_key('nasa', 'launched_by', 'apollo 11.', relaxed=True)
    assert k1 == k2
