"""Key attributes per entity domain for discovery results.

The state alone often does not answer the question: the state of a weather
entity is "sunny" while the readings are attributes, and a cover's state is
"open" while how far is in current_position. Discovery results therefore show,
for each domain, the one or few attributes people actually ask about,
formatted with their units. Everything else is left to get_entity_details.

To support another domain or attribute, add a line to KEY_ATTRIBUTES.
"""

from typing import Any, Dict, Optional, Tuple

# domain -> ((attribute, label shown to the model, kind), ...)
#
# kinds:
#   "temp"         temperature; unit from the temperature_unit attribute,
#                  else the Home Assistant default
#   "percent"      value is already 0-100
#   "fraction"     value is 0-1, shown as a percentage
#   "brightness"   value is 0-255, shown as a percentage
#   "unit:<attr>"  value with the unit taken from another attribute
#   "raw"          shown as is
KEY_ATTRIBUTES: Dict[str, Tuple[Tuple[str, str, str], ...]] = {
    "weather": (
        ("temperature", "temperature", "temp"),
        ("humidity", "humidity", "percent"),
        ("wind_speed", "wind_speed", "unit:wind_speed_unit"),
        ("pressure", "pressure", "unit:pressure_unit"),
    ),
    "climate": (
        ("current_temperature", "current_temperature", "temp"),
        ("temperature", "target_temperature", "temp"),
        ("current_humidity", "current_humidity", "percent"),
        ("hvac_action", "hvac_action", "raw"),
    ),
    "water_heater": (
        ("current_temperature", "current_temperature", "temp"),
        ("temperature", "target_temperature", "temp"),
    ),
    "humidifier": (
        ("current_humidity", "current_humidity", "percent"),
        ("humidity", "target_humidity", "percent"),
        ("mode", "mode", "raw"),
    ),
    "cover": (("current_position", "position", "percent"),),
    "valve": (("current_position", "position", "percent"),),
    "fan": (
        ("percentage", "speed", "percent"),
        ("preset_mode", "preset", "raw"),
    ),
    "light": (("brightness", "brightness", "brightness"),),
    "media_player": (
        ("volume_level", "volume", "fraction"),
        ("source", "source", "raw"),
        ("media_title", "title", "raw"),
    ),
    "vacuum": (
        ("battery_level", "battery", "percent"),
        ("fan_speed", "fan_speed", "raw"),
    ),
}

# Kept for every domain: the unit of a sensor's number and what kind it is.
GENERIC_ATTRIBUTES = ("unit_of_measurement", "device_class", "friendly_name")

NO_VALUE_STATES = frozenset({"unavailable", "unknown"})


def join_unit(value: Any, unit: Any) -> str:
    """Format a number with its unit: 22 °C -> 22°C, 45 % -> 45%, 120 W."""
    if not unit:
        return str(value)
    unit = str(unit)
    if unit == "%" or unit.startswith("°"):
        return f"{value}{unit}"
    return f"{value} {unit}"


def _unit_attribute(kind: str) -> Optional[str]:
    """Name of the attribute that carries the unit for this kind, if any."""
    if kind == "temp":
        return "temperature_unit"
    if kind.startswith("unit:"):
        return kind[len("unit:"):]
    return None


def pick_attributes(domain: str, attributes: Dict[str, Any]) -> Dict[str, Any]:
    """Subset of an entity's attributes worth carrying in discovery results."""
    picked = {key: attributes[key] for key in GENERIC_ATTRIBUTES if key in attributes}
    for name, _label, kind in KEY_ATTRIBUTES.get(domain, ()):
        if attributes.get(name) is None:
            continue
        picked[name] = attributes[name]
        unit_attr = _unit_attribute(kind)
        if unit_attr and unit_attr in attributes:
            picked[unit_attr] = attributes[unit_attr]
    return picked


def _format_value(
    value: Any, kind: str, attrs: Dict[str, Any], default_temp_unit: Any
) -> Optional[str]:
    try:
        if kind == "temp":
            return join_unit(value, attrs.get("temperature_unit") or default_temp_unit)
        if kind == "percent":
            return f"{value}%"
        if kind == "fraction":
            return f"{round(float(value) * 100)}%"
        if kind == "brightness":
            return f"{round(float(value) * 100 / 255)}%"
        if kind.startswith("unit:"):
            return join_unit(value, attrs.get(kind[len("unit:"):]))
    except (TypeError, ValueError):
        return None
    return str(value)


def format_state(
    domain: Optional[str],
    state: Any,
    attributes: Optional[Dict[str, Any]],
    default_temp_unit: Any = None,
) -> str:
    """The state plus the key values of its domain, e.g.

    sensor:  "22.5°C"
    weather: "sunny, temperature=15.8°C, humidity=80%, wind_speed=3 m/s"
    cover:   "open, position=40%"
    """
    state_text = "" if state is None else str(state)
    if state_text in NO_VALUE_STATES:
        return state_text

    attrs = attributes or {}
    parts = [join_unit(state_text, attrs.get("unit_of_measurement"))]
    for name, label, kind in KEY_ATTRIBUTES.get(domain or "", ()):
        value = attrs.get(name)
        if value is None:
            continue
        text = _format_value(value, kind, attrs, default_temp_unit)
        if text is not None:
            parts.append(f"{label}={text}")
    return ", ".join(parts)
