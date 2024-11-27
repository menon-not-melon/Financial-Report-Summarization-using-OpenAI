import os
import re
import sys
import string
import nltk
import fitz
import tiktoken
import openai
from PyPDF2 import PdfReader
from docx import Document
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from langchain.llms import OpenAI
from langchain import PromptTemplate

# Downloading NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Defining prompts for creating summaries for the chunks
chunks_prompt = """
I want the detailed information on this
1. Business Overview – Include information such as the company's formation/incorporation date, headquarters location, business description, employee count, latest revenues, stock exchange listing and market capitalization, number of offices and locations, and details on their clients/customers. 2. Business Segment Overview. i. Extract the revenue percentage of each component (verticals, products, segments, and sections) as a part of the total revenue. ii. Performance: Evaluate the performance of each component by comparing the current year's sales/revenue and market share with the previous year's numbers.  iii. Sales Increase/Decrease explanation: Explain the causes of the increase or decrease in the performance of each component.  4. Breakdown of sales and revenue by geography, specifying the percentage contribution of each region to the total sales. 5. Summarize geographical data, such as workforce, clients, and offices, and outline the company's regional plans for expansion or reduction. 6. Analyze and explain regional sales fluctuations, including a geographical sales breakdown to identify sales trends. 7. Year-over-year sales increase or decline and reasons for the change. 8. Summary of rationale & considerations (risks & mitigating factors). 9. SWOT Analysis which elaborates to Strenths, weaknesses, opportunities and Threats a company. 10. Information about credit rating/credit rating change/change in the rating outlook 

Document:`{text}'
Summary:
"""
custom_prompt = PromptTemplate(template=chunks_prompt,input_variables=["text"])

# Defining prompt for creating a 2 page-summary with all our objectives. Prompt can be edited to suit the input cases
final_combine_prompt = """
Create a concise summary of the financial position of the company based on the provided speech. The summary should be strictly 2 pages long, covering the following key points and information about the mentioned points only and should be under the heading:

Business Overview:

Formation and Incorporation date, headquarters location, business description, employee count, latest revenues, stock exchange listing and market capitalization, number of offices, and key clients/customers.
The business overview should be in a paragraph and not in bullet points containing all the above points.
Business Segment Overview:

Extract the revenue percentage of each component (verticals, products, segments, sections) as part of total revenue in bullet points.
Evaluate performance of each component by comparing current year's sales/revenue and market share with previous year's numbers.
Explain reasons for any increase or decrease in performance in brief.
Geographical Sales Breakdown:

Summarize sales and revenue breakdown by geography, specifying percentage contribution of each region to total sales in bullet points.
Provide insights into workforce, client distribution, office locations, and outline regional expansion or reduction plans briefly.
Year-over-Year Sales Analysis:

Analyze year-over-year sales fluctuations and provide reasons for changes.
Rationale & Considerations:

Include SWOT analysis (Strengths, Weaknesses, Opportunities, Threats) where each of the components are under subheadings.
Discuss key considerations, risks, and mitigating factors impacting the company's financial outlook.
Credit Rating and Outlook:

Provide information about current credit rating, any changes, and outlook briefly.

"""
final_summary_prompt = PromptTemplate(template=final_combine_prompt,input_variables=['text'])

# Defining prompt for generating 1-page summary. Prompt can be edited to suit the input cases
final_combine_prompt_1_pager = f"""
1-page summary should be summary of the given text including the numbers from Business segment overview & geographical segment overview with all the important points in just 1 page. The businesss overview should not be more than 4 lines.
The entire summary should not exceed 320 words.
"""
final_summary_prompt_one_pager = PromptTemplate(template=final_combine_prompt_1_pager,input_variables=['text'])
