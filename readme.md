# News Xenophobia Analysis Tool

## Overview
This is a Streamlit-based web application designed to analyze news articles for xenophobic content. The tool allows users to input news text or upload PDF/Word documents, and it uses the Dify API to classify the level of xenophobia in the text. The analysis includes classification, sentiment, subject category, and relevant keywords.

## Features
- **Text Input**: Users can directly enter news content.
- **File Upload**: Supports uploading PDF and Word (`.docx`) files.
- **Xenophobia Classification**: Classifies the news on a scale from 1 to 4.
- **Sentiment Analysis**: Determines the sentiment of the article (negative, neutral, positive).
- **Subject Categorization**: Identifies the main topics and categories of the content.
- **Keyword Extraction**: Provides a list of relevant keywords.

## Setup and Installation
### Prerequisites
- Python 3.8+
- Streamlit
- PyMuPDF (for PDF text extraction)
- python-docx (for Word document text extraction)
- Requests (for making HTTP requests)

### Installation

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set the environment variable `APP_KEY` with your Dify API key:
   ```bash
   export APP_KEY=your_dify_api_key
   ```

### Running the Application
1. Start the Streamlit app:
   ```bash
   streamlit run app.py
   ```

2. Open your web browser and navigate to the provided local URL (usually `http://localhost:8501`).

## Usage
1. **Enter News Content**:
   - Type or paste the news content into the "News Content" text area.

2. **Upload a File**:
   - Click the "Upload a PDF or Word file" button and select a file to upload.

3. **Analyze**:
   - Click the "Analyze" button to start the analysis.
   - The results will be displayed on the right side of the screen, including the classification, reason, sentiment, subject category, and keywords.

## Configuration
### Dify Workflow
The Dify workflow is configured to analyze the news content and return the results in XML format. The configuration includes:
- **Model**: gpt-4o-mini
- **Prompt Template**: A detailed prompt to guide the LLM in classifying the news, determining sentiment, categorizing the subject, and extracting keywords.
- **Output Format**: XML format with specific tags for classification, reason, sentiment, and subject category.

### Example Output
```xml
<Classification>3</Classification>
<Reason>The article contains language that is moderately xenophobic. It uses terms and phrases that promote negative stereotypes about a specific group, but does not explicitly call for violence or extreme actions.</Reason>
<Sentiment>Negative</Sentiment>
<Category>Employment and Contribution</Category>
<Keywords>immigrants, jobs, work, contribution, problems</Keywords>
```

## Customization
- **CSS Styling**: The application includes custom CSS for a better user experience. You can modify the styles in the `st.markdown` section.
- **API Endpoints**: Update the `BASE_URL` and `APP_KEY` as needed to point to your Dify API.


---

Thank you for using the News Xenophobia Analysis Tool! 🤖