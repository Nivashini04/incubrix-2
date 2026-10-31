from src.tracking import generate_utm_link


def test_utm_link():
    link = generate_utm_link(
        "https://example.com",
        "instagram",
        "social",
        "launch"
    )

    assert "utm_source=instagram" in link
    assert "utm_medium=social" in link
    assert "utm_campaign=launch" in link