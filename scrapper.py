from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os
import json
import time

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run without UI
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")

# Initialize WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Website URL
website_url = "https://www.ycombinator.com/companies"
driver.get(website_url)

# Wait for the companies to load initially
wait = WebDriverWait(driver,30)
company_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "_company_1pgsr_355")))
print(f"Total Companies Found: {len(company_elements)}")  # Prints initial count

# Store extracted data

company_elements = []
last_count = 0
target_count = 4665  # Adjust based on your target count

# Continue scrolling until we reach the target count
while last_count < target_count:
    # Scroll to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)  # Wait for new elements to load

    # Find all company elements again after scroll
    new_elements = driver.find_elements(By.CLASS_NAME, "_company_1pgsr_355")
  

    for company in new_elements:
        try:
            href = company.get_attribute("href")
            if href:  # Check if href is not None or empty
                company_elements.append(href)
        except:
            continue
    
    last_count = len(company_elements)
    print(f"Total Companies Found After Scrolling: {last_count}")
  

json_filename = "yc.json"

# Check if JSON file exists and load existing data
if os.path.exists(json_filename):
    with open(json_filename, "r") as file:
        try:
            all_companies = json.load(file)
            if not isinstance(all_companies, list):  
                all_companies = []  # Ensure it's a list
        except json.JSONDecodeError:
            all_companies = []  # If file is empty or corrupt, start fresh
else:
    all_companies = []


# Now that we've ensured we've loaded enough companies, loop through them to scrape details
for company in company_elements: 

    driver.get(company)

    # Wait for page elements to load
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))


    elements = driver.find_elements(By.CLASS_NAME, "yc-tw-Pill")# new class
    try:
        batch = elements[0].text.strip() 
    except:
        batch  = "No batch available"

    try:
        company_type = elements[1].text.strip() 
    except:
        company_type = "No company type found"    

    try:
        industry_tags = elements[2].text.strip()  
    except:
       industry_tags= "No company tag  found"    



    try:
        name = driver.find_element(By.TAG_NAME, "h1").text.strip()  
    except:
        name = "No company name found"


    prose_elements = driver.find_elements(By.CLASS_NAME, "prose") # new class
    try:
        tagline  = prose_elements[0].text.strip()
    except:
        tagline = "No company tagline found"

    try:
        description = prose_elements[1].text.strip()
    except:
        description = "No company desc found"    


    try:
        website_url  = driver.find_element(By.CLASS_NAME, "group").text.strip()   

    except:
        website_url = "No company url found"   


    cards = driver.find_elements(By.CLASS_NAME, "ycdc-card-new")  # new class

    if cards:  # Ensure there's at least one card

        first_card = cards[0]  
        card_text = first_card.text.strip().split("\n")  
        
        # Extract specific details from text
        year_founded = card_text[card_text.index("Founded:") + 1] if "Founded:" in card_text else "Unknown"
        team_size = card_text[card_text.index("Team Size:") + 1] if "Team Size:" in card_text else "Unknown"
        location = card_text[card_text.index("Location:") + 1] if "Location:" in card_text else "Unknown"
        
        # Extract social links
        social_links = {}
        links = first_card.find_elements(By.TAG_NAME, "a")
        
        for link in links:
            href = link.get_attribute("href")
            if "linkedin" in href:
                social_links["linkedin"] = href
            elif "twitter" in href:
                social_links["twitter"] = href
            elif "facebook" in href:
                social_links["facebook"] = href
            elif "crunchbase" in href:
                social_links["crunchbase"] = href
    
    
    # Store results
    company = {
        "name": name,
        "tagline": tagline,
        "description":description,
        "batch": batch,
        "company_type":company_type,
        "industry_tags":industry_tags,
        "location": location,
        "website": website_url,
        "founded": year_founded,
        "team_size": team_size,
        "social_profiles": social_links,
        
    }

    founders=[]
    if len(cards) > 1:  
        for index, card in enumerate(cards[1:], start=0):  
            card_text = card.text.strip().split("\n") 
            name = card_text[0] if card_text else "No name found"  

            # Extract all anchor tags (URLs)
            links = [a.get_attribute("href") for a in card.find_elements(By.TAG_NAME, "a")]

            # Initialize LinkedIn & Twitter URLs as empty
            linkedin_url = twitter_url = "Not found"

            # Check each URL and categorize
            for link in links:
                if "linkedin.com" in link:
                    linkedin_url = link
                elif "twitter.com" in link:
                    twitter_url = link

            founders.append({index : {
                "name": name,
                "linkedin_profile": linkedin_url,
                "twitter_profile": twitter_url
            }})

    all_companies.append({"company": company, "founders": founders})    
    with open(json_filename, "w") as file:
        json.dump(all_companies, file, indent=4)
    
    print(json.dumps(all_companies, indent=4))  # Optional for debugging
    total_companies = len(all_companies)
    print(f"Total number of companies: {total_companies}")

    
driver.quit()

