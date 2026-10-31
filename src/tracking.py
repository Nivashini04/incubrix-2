from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse


def generate_utm_link(url, source, medium, campaign):
    parsed = urlparse(url)

    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise ValueError("Please provide a valid HTTP or HTTPS URL.")

    params = dict(parse_qsl(parsed.query))

    params.update({
        "utm_source": source,
        "utm_medium": medium,
        "utm_campaign": campaign
    })

    return urlunparse(
        parsed._replace(query=urlencode(params))
    )