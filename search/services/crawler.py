import time
import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from search.models import Company

def crawl_google_maps(segment, city):
    print(f"Starting crawl for {segment} in {city}")
    
    chrome_options = Options()
    # chrome_options.add_argument("--headless") # Commented out headless for debugging if needed, but keeping it for now
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080") # specific window size might help
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    results = []
    try:
        query = f"{segment} in {city}"
        url = f"https://www.google.com/maps/search/{query}"
        driver.get(url)
        
        # Wait for the results feed to load
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='feed']"))
            )
        except:
            print("Could not find results feed. Maybe no results or blocked.")
            return []

        # Improved Scrolling Logic
        scrollable_div = driver.find_element(By.CSS_SELECTOR, "div[role='feed']")
        
        # scroll for a bit more time to load more results
        for _ in range(5): 
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
            time.sleep(2)
        
        # Find elements using a more broad selector or correct class
        # .Nv2PK is common, but let's try finding by role='article' or aria-label containing the company name logic
        # Another strong selector for result items is 'a' tags that wrap the result or the main container.
        
        # Taking a snapshot of items
        items = driver.find_elements(By.CSS_SELECTOR, "div.Nv2PK")
        print(f"Found {len(items)} items in the list.")
        
        for item in items:
            try:
                data = {
                    'name': '',
                    'phone': None,
                    'website': None,
                    'email': None,
                    'social_media': {}
                }
                
                # Extract Name
                # It's usually in a div with font-size larger or a specific class like qBF1Pd or hfpxzc (link)
                try:
                    # Generic strategy: first line of text or aria-label of the link
                    link_el = item.find_element(By.CSS_SELECTOR, "a")
                    data['name'] = link_el.get_attribute("aria-label")
                    if not data['name']:
                         data['name'] = item.text.split('\n')[0]
                except:
                    # Fallback
                    data['name'] = item.text.split('\n')[0] if item.text else "Unknown"

                # Extract Website from the list processing
                try:
                    # Look for website button in the list item
                    # Usually has data-value="Website" or is a link with text "Website"
                    website_link = item.find_element(By.CSS_SELECTOR, "a[data-value='Website']")
                    data['website'] = website_link.get_attribute("href")
                except:
                    pass

                # Extract Phone (often hard in list view without clicking)
                # Sometimes it's in the text.
                text_content = item.text
                # Simple regex for phone
                phone_match = re.search(r'(\(?\d{2}\)?\s)?\d{4,5}-\d{4}', text_content)
                if phone_match:
                    data['phone'] = phone_match.group(0)

                # Enrichment
                if data['website']:
                    print(f"Scraping website: {data['website']}")
                    email, socials = scrape_website(data['website'])
                    data['email'] = email
                    data['social_media'] = socials

                # Only save if we have at least a name
                if data['name']:
                    Company.objects.create(
                        name=data['name'],
                        segment=segment,
                        city=city,
                        phone=data['phone'],
                        website=data['website'],
                        email=data['email'],
                        social_media=data['social_media']
                    )
                    results.append(data)
                
            except Exception as e:
                print(f"Error processing item: {e}")
                continue
                
    except Exception as e:
        print(f"Crawler error: {e}")
    finally:
        driver.quit()
    
    return results

def scrape_website(url):
    email = None
    socials = {}
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Email
        mailto = soup.select_one('a[href^="mailto:"]')
        if mailto:
            email = mailto['href'].replace('mailto:', '')
        
        # Socials
        social_domains = ['facebook.com', 'instagram.com', 'linkedin.com', 'twitter.com', 'youtube.com']
        all_links = soup.find_all('a', href=True)
        for link in all_links:
            href = link['href']
            for domain in social_domains:
                if domain in href:
                    key = domain.split('.')[0]
                    socials[key] = href
                    
    except Exception as e:
        print(f"Website scrape error for {url}: {e}")
    
    return email, socials
