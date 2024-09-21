from bs4 import BeautifulSoup
import requests

url = 'https://www.arcgis.com/home/item.html?id=b3489960c0e942c6985d2eca471718dd#data' # Replace with the actual URL
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

print(response.text)
# dgrid-row-table

# Find the table
# table = soup.find('table', {'id': 'dgrid_2-header'})

# Extract headers
# headers = [th.get_text() for th in table.find_all('th')]
# print("Headers:", headers)

# # Extract rows
# rows = []
# for row in table.find_all('tr')[1:]:  # Skip header row
#     columns = [td.get_text() for td in row.find_all('td')]
#     rows.append(columns)

# print("Rows:")
# for row in rows:
#     print(row)