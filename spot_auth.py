import time
import traceback
import spotipy
from spotipy import oauth2




class Spot_Auth:

	def __init__(self):
		self.spot_client_id = '603e7a3f35d24f7da37918e3021644b7'
		self.spot_client_secret = 'b257936f0cbe4d719691d02e2501ca8c'
		self.REDIRECT_URI = 'http://example.com'
		

	def engine(self):
		try:
			auth = oauth2.SpotifyOAuth(client_id=self.spot_client_id, client_secret=self.spot_client_secret, redirect_uri=self.REDIRECT_URI, scope="playlist-modify-public")
			response = auth.get_access_token()


		except:
			raise ConnectionError(response)
		else:
			try:
				TOKEN = response['access_token']
				with open('token.txt', 'w') as doc:
					doc.write(TOKEN)
				sp = spotipy.Spotify(TOKEN)
				user = sp.current_user()
				
			except:
				raise ConnectionRefusedError(traceback.format_exc())
			else:
				return response


class Spot_Search:

	
	def __init__(self, sdict):
		with open('token.txt', 'r') as file:
			token = file.read()
		self.token = token
		print(f'TOKEN > {self.token}')
		self.sp = spotipy.Spotify(self.token)
		self.user = self.sp.current_user()

		self.songs_list = sdict['songs_names']
		self.songs_art = sdict['songs_artists']
		self.data = sdict['data']

		self.year = int(self.data.split('-')[0])
		self.range_year = f'{(self.year - 3)}-{(self.year + 3)}'

		self.number_songs_not_finded = 0
		self.name_songs_not_finded = {}
		self.songs_uri = []

		self.search_status = False
		self.playlist_status = False

		self.search()


	def search(self):

		for track_name in self.songs_list:
			track_name1 = track_name.split('(')[0].replace("'", "").replace("/", " ")
			
			track_name1

			try:
				query = f'track:{track_name1} year:{str(self.year)}'
				result = self.sp.search(q=query, type='track', limit=1)
				song_uri_result = result['tracks']['items'][0]['uri']
				self.songs_uri.append(song_uri_result)
				print(f'>>{len(self.songs_uri)}%<<')

			except IndexError:
				try:
					ind = self.songs_list.index(track_name)
					track_artis = self.songs_art[ind].split('Featuring')[0]					
					query = f'track:{track_name1} artist:{track_artis} year:{str(self.range_year)}'
					result = self.sp.search(q=query, type='track', limit=1)
					song_uri_result = result['tracks']['items'][0]['uri']
					self.songs_uri.append(song_uri_result)
					print(f'>>{len(self.songs_uri)}%<<')

				except IndexError:
					try:
						
						new_q = f'track:{track_name1}'
						result = self.sp.search(q=new_q, type='track')
						song_uri_result = result['tracks']['items'][0]['uri']
						self.songs_uri.append(song_uri_result)
						print(f'>>{len(self.songs_uri)}%<<')
					except IndexError:
						self.name_songs_not_finded[track_name] = new_q
						self.number_songs_not_finded += 1
						print(f'>>{len(self.songs_uri)}%<<')

		self.search_status = True
		self.playlists(self.songs_uri)


	def playlists(self, slist):


		self.slist = slist
		self.sp = spotipy.Spotify(self.token)
		user_id = self.sp.me()['id']

		pl_name = f'The 100 BillBoard Hot Songs! From week of {self.data}.'
		pl_desc = f'Your 100 top (or almost of it!) songs from the past! Enjoy'
		created_playlist = self.sp.user_playlist_create(user=user_id, name=pl_name, description=pl_desc)

		time.sleep(1)

		pl_url = created_playlist['external_urls']['spotify']
		pl_id = created_playlist['id']


		self.sp.playlist_add_items(playlist_id=pl_id, items=self.slist)

		self.url = pl_url



		
