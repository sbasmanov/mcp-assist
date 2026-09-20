# tool_descriptions

Put a file named `<tool_name>.json` here to replace the definition of that tool
that the LLM sees (for example `discover_entities.json`).

The file is a complete tool definition in the OpenAI format. It is inserted into
the request as-is:

```json
{
  "type": "function",
  "function": {
    "name": "discover_entities",
    "description": "Find entities. Use it before reading or controlling any device.",
    "parameters": {
      "type": "object",
      "properties": {
        "area": {"type": "string", "description": "Area name exactly as in the index"}
      }
    }
  }
}
```

Rules:

- `function.name` must match the file name, and `function.parameters` must be an object.
- If the file is missing, the built-in compact definition is used.
- If the file is invalid, a warning is written to the log and the built-in definition is used.
- A file only changes a tool that is currently offered. It cannot enable a tool that is
  disabled in the integration settings or hidden because it has no use in your system
  (for example `run_script` when there are no scripts).
- Changes are picked up automatically (the file modification time is checked); no restart is needed.

Starting points: the original, verbose definitions are in `../tool_examples/`. Copy a file
from there into this directory and edit it.

## Back up this directory before updating

HACS replaces the whole `mcp_assist` folder on update, which deletes everything in
`tool_descriptions`. Copy your `*.json` files somewhere outside `custom_components`
before you update, and put them back afterwards.
