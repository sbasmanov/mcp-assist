"""JSON serialization for text that is shown to the LLM."""

import json
from typing import Any

# Internal identifiers the model never needs: it works with names.
_INDEX_INTERNAL_KEYS = frozenset({"floor_id", "label_ids"})

_EMPTY_VALUES = (None, "", [], {})


def llm_json(obj: Any, ensure_ascii: bool = False) -> str:
    """Serialize obj compactly for an LLM prompt or tool result.

    - No indentation: whitespace only costs tokens, which matters for small
      models with short context.
    - ensure_ascii=False by default: non-Latin names (e.g. Cyrillic) stay
      readable instead of turning into \\uXXXX escape sequences the model
      cannot map back to the words the user speaks.

    Do NOT use this for protocol traffic (JSON-RPC, SSE, WebSocket): there
    the escaping is harmless and standard.
    """
    return json.dumps(obj, ensure_ascii=ensure_ascii, separators=(",", ":"))


def compact_index(index: Any) -> Any:
    """Return a copy of the system index without empty values or internal IDs.

    Empty fields (aliases: [], floor: null, people: [] ...) only give a small
    model something to try to use. The stored index is left untouched because
    other code (e.g. discovery via inferred_types) reads the full structure.
    """
    if isinstance(index, dict):
        cleaned = {}
        for key, value in index.items():
            if key in _INDEX_INTERNAL_KEYS:
                continue
            value = compact_index(value)
            if value in _EMPTY_VALUES:
                continue
            cleaned[key] = value
        return cleaned
    if isinstance(index, list):
        items = [compact_index(item) for item in index]
        return [item for item in items if item not in _EMPTY_VALUES]
    return index
