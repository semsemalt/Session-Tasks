import json
import requests
import csv
import pandas as pd
from bs4 import BeautifulSoup




url_task = "https://docs.google.com/document/d/1C8Cw85v-mRJWKL5uFA1rmP2pdTXD25X_IAA4IXIdVmI/edit?tab=t.0#heading=h.lle0yaszf479"

url = "https://baraasalout.github.io/test.html"
response = requests.get(url) # 2- Send a GET request to the website >>> html text

#3 - Parse HTML content using BeautifulSoup
url_html = BeautifulSoup(response.content, 'html.parser')

#? 1. Extract text Data!
Extract_Text_Data = []

all_headers_1 = url_html.find_all('h1')
all_headers_2 = url_html.find_all('h2')
all_paragraphs = url_html.find_all('p')
all_list_items = url_html.find_all('li')


for header_1 in all_headers_1:
    Extract_Text_Data.append({"Type" : "Headers","Content": header_1.get_text()})

for header_2 in all_headers_2:
    Extract_Text_Data.append({"Type" : "Headers","Content": header_2.get_text()})

for paragraphs in all_paragraphs:
    Extract_Text_Data.append({"Type" : "Paragraphs","Content": paragraphs.get_text()})

for list_items in all_list_items:
    Extract_Text_Data.append({"Type" : "List Items","Content": list_items.get_text()})

with open("extract_text_data.csv", 'w', encoding = 'utf-8', newline = '') as f:
       writer = csv.DictWriter(f, fieldnames=["Type", "Content"])
       writer.writeheader()
       writer.writerows(Extract_Text_Data)

# !file1 = open("extract_text_data1.csv", 'w', encoding='utf-8', newline='')
# writer = csv.writer(file1)
# writer.writerow(['type', 'content'])

# for tag in all_headers_1:
#     writer.writerow(['Headers H1', tag.get_text()])

# for tag in all_headers_2:
#     writer.writerow(['Headers H2', tag.get_text()])

# for tag in all_paragraphs:
#     writer.writerow(['Paragraphs p', tag.get_text()])

# for tag in all_list_items:
#     writer.writerow(['List Items li', tag.get_text()])
# !file1.close()

# * Convert the CSV file to a DataFrame
# df = pd.read_csv("extract_text_data.csv")
# # Display the DataFrame
# print(df)
# # Save the DataFrame to a new CSV file
# df.to_csv("extract_text_data_final.csv", index=False, encoding='utf-8')



#? 2. Extract Table Data:

"https://www.pythontutorial.net/python-basics/python-write-csv-file/"
"https://www.geeksforgeeks.org/pandas/saving-a-pandas-dataframe-as-a-csv/"

table_rows = url_html.find_all('tr')
cleaned_rows = []
for table_row in table_rows:
     cleaned_rows.append(table_row.get_text().strip("\n").split("\n"))
# print(cleaned_rows)

with open("extract_table_data.csv", 'w', encoding='utf-8', newline='') as f:
     writer = csv.writer(f)
     writer.writerows(cleaned_rows)
#table_data = url_html.find('table').find_all('td')


#? 3. Extract Product Information (Cards Section):
# Extract data from the book cards at the bottom of the page, including:
    # Book Title.
    # Price.
    # Stock Availability.
    # Button text (e.g., "Add to basket").
# Save the data into a  books_data.JSON file.
"https://www.geeksforgeeks.org/how-to-convert-python-dictionary-to-json/"


book_products = url_html.find('div', class_ = 'book-products')
book_data = []
# print(book_products.find_all('p'))


for t,p,s,b in zip(book_products.find_all('strong'),
                   book_products.find_all('p', string=lambda text: "£" in text.lower()),
                     book_products.find_all('p', string=lambda text: "stock" in text.lower()),
                    book_products.find_all('button')):
         
         temp = {"Title":t.get_text(), "Price" : p.get_text(), "Stock" : s.get_text(), "Button_Text" : b.get_text() }
         book_data.append(temp)
# print(book_data)

with open("books_data.json", 'w', encoding= 'utf-8', newline='') as f:
    json.dump(book_data, f, indent=4, ensure_ascii=False)
    #dumps s string -> API

#? 4. Extract Form Details:
# Extract all input fields from the form, including:
    # Field name (e.g., username, password).
    # Input type (e.g., text, password, checkbox, etc.).
    # Default values, if any.
    # Save the data into a  JSON file.

form_details = url_html.find('form').find_all('input')
form_data = []
print("Form_details: ", form_details)

for inp in form_details:
    if inp.get('name') is not None:
        temp = {"Field Name: ": inp.get('name'), "Input Type: " : inp.get('type')}
        form_data.append(temp)
    else:
        temp = {"Field Name: ": "Button Submit", "Input Type: " : inp.get('type')}
        form_data.append(temp)

with open("Form_Details.json", 'w', encoding= 'utf-8', newline='') as f:
        json.dump(form_data, f, indent=4, ensure_ascii=False)


#? 5. Extract Links and Multimedia:
#Extract the video link from the <iframe> tag -> Save in json
iframe_link = url_html.find('iframe').get('src')
with open("Multimedia.json", 'w', encoding= 'utf-8', newline='') as f:
        json.dump(iframe_link, f, indent=4, ensure_ascii=False)


#? 6. Scraping Challenge:
# Students must write a script to extract data from the Featured Products section with the following requirements:
        # Product Name: Located within <span class="name">.
        # Hidden Price: Located within <span class="price">, which has style="display: none;".
        # Available Colors: Located within <span class="colors">.
        # Product ID: The value stored in the data-id attribute.
        # Example Output:
            # [  {'id': '101', 'name': 'Wireless Headphones', 'price': '$49.99', 'colors': 'Black, White, Blue'}, …, ]



raw_product_card = url_html.find_all('div', 'product-card')
print(raw_product_card)
Featured_Products_List = []
for data in raw_product_card:
     product_id = data.get("data-id")
     name = data.find('p', attrs={'class': 'name'}).get_text()
     price = data.find('p', attrs={'class': 'price'}).get_text()
     colors = data.find('p', attrs={'class': 'colors'}).get_text()
     Featured_Products_List.append({"ID": product_id, 
                                    "Name" : name,
                                    "Price" : price,
                                    "Colors" : colors})
    
print(Featured_Products_List)

with open("Featured_Products.json", 'w', encoding= 'utf-8', newline='') as f:
        json.dump(Featured_Products_List, f, indent=4, ensure_ascii=False)