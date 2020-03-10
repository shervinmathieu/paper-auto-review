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

The application can perform three main tasks: crawl academic search engines for papers, analyse the results of a crawl using provided keywords, and download the pdfs of the analysis results.

The application will guide you through the configuration process for each task.

Results will be stored at `$HOME/Documents/paper-auto-review`

## Paper search query syntax

The syntax for queries support boolean search. Search terms can be mixed with parenthesis and keywords (AND, OR) to modify the search query.

Search terms must be inside double quotes. AND keywords can be written as both 'AND' and '&'. OR keywords can be written as both 'OR' and '|'. The AND keyword has precedence over the OR keyword, you can change this behaviour by adding parentheses.

Examples of valid queries:

* ("banana" OR "apple") AND "juice"
* "banana juice" & "ingredients" | "recipe"
* "apple" | "banana" AND ("orange" & "pineapple" OR ("kiwi" OR "mango"))