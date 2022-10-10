from bs4 import BeautifulSoup
import requests
from logs import Log
import traceback
log = Log()


class BillBoardSearch:

	def __init__(self, date):
		self.logs = Log()
		self.date = date
		self.URL = f'https://www.billboard.com/charts/hot-100/{self.date}'
		self.response = requests.get(self.URL)
		log.info_m(f'response: {self.response}')
		self.html = self.response.text

	def souped_songs(self):

		soup = BeautifulSoup(self.html, 'html.parser')
		try:
			soup_titles = soup.find_all(name="h3", class_="a-no-trucate")
			soup_artists = soup.find_all(name="span", class_="a-no-trucate")
			song_names = [heading.string.strip() for heading in soup_titles]
			song_artists = [heading.string.strip() for heading in soup_artists]
		except Exception:
			log.error_m(f"scrapping error >> {traceback.format_exc()}")
			print('an error has occurred')
			exit()
		else:
			songs_dict = {
				'songs_names': song_names,
				'songs_artists': song_artists,
				'data': self.date
			}
			return songs_dict
