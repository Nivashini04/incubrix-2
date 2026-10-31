# IncuBrix Content Engine

**AI-powered content repurposing using free local AI**

## Overview
IncuBrix Content Engine transforms long-form source content into platform-specific social media drafts using a locally hosted AI model through Ollama.

## Features
- Generate 30 platform-specific content drafts.
- Support LinkedIn, Instagram and YouTube Shorts.
- AI-assisted content repurposing.
- Basic content validation.
- UTM tracking link generation.
- Content calendar generation.
- CSV and JSON exports.
- Video and carousel production concepts.

## Technology Stack
- Python
- Streamlit
- Ollama
- Llama 3.2
- Pandas

## Installation

1. Install Python and Ollama.
2. Download the Llama model:

   `ollama pull llama3.2:3b`

3. Install dependencies:

   `pip install -r requirements.txt`

4. Start Ollama.
5. Run the application:

   `python -m streamlit run app.py`

## Project Outputs
- `incubrix_assets.csv`
- `incubrix_assets.json`
- `calendar.csv`
- `video_concepts.csv`
- `carousel_concepts.csv`
- 5 carousel designs (25 slides)
- 2 sample short videos

## AI Workflow
1. Paste long-form source content.
2. Select target platforms.
3. Generate AI-assisted drafts.
4. Review and edit the drafts.
5. Export content and calendar files.

## Limitations
The generated drafts require human review before publishing. Video concepts are production outlines, not automatically rendered videos. Audience testing and publishing results must be completed and documented separately.

## Project
**IncuBrix Private Limited — Growth Engineer Assessment**