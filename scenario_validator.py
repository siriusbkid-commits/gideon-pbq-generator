# scenario_validator.py

def validate_scenario(scenario: dict):
    """
    Validate scenario structure.
    Updated for Option A: 'name' is NOT allowed.
    'id' is required and supported.
    """

    # Allowed top-level fields
    allowed_fields = {
    "id",
    "description",
    "user",
    "location",
    "previous_location",
    "device",
    "mfa",
    "privilege_level",
    "sign_in_result",
    "metadata"
}
    

    # Reject any unexpected top-level fields
    for key in scenario.keys():
        if key not in allowed_fields:
            raise ValueError(f"Invalid field in scenario: {key}")

    # Metadata block is required
    if "metadata" not in scenario:
        raise ValueError("Scenario missing required 'metadata' block.")

    metadata = scenario["metadata"]

    # Required metadata fields
    required_metadata_fields = {
        "title",
        "learning_objectives",
        "difficulty"
    }

    for key in required_metadata_fields:
        if key not in metadata:
            raise ValueError(f"Metadata missing required field: {key}")

    # Optional metadata fields
    optional_metadata_fields = {
        "summary",
        "actors",
        "systems",
        "risks",
        "controls"
    }

    # Reject unexpected metadata fields
    for key in metadata.keys():
        if key not in required_metadata_fields and key not in optional_metadata_fields:
            raise ValueError(f"Invalid metadata field: {key}")

    return True
