#Needed libraries for web scrapping, data analysis and data visualization
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd 
import numpy as np


"""Step 1: Obtaining the data to work with. Using web scrapping methodologies"""


"""1.1: Utilizing Selenium to extract URLs from Sephora's Website for three selected categories: Body, Treatment, and Make-up"""


def load_browser(url):
    """
    Initialize the browser and load the given URL.
    
    Args:
        url (str): The URL to load in the browser.
    
    Returns:
        WebDriver: The initialized WebDriver instance.
    """
    driver = webdriver.Chrome() 
    driver.get(url)
    return driver

def click_see_more_button(driver, timeout=15):
    """
    Click on the 'See More Products' button if it is present.

    Args:
        driver (WebDriver): The WebDriver instance.
        timeout (int): The maximum time to wait for the button.
    
    Raises:
        Exception: If the button is not found or cannot be clicked.
    """
    try:
        see_more_button = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "see-more-button"))
        )
        ActionChains(driver).move_to_element(see_more_button).click(see_more_button).perform()
        time.sleep(3)  # Pause to allow initial loading of more products
    except Exception as e:
        print(f"'See More Products' button not found or could not be clicked: {e}")

def scroll_and_extract_urls(driver, max_products, scroll_pause_time=3):
    """
    Perform infinite scrolling to load all products and extract their URLs.

    Args:
        driver (WebDriver): The WebDriver instance.
        max_products (int): The expected number of products in the category.
        scroll_pause_time (int): Pause between scrolls to allow product loading.

    Returns:
        list: A list of extracted product URLs.
    """
    product_urls = []
    loaded_products = 0
    
    while loaded_products < max_products:
        # Scroll to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)  # Pause to allow loading of products

        # Extract product URLs
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        product_containers = soup.find_all('div', class_='product-tile')
        
        # Extract URLs and avoid duplicates
        for container in product_containers:
            link = container.find('a', class_='product-tile-link')
            if link and link.get('href'):
                url = link.get('href')
                if url not in product_urls:
                    product_urls.append(url)
        
        loaded_products = len(product_urls)
        print(f"Products loaded: {loaded_products}")

        # If no more products are loaded after a while, stop the loop
        if loaded_products >= max_products or scroll_pause_time > 60:
            print("Loading complete or product limit reached.")
            break
    
    return product_urls

def urls_to_dataframe(urls, filename='product_urls.csv'):
    """
    Convert a list of URLs into a DataFrame and save it to a CSV file.

    Args:
        urls (list): List of product URLs.
        filename (str): The name of the CSV file to save the URLs.

    Returns:
        pd.DataFrame: DataFrame containing the product URLs.
    """
    df = pd.DataFrame(urls, columns=['Product URL'])
    print("DataFrame output:")
    print(df)
    
    # Save the DataFrame to a CSV file
    df.to_csv(filename, index=False)
    return df


"""1.2: #### 1.2: Extracting Information with Beautiful Soup from URLs. Fields to obtain: category, subcategory, product name, brand name, rating, review count, price, and ingredients."""


# Headers to simulate a browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
}

# Function to extract product details from a given URL
def extract_product_info(url, index):
    """
    Extracts product details from a given Sephora product URL.
    
    Args:
        url (str): The URL of the product page to scrape.
        index (int): The index of the product in the list, used for tracking and logging.

    Returns:
        dict: A dictionary with product details (catogory, name, brand, rating, number of reviews, price, ingredients).
    """
    try:
        print(f"Extracting info for index: {index}")  # Display the index number
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract product details
        product_name = soup.find("span", class_="product-name product-name-bold").get_text(strip=True) if soup.find("span", class_="product-name product-name-bold") else "N/A"
        brand_name = soup.find("span", class_="brand-name", itemprop="name").get_text(strip=True) if soup.find("span", class_="brand-name", itemprop="name") else "N/A"
        rating = soup.find("span", itemprop="ratingValue").get_text(strip=True) if soup.find("span", itemprop="ratingValue") else "N/A"
        review_count = soup.find("meta", itemprop="reviewCount")['content'] if soup.find("meta", itemprop="reviewCount") else "N/A"
        price = soup.find("span", class_="price-sales price-sales-standard").get_text(strip=True) if soup.find("span", class_="price-sales price-sales-standard") else "N/A"
        ingredients = soup.find("div", class_="ingredients-content").get_text(strip=True) if soup.find("div", class_="ingredients-content") else "N/A"

        # Extract breadcrumb categories
        breadcrumb_elements = soup.find_all("div", class_="breadcrumb-element")
        categories = [element.get_text(strip=True) for element in breadcrumb_elements]

        # Separate categories
        subcategories = categories[0:3]
        while len(subcategories) < 3:
            subcategories.append("N/A")

        return {
            "subcategory1": subcategories[0],
            "subcategory2": subcategories[1],
            "subcategory3": subcategories[2],
            "product_name": product_name,
            "brand_name": brand_name,
            "rating": rating,
            "review_count": review_count,
            "price": price,
            "ingredients": ingredients,
            "product_url": url  # Move URL to the last position
        }
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return {
            "subcategory1": "Error",
            "subcategory2": "Error",
            "subcategory3": "Error",
            "product_name": "Error",
            "brand_name": "Error",
            "rating": "Error",
            "review_count": "Error",
            "price": "Error",
            "ingredients": "Error",
            "product_url": url  # Ensure the URL is present even on error
        }

# Function to scrape product information for all URLs in a DataFrame
def scrape_sephora_products(urls_df):
    """
    Iterates over a DataFrame of product URLs, extracts product information for each, 
    and returns a DataFrame of the collected data.
    
    Args:
        urls_df (pd.DataFrame): DataFrame containing a column 'Product URL' with the URLs to scrape.
    
    Returns:
        pd.DataFrame: DataFrame with product details for all URLs.
    """

    product_data = []
    for index, url in enumerate(urls_df['Product URL']):
        product_info = extract_product_info(url, index)  # Pass the index
        product_data.append(product_info)
    return pd.DataFrame(product_data)







