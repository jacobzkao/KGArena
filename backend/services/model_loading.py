from __future__ import annotations

import os
from pathlib import Path

from huggingface_hub import snapshot_download

LUKE_MODEL_ID = 'studio-ousia/luke-large-finetuned-conll-2003'
REBEL_MODEL_ID = 'Babelscape/rebel-large'


def configure_huggingface_environment() -> Path:
    """Configure Hugging Face cache defaults for predictable startup behavior."""
    cache_root = Path(os.getenv('HF_HOME', '/models/huggingface')).resolve()
    cache_root.mkdir(parents=True, exist_ok=True)

    os.environ.setdefault('HF_HOME', str(cache_root))
    os.environ.setdefault('TRANSFORMERS_CACHE', str(cache_root / 'transformers'))
    os.environ.setdefault('HF_HUB_DISABLE_SYMLINKS_WARNING', '1')

    return cache_root


def prefetch_models() -> None:
    """Download model snapshots ahead-of-time to avoid first-request latency."""
    configure_huggingface_environment()
    for model_id in (LUKE_MODEL_ID, REBEL_MODEL_ID):
        snapshot_download(repo_id=model_id, resume_download=True)
