"""Compact default definitions of the built-in MCP tools.

Small local models handle short, plain tool descriptions much better than long
ones, so these are deliberately minimal. Anything that has no use in the
current system (scripts, floors, labels...) is not advertised at all.

The original long definitions live in tool_examples/ as ready-to-copy
starting points; a file named tool_descriptions/<tool>.json replaces the
definition the LLM sees for that tool (see tool_descriptions.py).
"""

from typing import Any, Dict, List, Optional


def _str(description: str) -> Dict[str, Any]:
    return {"type": "string", "description": description}


def _tool(
    name: str,
    description: str,
    properties: Optional[Dict[str, Any]] = None,
    required: Optional[List[str]] = None,
) -> Dict[str, Any]:
    schema: Dict[str, Any] = {"type": "object", "properties": properties or {}}
    if required:
        schema["required"] = required
    return {"name": name, "description": description, "inputSchema": schema}


def default_tools(
    *,
    floors: bool = True,
    labels: bool = True,
    inferred_types: bool = True,
    scripts: bool = True,
    automations: bool = True,
) -> List[Dict[str, Any]]:
    """Build the built-in tool list in MCP format (name/description/inputSchema).

    The keyword flags say what the system actually contains; tools and
    parameters without a use are left out.
    """
    discover_props: Dict[str, Any] = {
        "area": _str("Area name exactly as in the index"),
        "domain": _str("e.g. light, switch, sensor"),
        "device_class": _str("e.g. temperature, motion"),
        "name_contains": _str("Text in the entity name"),
        "state": _str("e.g. on, off"),
    }
    if floors:
        discover_props["floor"] = _str("Floor name exactly as in the index")
    if labels:
        discover_props["label"] = _str("Label name exactly as in the index")
    if inferred_types:
        discover_props["inferred_type"] = _str("Type from inferred_types in the index")

    tools = [
        _tool(
            "discover_entities",
            "Find entities. Use it before reading or controlling any device.",
            discover_props,
        ),
        _tool(
            "get_entity_details",
            "Get the current state and attributes of entities.",
            {
                "entity_ids": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Entity IDs from discover_entities",
                }
            },
            ["entity_ids"],
        ),
        _tool("list_areas", "List areas with entity counts."),
        _tool("list_domains", "List domains with entity counts."),
        _tool("get_index", "Get the overview: areas, domains, device classes."),
        _tool(
            "perform_action",
            "Control a device using an entity ID from discover_entities.",
            {
                "domain": _str("e.g. light"),
                "action": _str("e.g. turn_on, turn_off, set_temperature"),
                "target": {
                    "type": "object",
                    "description": "The entity to control",
                    "properties": {"entity_id": _str("Entity ID")},
                    "required": ["entity_id"],
                },
                "data": {
                    "type": "object",
                    "description": "Extra parameters, e.g. brightness, temperature",
                },
            },
            ["domain", "action", "target"],
        ),
        _tool(
            "set_conversation_state",
            "Say whether you expect the user to reply.",
            {"expecting_response": {"type": "boolean", "description": "true if a reply is expected"}},
            ["expecting_response"],
        ),
        _tool(
            "get_entity_history",
            "Get past state changes of an entity.",
            {
                "entity_id": _str("Entity ID"),
                "hours": {"type": "integer", "description": "Hours back, default 24"},
            },
            ["entity_id"],
        ),
    ]

    if scripts:
        tools.append(
            _tool(
                "run_script",
                "Run a script and return its result.",
                {
                    "script_id": _str("Script entity ID"),
                    "variables": {"type": "object", "description": "Script inputs"},
                },
                ["script_id"],
            )
        )
    if automations:
        tools.append(
            _tool(
                "run_automation",
                "Trigger an automation.",
                {"automation_id": _str("Automation entity ID")},
                ["automation_id"],
            )
        )

    return tools
