"""Constants for the MCP Assist integration."""

DOMAIN = "mcp_assist"
SYSTEM_ENTRY_UNIQUE_ID = "mcp_assist_system_settings"

# Server type options
SERVER_TYPE_LMSTUDIO = "lmstudio"
SERVER_TYPE_LLAMACPP = "llamacpp"
SERVER_TYPE_OLLAMA = "ollama"
SERVER_TYPE_OPENAI = "openai"
SERVER_TYPE_GEMINI = "gemini"
SERVER_TYPE_ANTHROPIC = "anthropic"
SERVER_TYPE_OPENROUTER = "openrouter"
SERVER_TYPE_OPENCLAW = "openclaw"
SERVER_TYPE_VLLM = "vllm"
SERVER_TYPE_HERMES = "hermes"

# Configuration keys
CONF_PROFILE_NAME = "profile_name"
CONF_SERVER_TYPE = "server_type"
CONF_API_KEY = "api_key"
CONF_LMSTUDIO_URL = "lmstudio_url"
CONF_MODEL_NAME = "model_name"
CONF_MCP_PORT = "mcp_port"
CONF_AUTO_START = "auto_start"
CONF_SYSTEM_PROMPT = "system_prompt"
CONF_TECHNICAL_PROMPT = "technical_prompt"
CONF_CONTROL_HA = "control_home_assistant"
CONF_RESPONSE_MODE = "response_mode"
CONF_FOLLOW_UP_MODE = "follow_up_mode"  # Keep for backward compatibility
CONF_TEMPERATURE = "temperature"
CONF_MAX_TOKENS = "max_tokens"
CONF_MAX_HISTORY = "max_history"
CONF_MAX_ITERATIONS = "max_iterations"
CONF_DEBUG_MODE = "debug_mode"
CONF_ENABLE_CUSTOM_TOOLS = "enable_custom_tools"
CONF_BRAVE_API_KEY = "brave_api_key"
CONF_ALLOWED_IPS = "allowed_ips"
CONF_SEARCH_PROVIDER = "search_provider"
CONF_ENABLE_GAP_FILLING = "enable_gap_filling"
CONF_OLLAMA_KEEP_ALIVE = "ollama_keep_alive"
CONF_OLLAMA_NUM_CTX = "ollama_num_ctx"
CONF_FOLLOW_UP_PHRASES = "follow_up_phrases"
CONF_END_WORDS = "end_words"
CONF_CLEAN_RESPONSES = "clean_responses"
CONF_TIMEOUT = "timeout"
CONF_ALLOWED_TOOLS = "allowed_tools"
# Message spoken/shown when the tool-call loop hits max_iterations without a
# final answer. Overridable per-profile so it can be set in the profile's own
# language instead of always falling back to English. Use {max_iterations} as
# a placeholder for the configured limit.
CONF_LIMIT_MESSAGE = "limit_message"
# Whether pure state-read answers get replaced with a placeholder in history
# before the next request (see agent.py _STALE_VALUE_PLACEHOLDER). Small
# models tend to parrot a stale value instead of re-calling a tool; larger
# models can often be trusted with the real history instead. Per-profile so
# a small-model and a large-model profile can each use the setting that
# suits them.
CONF_MASK_STALE_READS = "mask_stale_reads"
# Text substituted for a masked turn (see CONF_MASK_STALE_READS above).
# Overridable per-profile, same reasoning as CONF_LIMIT_MESSAGE: the default
# below is English regardless of prompt language, so a non-English profile
# should set this to a translation, or to an empty string to drop the
# anomalous text pattern entirely instead of substituting one - some small
# models turn out to imitate ANY unusual turn sitting in recent history
# (including this placeholder itself), so removing it outright can work
# better than translating it.
CONF_STALE_READ_PLACEHOLDER = "stale_read_placeholder"
# Whether a masked turn uses CONF_STALE_READ_PLACEHOLDER's text at all.
# When False, the masked turn's assistant message (and its history-side
# `user` question stays) is dropped from the messages sent to the model
# entirely, instead of substituting any placeholder text - including an
# empty string. This sidesteps the HA options-flow quirk where clearing an
# Optional field with a non-empty default just resubmits that default, and
# it removes the copyable-anomalous-text substrate outright rather than
# picking better wording for it. Default True preserves existing behavior
# (use the placeholder text) for profiles created before this setting
# existed.
CONF_STALE_READ_USE_PLACEHOLDER = "stale_read_use_placeholder"

# All MCP tools the agent can be given access to. Used both as the source of
# selector options in the config/options flow and as the default (all
# enabled) for entries that predate this setting.
#
# Keep in sync with the tool names registered in mcp_server.py's
# handle_tools_list() (built-ins) and custom_tools/*.py (search, read_url -
# only actually registered when a search provider is configured). A tool
# fetched from the MCP server whose name is NOT in this list is never hidden
# by a stale copy of this list; see the allowed_tools filtering in agent.py.
ALL_MCP_TOOLS = [
    "discover_entities",
    "get_entity_details",
    "list_areas",
    "list_domains",
    "get_index",
    "perform_action",
    "get_entity_history",
    "run_script",
    "run_automation",
    "set_conversation_state",
    "search",
    "read_url",
]

# Default values
DEFAULT_SERVER_TYPE = "lmstudio"
DEFAULT_LMSTUDIO_URL = "http://localhost:1234"
DEFAULT_LLAMACPP_URL = "http://localhost:8080"
DEFAULT_OLLAMA_URL = "http://localhost:11434"
# OpenClaw Gateway defaults
CONF_OPENCLAW_HOST = "openclaw_host"
CONF_OPENCLAW_PORT = "openclaw_port"
CONF_OPENCLAW_TOKEN = "openclaw_token"
CONF_OPENCLAW_USE_SSL = "openclaw_use_ssl"
CONF_OPENCLAW_SESSION_KEY = "openclaw_session_key"
DEFAULT_OPENCLAW_HOST = "localhost"
DEFAULT_OPENCLAW_PORT = 18789
DEFAULT_OPENCLAW_USE_SSL = True
DEFAULT_OPENCLAW_SESSION_KEY = "main"
DEFAULT_VLLM_URL = "http://localhost:8000"
# Hermes Agent (Nous Research) defaults — OpenAI-compatible API server
CONF_HERMES_URL = "hermes_url"
CONF_HERMES_SESSION_KEY = "hermes_session_key"
DEFAULT_HERMES_URL = "http://localhost:8642"
DEFAULT_HERMES_SESSION_KEY = "homeassistant"
DEFAULT_HERMES_MODEL = "hermes-agent"
DEFAULT_MCP_PORT = 8090
DEFAULT_API_KEY = ""

# Cloud provider base URLs
OPENAI_BASE_URL = "https://api.openai.com"
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai"
ANTHROPIC_BASE_URL = "https://api.anthropic.com"
OPENROUTER_BASE_URL = "https://openrouter.ai/api"

# No hardcoded model lists - models are fetched dynamically from provider APIs
DEFAULT_MODEL_NAME = "model"
DEFAULT_SYSTEM_PROMPT = """You are a Home Assistant voice assistant.
Reply in the user's language, briefly and naturally, as plain text suitable for speech: no lists, no markdown.
Call devices by their friendly names, never by entity IDs. Say states in natural words ("turned on", "at home").
Never mention tools, the INDEX or your reasoning. Do not ask questions you don't need answered."""
DEFAULT_CONTROL_HA = True
DEFAULT_RESPONSE_MODE = "default"
DEFAULT_FOLLOW_UP_MODE = "default"  # Keep for backward compatibility
DEFAULT_TEMPERATURE = 0.5
DEFAULT_MAX_TOKENS = 500
# OpenAI reasoning models (GPT-5.x, o-series) count reasoning tokens against
# max_completion_tokens; a 500-token voice budget yields empty visible replies
MIN_REASONING_COMPLETION_TOKENS = 2000
DEFAULT_MAX_HISTORY = 10
DEFAULT_MAX_ITERATIONS = 10
DEFAULT_DEBUG_MODE = False
DEFAULT_ENABLE_CUSTOM_TOOLS = False
DEFAULT_BRAVE_API_KEY = ""
DEFAULT_ALLOWED_IPS = ""
DEFAULT_SEARCH_PROVIDER = "none"
DEFAULT_ENABLE_GAP_FILLING = True
DEFAULT_OLLAMA_KEEP_ALIVE = "5m"  # 5 minutes
DEFAULT_OLLAMA_NUM_CTX = 0  # 0 = use model default
DEFAULT_FOLLOW_UP_PHRASES = "anything else, what else, would you, do you, should i, can i, which, how can, what about, is there"
DEFAULT_END_WORDS = "stop, cancel, no, nope, thanks, thank you, bye, goodbye, done, never mind, nevermind, forget it, that's all, that's it"
DEFAULT_CLEAN_RESPONSES = False
DEFAULT_TIMEOUT = 30
DEFAULT_LIMIT_MESSAGE = (
    "I reached the maximum of {max_iterations} tool calls while processing your "
    "request. Try simplifying your request, or increase the limit in Advanced "
    "Settings if you have a complex automation need."
)
# Default True: preserves the existing (small-model-safe) behavior for
# profiles created before this setting existed.
DEFAULT_MASK_STALE_READS = True
DEFAULT_STALE_READ_PLACEHOLDER = (
    "(Reported a live value here earlier - it may already be outdated. "
    "Do not reuse it; call a tool again for the current value.)"
)
DEFAULT_STALE_READ_USE_PLACEHOLDER = True
# Default is "all tools enabled" - matches pre-existing behavior for entries
# created before this setting existed, and is the sane default for new ones.
DEFAULT_ALLOWED_TOOLS = list(ALL_MCP_TOOLS)

# MCP Server settings
MCP_SERVER_NAME = "ha-entity-discovery"
MCP_PROTOCOL_VERSION = "2024-11-05"

# Entity discovery limits
MAX_ENTITIES_PER_DISCOVERY = 50  # Default, can be overridden in system settings
MAX_DISCOVERY_RESULTS = 100
CONF_MAX_ENTITIES_PER_DISCOVERY = "max_entities_per_discovery"
DEFAULT_MAX_ENTITIES_PER_DISCOVERY = 50

# Shared setting: escape non-ASCII characters as \uXXXX in JSON text that is
# shown to the LLM (index, tool results). Off by default - small models read
# real Cyrillic/etc. characters far better than escape sequences.
CONF_ENSURE_ASCII = "ensure_ascii"
DEFAULT_ENSURE_ASCII = False

RESPONSE_MODE_INSTRUCTIONS = {
    "none": """## Follow-up Questions
Do NOT ask follow-up questions. Complete the task and end immediately.

## Ending Conversations
Always end after completing the task.""",
    "default": """## Follow-up Questions
Generate contextually appropriate follow-up questions naturally:
- After single device actions: Create a natural follow-up asking if the user needs help with anything else (vary phrasing each time)
- When reporting adjustable status: Spontaneously suggest adjusting it in a natural way
- For partial completions: Ask if the user wants you to complete the remaining tasks
Always vary your phrasing - never repeat the same question twice in a conversation.

Do NOT ask generic "anything else?" or "can I help with anything else?" questions without specific context.
When asking a question, use the set_conversation_state tool to indicate you're expecting a response.

## Ending Conversations
After completing the task, end the conversation unless a natural follow-up is relevant.""",
    "always": """## Follow-up Questions
Generate contextually appropriate follow-up questions naturally:
- After single device actions: Create a natural follow-up asking if the user needs help with anything else (vary phrasing each time)
- When reporting adjustable status: Spontaneously suggest adjusting it in a natural way
- For partial completions: Ask if the user wants you to complete the remaining tasks
Always vary your phrasing - never repeat the same question twice in a conversation.
When asking a question, use the set_conversation_state tool to indicate you're expecting a response.

## Ending Conversations
When user indicates they're done, acknowledge and end naturally.""",
}

DEFAULT_TECHNICAL_PROMPT = """TOOLS
discover_entities: find entities and read their current state and key values. It changes nothing.
get_entity_details: all attributes of an entity you already found.
perform_action: control an entity (turn on/off, open/close, set a value).
get_entity_history: past state changes ("when did the door open?").
run_script, run_automation: only for a script or automation you discovered.
set_conversation_state: only when you ask the user a question and wait for the answer.

INDEX
The INDEX at the end lists what exists in this home: areas, domains, device classes. It has no states.
Use its names exactly as written; never translate or invent names. Never guess entity IDs.
Do not call list_areas, list_domains or get_index.

FINDING ENTITIES
- The user names a device (lamp, TV, door): discover_entities with name_contains = a word copied from the user's request, never translated, in its base form (for "What's the window's status?": name_contains="window"), plus the area if one applies (see below), nothing else.
- The user asks about a kind of value (temperature, humidity, motion, weather): use domain or device_class from the INDEX.
- The user names a room: use that area and search only there.
- No room named: use the Assistant location from the user message as the area. If it is Unknown, or nothing is found there, search without an area. One match anywhere: use it. Several matches and unclear which: ask which one.
- Take the room only from the current request or from Assistant location. Ignore rooms mentioned in earlier messages.
- "everywhere", "all rooms", "the whole house": search without an area and do not use Assistant location.
- Several devices in one request: handle each one separately, answer after all are done.
- Nothing found: follow the hint in the tool result, retry at most once, then say you could not find it.

VALUES AND STATES
- Any answer about a current state or value must come from a tool call made for this request. Earlier results in the conversation are outdated.
- If discover_entities found the entity but the result lacks the value you need (position, volume, source, setpoint...), call get_entity_details for it. Use get_entity_details only if you need additional information that is not included in the result of discover_entities.
- After perform_action do not assume the new state; call a state tool if the user asks for it.

CONTROL
- Any request to change something (turn on/off, open/close, set a value) must end with a perform_action call. discover_entities only searches and changes nothing.
- Wrong: discover_entities → "Done."  Right: discover_entities → perform_action → "Done."
- Say it was done only after perform_action succeeded.
- If perform_action fails, correct the action name from the error at most once. If the device does not support the action, do not retry: tell the user it cannot be done.

UNCLEAR INPUT
If the request is not a clear command or question (noise, sound labels like "[music]", fragments), do not act and do not claim anything: say briefly that you did not catch it.

EXAMPLES (a description of behavior, not a template for your reply — never output tool names or parentheses in your answer)
"Turn on the fan" (Assistant location: Living room): look up entities by the word "fan" in the area "Living room"; switch on the one found; reply only "Done."
"Open the blinds halfway": look up entities by the word "blinds"; set the found cover's position to 50; reply "Done."
"What's the window's status?": look up entities by the word "window"; if the state isn't in the search result, look up that entity's details separately; then answer.
"What is the temperature in the kitchen?": look up entities in the area "Kitchen" with device class "temperature"; answer with the value from the result.

{response_mode}

INDEX
{index}"""
