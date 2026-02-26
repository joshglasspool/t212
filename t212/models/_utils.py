def to_camel(field_name: str) -> str:
    """Convert snake_case field name to camelCase for JSON alias generation."""
    components = field_name.split("_")
    return components[0] + "".join(x.title() for x in components[1:])
