# NMC Scraper

This project scrapes doctor details from the Nepal Medical Council (NMC) website and saves them into a JSON file.

## Directory Structure

```
/nmc_scraper
|-- /data
| |-- doctors_details.json
|-- /scripts
| |-- scrape_doctors.py
|-- requirements.txt
|-- README.md
```


## Prerequisites

- Python 3.x
- `requests` library
- `beautifulsoup4` library

Install the required libraries using:

```bash
pip install -r requirements.txt

```

## Usage

1. Navigate to the scripts directory:
```bash
cd scripts
```

2. Run the scraper script:
```bash
python scrape_doctors.py
```

3. The script will scrape the data and save it to data/doctors_details.json.