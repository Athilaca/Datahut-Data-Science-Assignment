# Web Scraping with Selenium

This project scrapes company details  and founders from Y Combinator's website using Selenium and stores the data in a JSON file.


## Setup Instructions

### 1. Create and Activate a Virtual Environment

#### On Windows:
```sh
python -m venv venv
venv\Scripts\activate
```

#### On macOS/Linux:
```sh
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

Ensure you have the required dependencies installed by running:
```sh
pip install -r requirements.txt
```

### 3. Run the Web Scraper

Execute the following command to start scraping:
```sh
python scraper.py
```

## How the Script Works

1. The script sets up a Selenium WebDriver using `webdriver-manager`.
2. It navigates to the Y Combinator website and loads company details.
3. It scrolls down the page to load more results until a target number is reached.
4. It extracts key details such as name, batch, company type, industry tags, location, website, and founder details.
5. The data is saved to a `yc.json` file.
6. If `yc.json` already exists, it loads and appends new data to it.

## Output

The scraped data is stored in `yc.json` in the following format:

```json
[
    {
        "company": {
            "name": "Example Company",
            "tagline": "Innovative Solutions",
            "description": "A company focused on AI-driven analytics.",
            "batch": "W21",
            "company_type": "B2B",
            "industry_tags": "AI, Analytics",
            "location": "San Francisco, CA",
            "website": "https://example.com",
            "founded": "2021",
            "team_size": "50",
            "social_profiles": {
                "linkedin": "https://linkedin.com/example",
                "twitter": "https://twitter.com/example"
            }
        },
        "founders": {
            "0": {
                "name": "John Doe",
                "linkedin_profile": "https://linkedin.com/in/johndoe",
                "twitter_profile": "https://twitter.com/johndoe"
            }
        }
    }
]
```

## Troubleshooting

- If ChromeDriver issues occur, ensure your Chrome browser is up to date.
- Run `pip install --upgrade webdriver-manager` if needed.
- Ensure pop-up blockers or security software aren’t interfering with Selenium.



This project is licensed under the MIT License.

