"""Per-tool overrides of the tool definitions the LLM sees.

The built-in definitions (tool_definitions.py) are deliberately minimal. To
tune the wording for a particular model, put a file named

    tool_descriptions/<tool_name>.json

next to this module. Its content is a complete tool definition in the exact
OpenAI format that goes into the request as-is:

    {
      "type": "function",
      "function": {
        "name": "discover_entities",
        "description": "...",
        "parameters": {"type": "object", "properties": {...}}
      }
    }

If the file exists it replaces the built-in definition of that tool, otherwise
the built-in one is used. Files are re-read when their modification time
changes, so edits apply without restarting Home Assistant. An invalid file is
skipped with a warning and the built-in definition is used instead.

Ready-to-copy starting points (the original verbose definitions) are in
tool_examples/.
"""

import json
import logging
import os
import re
from typing import Any, Dict, List, Optional, Tuple

_LOGGER = logging.getLogger(__name__)

OVERRIDES_DIR = os.path.join(os.path.dirname(__file__), "tool_descriptions")

_SAFE_TOOL_NAME = re.compile(r"^[A-Za-z0-9_-]+$")

# path -> (mtime_ns, parsed definition or None if the file is invalid)
_cache: Dict[str, Tuple[int, Optional[Dict[str, Any]]]] = {}


def _validate(data: Any, tool_name: str) -> Optional[str]:
    """Return a problem description, or None if data is a usable definition."""
    if not isinstance(data, dict):
        return "top level must be a JSON object"
    if data.get("type") != "function":
        return 'missing "type": "function"'
    function = data.get("function")
    if not isinstance(function, dict):
        return 'missing "function" object'
    if function.get("name") != tool_name:
        return f'"function.name" must be "{tool_name}"'
    if not isinstance(function.get("parameters"), dict):
        return 'missing "function.parameters" object'
    return None


def _load_override(tool_name: str) -> Optional[Dict[str, Any]]:
    """Return the override definition for tool_name, or None to use the default."""
    if not _SAFE_TOOL_NAME.match(tool_name):
        return None

    path = os.path.join(OVERRIDES_DIR, f"{tool_name}.json")
    try:
        mtime = os.stat(path).st_mtime_ns
    except OSError:
        _cache.pop(path, None)
        return None

    cached = _cache.get(path)
    if cached and cached[0] == mtime:
        return cached[1]

    parsed: Optional[Dict[str, Any]] = None
    try:
        with open(path, encoding="utf-8") as handle:
            data = json.load(handle)
        problem = _validate(data, tool_name)
        if problem:
            _LOGGER.warning(
                "Ignoring tool override %s (%s); using the built-in definition",
                path,
                problem,
            )
        else:
            parsed = data
            _LOGGER.info("Loaded tool override for %s from %s", tool_name, path)
    except (OSError, ValueError) as err:
        _LOGGER.warning(
            "Ignoring tool override %s (%s); using the built-in definition",
            path,
            err,
        )

    _cache[path] = (mtime, parsed)
    return parsed


def apply_tool_overrides(tools: Optional[List[Dict[str, Any]]]) -> Optional[List[Dict[str, Any]]]:
    """Replace definitions in an OpenAI-format tool list with override files.

    Only tools that are already in the list are touched, so an override file
    can never enable a tool that is disabled or hidden.

    Does blocking file I/O: call it in an executor from async code.
    """
    if not tools:
        return tools

    result = []
    for tool in tools:
        name = (tool.get("function") or {}).get("name")
        override = _load_override(name) if isinstance(name, str) else None
        result.append(override if override is not None else tool)
    return result
