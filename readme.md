# Media Narrative Analysis

Paste a news article or upload a text-based PDF or DOCX. This Streamlit app flags potentially xenophobic language and shows the model's reason alongside its rating. I built the document handling and connected the app to a Dify workflow for a UNICC-sponsored project at NYU.

![Streamlit upload screen from the 2024 project report](assets/media-interface.png)

## Run locally

Import [the workflow](news-dify-config.yml) into Dify Cloud, configure its model provider and publish it. The app reads the workflow's API key from the `APP_KEY` environment variable. Newer Dify versions may require changes to the original export.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt requests
export APP_KEY='your-dify-workflow-key'
streamlit run demo.py
```

## What the app expects

The [document reader](demo.py#L49-L61) extracts embedded text from PDF pages and paragraphs from Word files. A scanned PDF needs OCR before upload. The app sends the resulting article as `news` and reads the workflow response from `data.outputs.text`.

The [parser](demo.py#L32-L47) requires both `<Classification>` and `<Reason>`. When the workflow returns a rating without an explanation, the interface shows a format error. Missing sentiment, category or keywords simply leaves those fields off the review card.

## Related paper

[Navigating Ethical Challenges in Media: AI Tools for Detecting Harmful Narratives](https://doi.org/10.1109/ISEC64801.2025.11147198), IEEE ISEC 2025. Elaine Zhang, Hillary Liu, Shixuan Lin, Qisong Zhou, Siranush Kostanyan and Andres Fortino.

[Full project, including the chatbot and analysis modules](https://shixuanlin.com/projects/multilingual-content-safety-analysis)
