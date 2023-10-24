from bs4 import BeautifulSoup
import urllib, json
import csv
import requests
import time


url = 'https://www.linkedin.com/jobs/collections/recommended/?currentJobId=2592651955'
# url = 'https://blockchain.info/rawaddr/12c6DSiU4Rq3P4ZxziKxzrL5LmMBrzjrJX'

response = requests.get(url)

# To let requests load
time.sleep(10)

# Use beautiful soup as content type is text/html instead of application/json
soup = BeautifulSoup(response.text, 'html.parser')  

if response.status_code == 200:
        # Check if response is not empty
        if response.text:
                content_type = response.headers.get('Content-Type', '')
                
                # If content type is application/json (Contains Valid JSON data)
                if 'application/json' in content_type:
                    data = response.json()
                    print(data)
                    
                # If content type is text/HTML
                else:
                    data = response.json()
                    
                    # tag and class are identified from inspecting the webpage
                    data = {
                        "company_name": soup.find('a', {'class':'app-aware-link '}).text,
                        "role": soup.find('h2', {'class':'t-24 t-bold job-details-jobs-unified-top-card__job-title'}).text,
                        "location": soup.find('span', {'class':'white-space-pre'}).text
                            # Add more keys as needed
                    }
                    
                    json_data = json.dumps(data)
                    print(json_data)
        else:
            print("Response is empty")
else:
         print(f"Failed to retrieve data. Status code: {response.status_code}")


# with urllib.request.urlopen('https://www.linkedin.com/jobs/collections/recommended/?currentJobId=3737301869') as url:
#     data = json.loads(url.read().decode())
#     print(data)




