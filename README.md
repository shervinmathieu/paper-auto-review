# Paper automatic systematic review
Python tool to scrape search engines for papers, and sort them by relevance according to provided keywords.

# Setup

Create a Python 3 virtual environment and activate it :
> python3 -m venv venv-directory-path
>
> source venv-directory-path/bin/activate

Install all dependencies :

> pip install spacy spacy-langdetect prompt-toolkit lark-parser scrapy
>
> python -m spacy download en_core_web_sm

# Usage

Navigate to the src directory (or else the scraping library scrapy will not work).

Launch `main.py`.

The application can perform three main tasks: crawl academic search engines for papers, analyse the results of a crawl using provided keywords, and download the pdfs of the 

The application will guide you through the configuration process for these tasks

Results will be stored at `$HOME/Documents/paper-auto-review`