import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm  # Assuming you've imported tqdm elsewhere

id_count = ['1-100','101-200','201-300','301-400','401-500']

class ServantDatabase:
    def __init__(self):
        self.names = []
        self.ids = []
        self.rarities = []
        self.links = []

    def create_ServantDB_file(self):
        print('Collecting Servant name, ID, and Rarity')
        base_url = 'https://fategrandorder.fandom.com/wiki/Sub:Servant_List_by_ID/'

        for count in tqdm(id_count):
            url = f'{base_url}{count}'
            req = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(req.content, 'lxml')

            first = soup.find('div', {'id': 'mw-content-text'})
            f_rows = first.find_all('tr')[2:]

            for i in f_rows:
                data = i.find_all('td')
                self.names.append(data[2].text.strip())
                self.links.append(data[2].find('a').get('href').replace('/wiki/', ''))
                self.ids.append(data[0].text.strip())
                self.rarities.append(data[3].text.strip())

        corr_rarity = {'★ ★ ★': '3-Star', '★ ★ ★ ★ ★': '5-Star', '★ ★ ★ ★': '4-Star', '★ ★': '2-Star', '★': '1-Star', '—': '2-Star'}

        data = {'Servant Name': self.names, 'ID': self.ids, 'Rarity': self.rarities, 'Link':self.links}
        df = pd.DataFrame(data)

        # Remove non-playable servants
        df = df.query("ID not in ['83', '149', '151', '152', '168', '240', '333']")

        # Replace emoji-text rarities
        df['Rarity'] = df['Rarity'].replace(corr_rarity)

        # Create the CSV file
        #d_link = os.path.join(os.getcwd(), 'Total Servant Database.csv')
        d_link = os.path.join(os.getcwd(), 'Data_unfinished.csv')
        df.to_csv(d_link, index=False)
        print(f"Servant data saved to '{d_link}'")

# Assuming you have defined 'id_count' somewhere
servant_db = ServantDatabase()
servant_db.create_ServantDB_file()