from bs4 import BeautifulSoup
import urllib, json
import csv
import requests
import time
import openai

openai.api_key = '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'

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
                    # data = response.json()
                    
                    company_name = soup.find('a', {'class':'app-aware-link '}).text
                    position = soup.find('h2', {'class':'t-24 t-bold job-details-jobs-unified-top-card__job-title'}).text
                    location = soup.find('span', {'class':'white-space-pre'}).text
        
                    description_section = soup.find('div', class_='description__text description__text--rich')
                    
                    #Create array to store technologies
                    technologies = []
                    
                    if description_section:
                        #Get description information
                        description_text = description_section.text

                        
                        openAI_response = openai.Completion.create(
                            engine="text-davinci-002",
                            prompt = description_text,
                            max_tokens=50, 
                            temperature=0.7, 
                            n = 1
                        )
                        
                        #to extract information from OpenAi response
                        generated_text = response.choices[0].text
                        
                        # Extract technologies from generated_text
                        potential_technologies = ["Python", "Java", "C++", "JavaScript", "iOS", "Swift", "Android", "React", "Node.js"]
                        techs_in_description = [tech for tech in potential_technologies if tech in generated_text]

                        technologies.extend(techs_in_description)
                        
                        # Remove duplicates in list
                        unique_technologies = list(set(technologies))
                                
                    job_info = {
                        "company_name": company_name,
                        "position": position,
                        "location": location,
                        "technologies": unique_technologies
                    }
                    
                    job_data = []
                    job_data.append(job_info)
                    
                    
                    json_data = json.dumps(job_data)
                    print(json_data)
        else:
            print("Response is empty")
else:
         print(f"Failed to retrieve data. Status code: {response.status_code}")


# with urllib.request.urlopen('https://www.linkedin.com/jobs/collections/recommended/?currentJobId=3737301869') as url:
#     data = json.loads(url.read().decode())
#     print(data)