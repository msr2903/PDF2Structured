---
title: PDF2JSON Extractor
emoji: 📄
colorFrom: blue
colorTo: indigo
sdk: streamlit
sdk_version: 1.45.0
app_file: streamlit_app.py
pinned: false
---
# PDF2Structured LLM Extractor

This application uses Google's Gemini language models to extract structured information (JSON) from PDF documents based on user-defined prompts. It provides a web interface built with Streamlit for uploading PDFs, selecting models, choosing or customizing extraction prompts, and viewing/downloading the results.

## Features

* **PDF Upload:** Upload PDF files directly through the web interface.
* **Gemini Model Selection:** Choose from available Gemini models for extraction.
* **Prompt Engineering:**
  * Use predefined prompt templates for common financial statements (Income Statement, Balance Sheet, Cash Flow).
  * Write or edit custom prompts to specify the desired extraction format and information.
* **JSON Extraction:** Extracts data from the PDF according to the prompt and returns it in JSON format.
* **PDF Viewer:** Displays the uploaded PDF alongside the extraction interface.
* **Download Results:** Download the extracted JSON data.

## File Structure

* `app.py`: Contains the main Streamlit application code, handling the user interface, file uploads, API calls, and display of results.
* `extractor.py`: Includes the core function `gemini_extract_pdf` which handles API key configuration, temporary file creation, uploading the PDF to the Gemini API, calling the generative model, processing the response, and cleaning up resources.
* `models.py`: Lists the available Gemini models that can be selected in the application.
* `prompts.py`: Defines standard prompt templates for extracting data from financial statements (Income Statement, Balance Sheet, Cash Flow) in a specific JSON structure. It also includes a dictionary mapping template names to their corresponding prompt text.

## Setup and Usage

1. **Prerequisites:**
   * Python 3.x
   * Required libraries (install using pip): `streamlit`, `google-generativeai`, `streamlit-pdf-viewer` (Note: `streamlit-pdf-viewer` might be the intended library based on usage in `app.py`).
     ```bash
     pip install streamlit google-generativeai streamlit-pdf-viewer
     ```
2. **API Key:**
   * Obtain a Google AI API Key from Google AI Studio.
   * You can set the API key as an environment variable named `GOOGLE_API_KEY`.
   * Alternatively, you can enter the API key directly into the application's sidebar.
3. **Run the Application:**
   ```bash
   streamlit run app.py
   ```
4. **Using the App:**
   * Open the application in your web browser.
   * Enter your Google AI API Key in the sidebar if not set as an environment variable.
   * Select the desired Gemini model from the sidebar.
   * Upload a PDF file.
   * Choose a prompt template or write/edit your custom extraction prompt in the text area.
   * Click the "Extract" button.
   * The uploaded PDF will be displayed on the left, and the extracted JSON output will appear on the right after processing.
   * You can download the extracted JSON using the download button.

## Prompt Templates

The application includes predefined prompts designed to extract data from Indonesian financial statements into a standardized JSON format:

* **Income Statement JSON:** Extracts items like revenue, cost of revenue, gross profit, operating expenses, net income, EPS, etc., mapping Indonesian descriptions to standard English labels and structuring them under period keys (YYYY-MM-DD).
* **Balance Sheet JSON:** Extracts assets (current/non-current), liabilities (current/non-current), and equity, mapping Indonesian descriptions to standard English labels and structuring them hierarchically under period keys (YYYY-MM-DD).
* **Cash Flow JSON:** Extracts cash flows from operating, investing, and financing activities, mapping Indonesian descriptions to standard English labels and structuring them by activity type under period keys (YYYY-MM-DD).

These templates provide detailed instructions to the LLM on how to identify company names, statement types, standardize date formats, map line items to a provided list of standard labels, and structure the output JSON. They handle cases where no suitable standard label is found by using an empty string as the key.

## Available Models

The application currently supports the following Gemini models (defined in `models.py`):

* `gemini-2.5-flash-preview-04-17`
* `gemini-2.5-pro-preview-03-25`
