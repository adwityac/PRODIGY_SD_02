import requests
from bs4 import BeautifulSoup
import csv

# Define the URL of the website to scrape
url = 'http://books.toscrape.com/catalogue/page-1.html'

# Headers to mimic a browser visit
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
}

# Open a CSV file to save the data
with open('books.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Title', 'Price', 'Rating'])

    # Loop through multiple pages
    while True:
        # Send a GET request to the page
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all book elements on the page
        books = soup.find_all('article', class_='product_pod')

        # Extract data for each book
        for book in books:
            # Title
            title = book.h3.a['title']
            # Price
            price = book.find('p', class_='price_color').get_text(strip=True)
            # Rating (convert star rating text to numerical form)
            rating_text = book.find('p')['class'][1]
            rating_dict = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
            rating = rating_dict.get(rating_text, 0)

            # Write data to CSV
            writer.writerow([title, price, rating])

        # Find the link to the next page
        next_button = soup.find('li', class_='next')
        if next_button:
            # Update the URL to the next page
            url = 'http://books.toscrape.com/catalogue/' + next_button.a['href']
        else:
            # If no next button, break the loop
            break

print("Data has been written to books.csv")
