from __future__ import annotations

import os

from services.model_loading import configure_huggingface_environment


def test_configure_huggingface_environment_sets_defaults(monkeypatch, tmp_path):
    monkeypatch.setenv('HF_HOME', str(tmp_path / 'hf-home'))
    monkeypatch.delenv('TRANSFORMERS_CACHE', raising=False)
    monkeypatch.delenv('HF_HUB_DISABLE_SYMLINKS_WARNING', raising=False)

    cache_root = configure_huggingface_environment()

    assert cache_root.exists()
    assert cache_root.name == 'hf-home'
    assert os.environ['HF_HOME'] == str(cache_root)
    assert os.environ['TRANSFORMERS_CACHE'] == str(cache_root / 'transformers')
    assert os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] == '1'
