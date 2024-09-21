import requests

# Define the API endpoint
url = "https://www.fema.gov/api/open/v2/FimaNfipClaims"

# Make a GET request to the API
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()
    print(data["FimaNfipClaims"][0])  # Display the data
else:
    print(f"Error: {response.status_code}")