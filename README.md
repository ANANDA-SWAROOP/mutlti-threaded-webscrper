
---

# Multi-Threaded WebScrapper with GUI

A multithreaded web scraping tool built with Python and JavaScript, featuring a graphical user interface (GUI) for extracting specific data from websites. This project demonstrates the power of multithreading for efficient data extraction and provides an intuitive interface for users to interact with the scraper.

## Features

- **Data Extraction**: Selectively scrape the following data types from a given URL:
  - **Headings**: Text from `<h1>` to `<h6>` tags.
  - **Text**: Text from `<p>` tags.
  - **Links**: `href` attributes from `<a>` tags.
  - **Emails**: Email addresses from `mailto:` links and text patterns.
  - **Images**: `src` attributes from `<img>` tags (photos, images, logos).
  - **Contacts**: Phone numbers extracted from text.
- **Multithreading**: Utilizes concurrent threads to extract different data types simultaneously, improving performance and efficiency.
- **User-Friendly GUI**: A simple web-based interface allows users to input a URL, select data types via checkboxes, and view results without needing command-line knowledge.
- **Tech Stack**: 
  - **Backend**: Python with FastAPI and BeautifulSoup.
  - **Frontend**: HTML and vanilla JavaScript.

## Setup

### Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

### Installation

1. **Download the Project Files**: 
   - Ensure you have the following files in your project directory:
     - `app.py` (backend code)
     - `index.html` (frontend GUI)

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment**:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install Dependencies**:
   ```bash
   pip install fastapi uvicorn requests beautifulsoup4
   ```

5. **Run the FastAPI Server**:
   ```bash
   uvicorn app:app --host 127.0.0.1 --port 8000 --reload
   ```
   - The `--reload` flag enables auto-reloading for development purposes.

## Usage

1. **Access the GUI**:
   - Open your web browser and navigate to `http://127.0.0.1:8000`.

2. **Scrape a Website**:
   - Enter the URL of the website you want to scrape (e.g., `https://example.com`).
   - Select the types of data you wish to extract using the checkboxes (e.g., Headings, Links, Emails).
   - Click the "Scrape" button.

3. **View Results**:
   - The extracted data will be displayed below the form, organized by data type.
   - If no data is found for a selected type, a "No data found" message will be shown.

## How It Works

- **Frontend**: 
  - An HTML form collects the URL and selected data types.
  - JavaScript sends a POST request to the backend with the user inputs using the Fetch API.
  - Results are dynamically displayed on the page.

- **Backend**:
  - A FastAPI server receives the POST request and fetches the webpage using `requests`.
  - The HTML is parsed with BeautifulSoup.
  - A `ThreadPoolExecutor` is used to extract the selected data types concurrently, with each data type processed in a separate thread.
  - The extracted data is returned as a JSON response and displayed in the GUI.

- **Multithreading**:
  - By using multithreading, the scraper can overlap the extraction of different data types, making the process faster and more efficient, especially for large webpages.

## Limitations

- **Single-Page Scraping**: The tool is designed to scrape data from a single webpage and does not follow links to other pages.
- **Ethical Considerations**: Always ensure that your scraping activities comply with the website's terms of service and respect `robots.txt` guidelines. This tool is intended for educational purposes and responsible use.

## Contributing

Contributions are welcome! If you encounter any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License.

---
