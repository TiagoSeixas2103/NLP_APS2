import os
import pandas as pd
import requests
from bs4 import BeautifulSoup

class ServantDescriptions:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.servant_data = pd.read_csv(csv_path)
        self.descriptions = []

    def scrape_servant_descriptions(self):
        base_url = 'https://fategrandorder.fandom.com/wiki/'

        for index, row in self.servant_data.iterrows():
            servant_name = row['Link']
            print(servant_name)
            url = f'{base_url}{servant_name}'
            req = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(req.content, 'lxml')
            
            # Find the fourth <p> tag (change index if needed)
            #description = soup.find_all('table')[29].text.strip()
            #print(description)
            servant_exceptions = {"Mashu Kyrielight" : "Mashu Kyrielight"}
            servant_description = "None"
            if servant_name not in servant_exceptions:
                description = soup.find_all('table')
                i = 0
                for table in description:
                    tr_list = table.find_all('tr')
                    tr = tr_list[0]
                    th_list = tr.find_all('th')
                    if len(th_list) > 1:
                        th = th_list[1]
                        if th.text.strip()=="Description":
                            servant_description = table.text.strip()                       

            self.descriptions.append(servant_description)

        # Add a new column to the DataFrame
        self.servant_data['Description'] = self.descriptions

        return self.servant_data

# Specify the path to your existing CSV file
csv_file_path = 'Data_unfinished.csv'

# Create an instance of the ServantDescriptions class
servant_desc = ServantDescriptions(csv_file_path)

# Scrape the descriptions and update the DataFrame
updated_df = servant_desc.scrape_servant_descriptions()

# Save the updated DataFrame to a new CSV file
updated_csv_path = os.path.join(os.getcwd(), 'Data.csv')
updated_df.to_csv(updated_csv_path, index=False)
print(f"Servant data with descriptions saved to '{updated_csv_path}'")