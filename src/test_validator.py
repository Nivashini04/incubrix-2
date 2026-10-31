from src.validator import validate_asset, validate_assets


def test_valid_asset():
    asset = {
        "platform": "LinkedIn",
        "hook": "Test hook",
        "caption": "Test caption",
        "hashtags": ["Marketing"],
        "call_to_action": "Follow us",
        "source_idea": "Content marketing"
    }

    assert validate_asset(asset)["valid"] is True


def test_invalid_asset():
    asset = {"platform": "Unknown"}

    assert validate_asset(asset)["valid"] is False


def test_multiple_assets():
    result = validate_assets([
        {
            "platform": "Instagram",
            "hook": "Hook",
            "caption": "Caption",
            "hashtags": ["AI"],
            "call_to_action": "Save",
            "source_idea": "Marketing"
        },
        {}
    ])

    assert result["total"] == 2
    assert result["valid"] == 1
    assert result["invalid"] == 1