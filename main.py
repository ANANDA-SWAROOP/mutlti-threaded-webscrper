from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import requests
from fastapi.middleware.cors import CORSMiddleware
from bs4 import BeautifulSoup
import re
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins; adjust this in production for security
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)
# Serve the HTML page at the root URL
@app.get("/", response_class=HTMLResponse)
async def get_home():
    with open("index.html") as f:
        return f.read()

# API endpoint to handle scraping requests
@app.post("/scrape")
async def scrape(request: Request):
    # Parse the incoming JSON request
    data = await request.json()
    url = data["url"]
    options = data["options"]

    # Fetch the webpage content
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes
    except requests.RequestException as e:
        return {"error": f"Failed to fetch URL: {str(e)}"}

    # Parse the HTML content
    soup = BeautifulSoup(response.text, "html.parser")
    results = {}

    # Use ThreadPoolExecutor to scrape data types concurrently
    with ThreadPoolExecutor(max_workers=len(options)) as executor:
        future_to_option = {}
        for option in options:
            if option == "headings":
                future = executor.submit(extract_headings, soup)
            elif option == "text":
                future = executor.submit(extract_text, soup)
            elif option == "links":
                future = executor.submit(extract_links, soup)
            elif option == "emails":
                future = executor.submit(extract_emails, soup)
            elif option == "images":
                future = executor.submit(extract_images, soup)
            elif option == "contacts":
                future = executor.submit(extract_contacts, soup)
            future_to_option[future] = option

        # Collect results from completed threads
        for future in concurrent.futures.as_completed(future_to_option):
            option = future_to_option[future]
            try:
                results[option] = future.result()
            except Exception as e:
                results[option] = [f"Error extracting {option}: {str(e)}"]

    return results

# Data extraction functions
def extract_headings(soup):
    """Extract text from heading tags."""
    return [heading.text.strip() for heading in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])]

def extract_text(soup):
    """Extract text from paragraph tags."""
    return [p.text.strip() for p in soup.find_all("p")]

def extract_links(soup):
    """Extract href attributes from anchor tags."""
    return [a["href"] for a in soup.find_all("a", href=True)]

def extract_emails(soup):
    """Extract emails from mailto: links and text patterns."""
    mailtos = [a["href"][7:] for a in soup.find_all("a", href=True) if a["href"].startswith("mailto:")]
    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    text = soup.get_text()
    emails_in_text = re.findall(email_pattern, text)
    return list(set(mailtos + emails_in_text))  # Remove duplicates

def extract_images(soup):
    """Extract src attributes from image tags."""
    return [img["src"] for img in soup.find_all("img", src=True)]

def extract_contacts(soup):
    """Extract phone numbers from text."""
    phone_pattern = r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b"  # Matches formats like 123-456-7890
    text = soup.get_text()
    return re.findall(phone_pattern, text)

# @app.post("/test")
# async def scrape(request: Request):
#     return {"message": "Test response"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)