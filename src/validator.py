REQUIRED_FIELDS = [
    "platform",
    "hook",
    "caption",
    "hashtags",
    "call_to_action",
    "source_idea"
]


def validate_asset(asset):
    errors = []

    for field in REQUIRED_FIELDS:
        if field not in asset or not asset[field]:
            errors.append(f"Missing or empty field: {field}")

    if asset.get("platform") not in [
        "LinkedIn", "Instagram", "YouTube Shorts"
    ]:
        errors.append("Invalid platform")

    if not isinstance(asset.get("hashtags", []), list):
        errors.append("Hashtags must be a list")

    return {
        "valid": len(errors) == 0,
        "errors": errors
    }


def validate_assets(assets):
    results = [validate_asset(asset) for asset in assets]

    return {
        "total": len(assets),
        "valid": sum(r["valid"] for r in results),
        "invalid": sum(not r["valid"] for r in results),
        "results": results
    }