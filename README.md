# Goodreads-Autobiography-Scraping
Extracts detailed metadata for books from the Goodreads **Autobiography** shelf:
**title, original title, author, genres (multi), first publication date, ratings, reviews, rating score, description, language, ISBN**.

> Built with Selenium + undetected-chromedriver and defensive waits/overlays handling.

## Features
- Collects item URLs from the shelf and opens each book page to gather rich metadata
- Extracts **multi-genre** lists and **publication details**
- Handles popups/overlays and iframes gracefully
- Outputs a **clean UTF-8 CSV** with stable column headers
