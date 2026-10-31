
import streamlit as st
import pandas as pd
import json
import requests

from datetime import date, timedelta
from urllib.parse import urlencode, urlsplit, urlunsplit, parse_qsl

from src.generator import generate_assets


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="IncuBrix Content Engine",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 IncuBrix Content Engine")
st.caption("AI-powered content repurposing | Free local AI")

# --------------------------------------------------
# BRAND SETTINGS
# --------------------------------------------------

with st.sidebar:
    st.header("Brand Settings")

    brand = st.text_input("Brand name", "IncuBrix")

    audience = st.text_input(
        "Target audience",
        "Creators and small content teams"
    )

    website = st.text_input(
        "Website URL for tracking",
        "https://example.com"
    )

    campaign = st.text_input(
        "Campaign name",
        "content_campaign"
    )

    st.divider()
    st.caption("Powered by Ollama local AI")


# --------------------------------------------------
# SOURCE CONTENT
# --------------------------------------------------

st.header("1. Source Content")

source = st.text_area(
    "Paste a blog post, podcast transcript or webinar",
    height=220,
    placeholder="Paste your long-form content here..."
)

platforms = st.multiselect(
    "Select platforms",
    ["LinkedIn", "Instagram", "YouTube Shorts"],
    default=["LinkedIn", "Instagram", "YouTube Shorts"]
)

if st.button("✨ Generate 30 AI Assets", type="primary"):

    if not source.strip():
        st.error("Please enter source content.")

    elif not platforms:
        st.error("Please select at least one platform.")

    else:
        try:
            with st.spinner(
                "Local AI is generating content. Please wait..."
            ):
                assets = generate_assets(source, platforms)

                st.session_state.assets = assets
                st.session_state.generated = True

            st.success("Content generation completed!")

        except requests.exceptions.ConnectionError:
            st.error(
                "Cannot connect to Ollama. "
                "Please make sure Ollama is running."
            )

        except requests.exceptions.Timeout:
            st.error(
                "AI generation timed out. "
                "Try shorter source content."
            )

        except Exception as error:
            st.error(f"Generation failed: {error}")


# --------------------------------------------------
# RESULTS DASHBOARD
# --------------------------------------------------

if st.session_state.get("generated", False):

    assets = st.session_state.get("assets", [])

    if not assets:
        st.warning("No assets were generated.")

    else:

        st.divider()
        st.header("2. Content Dashboard")

        c1, c2, c3 = st.columns(3)

        c1.metric("Generated assets", len(assets))

        c2.metric(
            "Platforms",
            len(set(a.get("platform", "") for a in assets))
        )

        c3.metric("Target", 30)

        # --------------------------------------------------
        # REVIEW AND EDIT
        # --------------------------------------------------

        st.header("3. Review and Edit Content")

        df = pd.DataFrame(assets)

        edited = st.data_editor(
            df,
            use_container_width=True,
            num_rows="dynamic",
            key="content_editor"
        )

        edited_assets = edited.fillna("").to_dict("records")

        st.session_state.assets = edited_assets

        # --------------------------------------------------
        # QUALITY VALIDATION
        # --------------------------------------------------

        st.header("4. Quality Validation")

        valid_count = 0
        issues = []

        required_fields = [
            "platform",
            "hook",
            "caption",
            "hashtags",
            "call_to_action",
            "source_idea"
        ]

        for i, asset in enumerate(edited_assets, start=1):

            errors = []

            for field in required_fields:

                value = asset.get(field)

                if value is None or value == "":
                    errors.append(f"Missing {field}")

                elif isinstance(value, list) and not value:
                    errors.append(f"Empty {field}")

            if errors:
                issues.append(
                    f"Asset {i}: " + ", ".join(errors)
                )
            else:
                valid_count += 1

        v1, v2 = st.columns(2)

        v1.metric("Valid drafts", valid_count)

        v2.metric(
            "Drafts needing review",
            len(issues)
        )

        if issues:
            for issue in issues:
                st.warning(issue)
        else:
            st.success(
                "All drafts passed basic structural validation."
            )

        if len(edited_assets) != 30:
            st.info(
                f"Current output: {len(edited_assets)} assets. "
                "Assessment target: 30 assets."
            )

        # --------------------------------------------------
        # UTM TRACKING
        # --------------------------------------------------

        st.header("5. UTM Tracking Links")

        tracking_rows = []

        for i, asset in enumerate(edited_assets, start=1):

            try:
                parsed = urlsplit(website.strip())

                if parsed.scheme not in ("http", "https") or not parsed.netloc:
                    raise ValueError("Enter a valid website URL.")

                existing_params = dict(
                    parse_qsl(parsed.query, keep_blank_values=True)
                )

                new_params = {
                    "utm_source": asset.get(
                        "platform", "social"
                    ).lower().replace(" ", "_"),
                    "utm_medium": "social",
                    "utm_campaign": campaign,
                    "utm_content": f"asset_{i}"
                }

                existing_params.update(new_params)

                tracking_link = urlunsplit((
                    parsed.scheme,
                    parsed.netloc,
                    parsed.path,
                    urlencode(existing_params),
                    parsed.fragment
                ))

            except ValueError:
                tracking_link = "Invalid website URL"

            tracking_rows.append({
                "asset_id": i,
                "platform": asset.get("platform", ""),
                "tracking_link": tracking_link
            })

        tracking_df = pd.DataFrame(tracking_rows)

        st.dataframe(
            tracking_df,
            use_container_width=True
        )

        st.download_button(
            "Download UTM Tracking CSV",
            tracking_df.to_csv(index=False).encode("utf-8"),
            "utm_tracking_links.csv",
            "text/csv"
        )

        # --------------------------------------------------
        # CONTENT CALENDAR
        # --------------------------------------------------

        st.header("6. Content Calendar")

        start_date = st.date_input(
            "Publishing start date",
            value=date.today()
        )

        calendar_rows = []

        for i, asset in enumerate(edited_assets):

            hashtags = asset.get("hashtags", [])

            if isinstance(hashtags, str):
                hashtag_text = hashtags
            else:
                hashtag_text = " ".join(
                    "#" + str(tag).lstrip("#")
                    for tag in hashtags
                )

            calendar_rows.append({
                "publish_date": str(
                    start_date + timedelta(days=i)
                ),
                "platform": asset.get("platform", ""),
                "hook": asset.get("hook", ""),
                "caption": asset.get("caption", ""),
                "hashtags": hashtag_text,
                "call_to_action": asset.get(
                    "call_to_action", ""
                ),
                "status": "Draft"
            })

        calendar_df = pd.DataFrame(calendar_rows)

        st.dataframe(
            calendar_df,
            use_container_width=True
        )

        # --------------------------------------------------
        # EXPORT
        # --------------------------------------------------

        st.header("7. Export Your Work")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.download_button(
                "Download Assets CSV",
                edited.to_csv(index=False).encode("utf-8"),
                "incubrix_assets.csv",
                "text/csv"
            )

        with col2:
            st.download_button(
                "Download Calendar CSV",
                calendar_df.to_csv(index=False).encode("utf-8"),
                "calendar.csv",
                "text/csv"
            )

        with col3:
            st.download_button(
                "Download JSON",
                json.dumps(
                    edited_assets,
                    indent=2,
                    ensure_ascii=False
                ),
                "incubrix_assets.json",
                "application/json"
            )

        st.success("Your content workspace is ready!")

        # --------------------------------------------------
        # CREATIVE ASSET STUDIO
        # --------------------------------------------------

        st.divider()
        st.header("8. Creative Asset Studio")

        st.caption(
            "Transform generated social content into "
            "video and graphic production concepts."
        )

        # VIDEO CONCEPTS

        st.subheader("10 Short Video Concepts")

        video_assets = [
            a for a in edited_assets
            if a.get("platform") == "YouTube Shorts"
        ][:10]

        video_rows = []

        for i, asset in enumerate(video_assets, 1):

            video_rows.append({
                "Video": f"Video {i}",
                "Title": asset.get("hook", ""),
                "Opening Hook": asset.get("hook", ""),
                "Script": asset.get("caption", ""),
                "CTA": asset.get("call_to_action", ""),
                "Duration": "30-45 seconds",
                "Format": "Vertical 9:16",
                "Status": "Concept - Ready for production"
            })

        video_df = pd.DataFrame(video_rows)

        st.metric(
            "Short video concepts",
            len(video_df)
        )

        st.dataframe(
            video_df,
            use_container_width=True
        )

        st.download_button(
            "Download Video Concepts",
            video_df.to_csv(index=False).encode("utf-8"),
            "video_concepts.csv",
            "text/csv"
        )

        # GRAPHIC CONCEPTS

        st.subheader("5 Graphics and Carousel Concepts")

        instagram_assets = [
            a for a in edited_assets
            if a.get("platform") == "Instagram"
        ][:5]

        graphic_rows = []

        for i, asset in enumerate(instagram_assets, 1):

            graphic_rows.append({
                "Design": f"Carousel {i}",
                "Slide 1 - Hook": asset.get("hook", ""),
                "Slide 2 - Problem": (
                    "Why consistent content creation is difficult"
                ),
                "Slide 3 - Solution": asset.get("caption", ""),
                "Slide 4 - Key Takeaway": asset.get(
                    "source_idea", ""
                ),
                "Slide 5 - CTA": asset.get(
                    "call_to_action", ""
                ),
                "Design Format": "Instagram Carousel",
                "Status": "Concept - Ready for design"
            })

        graphic_df = pd.DataFrame(graphic_rows)

        st.metric(
            "Carousel concepts",
            len(graphic_df)
        )

        st.dataframe(
            graphic_df,
            use_container_width=True
        )

        st.download_button(
            "Download Carousel Concepts",
            graphic_df.to_csv(index=False).encode("utf-8"),
            "carousel_concepts.csv",
            "text/csv"
        )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "IncuBrix Content Engine | "
    "Powered by Ollama | Free Local AI"
)
