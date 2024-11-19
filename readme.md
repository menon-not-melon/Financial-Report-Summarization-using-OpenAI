# Report Summarization for Financial Advisors

This project aims to extract texts from PDF documents and generate concise summaries of financial information using OpenAI’s GPT-4 model. It is designed to automate the extraction and summarization process for multiple PDF files.

## 1. Installation

To run the Python script, ensure you have the following packages installed:

- Fitz
- Pymupdf
- Langchain
- Langchain_community
- Tiktoken
- OpenAI
- Docx

Or you can install Python packages running this pip command in the terminal:
```
pip install -r requirements.txt
```
## 2. Usage

### Running the Python script

1. Obtain an OpenAI API key and replace `{your_openai_key}` in the script.
2. Run the Python file `summarization.py`.
3. Input the file paths separated by commas when prompted, e.g., `"Apple 10K.pdf,Apple 10Q.pdf,Apple_Deutsche_Jun23.pdf,Apple_JPM_Jun23.pdf"`.

### Output

After successful execution, the following files will be saved in your current directory:

- `final_summary_one_page.docx`: One-page summary
- `final_summary_two_page.docx`: Two-page summary

You will receive confirmation messages once the summaries are generated and saved.

## 3. Dependencies

- **Pymupdf and fitz:** For reading PDF files and extracting text.
- **Langchain:** For utilizing PromptTemplate to use with OpenAI's GPT-4o-mini model
- **Tiktoken:** To count the number of tokens.
- **OpenAI:** Python client for the OpenAI API.
- **Docx:** To write text into .docx files and save them.



## 4. Error Handling during Script Execution

Solutions for possible errors one can encounter during script execution:

- **File Not Found:** Check that the file paths are correct and accessible.
- **PDF Parsing Error:** Some PDFs may not be compatible with PyMuPDF (fitz). Verify PDF compatibility or try other PDF libraries.
- **OpenAI API Errors:** Ensure your API key is correct and active. Check internet connectivity and API rate limits.

## 5. Customization

- Modify `chunks_prompt`, `final_combine_prompt`, and `final_combine_prompt_1_pager` templates to adjust the content and style of generated summaries.

## 6. Future Enhancements
- Additional Output Formats: Support for Excel or PowerPoint summaries.
- Batch Processing: Automate the summarization of PDFs in a folder without manual file path entry.
- GUI Integration: Add a user-friendly interface for non-technical users.
- Expanded Language Support: Extend functionality to include multilingual summarization for global financial reports.
- Advanced Customization: Provide a configuration file to adjust prompts, summary length, and output formatting.

## 7. License
This project is licensed under the MIT License. Feel free to use and modify the code for personal or commercial purposes.
