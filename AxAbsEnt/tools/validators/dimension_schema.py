def validate_dimension_schema(dim: dict) -> bool:
    required_keys = ["code", "name", "formulation", "description"]
    return all(k in dim for k in required_keys)
