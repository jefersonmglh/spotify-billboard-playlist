from datetime import date

from billboard_scrap import *
from spot_auth import *
from logs import Log
import time
log = Log()


class Main:

    def __init__(self):


        self.today = date.today()
        self.day_str = self.today.strftime("%d-%m-%Y")

        log.info_m("app initiated ******************")
        self.init_message()

    def init_message(self):
        print('''
        >>WELCOME TO MUSIC TIME MACHINE!!!<<
        >>>Your App to find the 100 BillBoard Hot Musics from a time from your choice!<<<
        ''')

        print('''
        Please, insert the informations asked:
            ''')
        self.year = input('''
            >tell me the year you want to travel (format: "yyyy"): '''
                          )
        self.month = input('''
            >tell me the month (format: "mm"): '''
                           )
        self.day = input('''
            >tell a day(format: "dd"): '''
                         )
        self.date = f'{self.year}-{self.month}-{self.day}'

        log.info_m(f"input: {self.date} >> checking_input")
        self.check_input()

    def check_input(self):

        if len(self.date) != 10:
            print(
                '*******\n Please, tell the date like the example below: \nyear = 2000\nmonth = 01\nday = 01\n*******')
            log.info_m("len(input) =! 10")
            self.__init__()


        elif int(self.year) >= int(self.day_str.split('-')[2]):
            if int(self.month) >= int(self.day_str.split('-')[1]):
                print('******* Please, tell me a older date. *******')
                log.info_m("date not older than this month/year")
                self.__init__()
        else:
            self.search_instance()

    def search_instance(self):

        self.billboard_search = BillBoardSearch(self.date)
        print('''
        >Searching your songs from BillBoard DataBase
        >>>>>>>>loading<<<<<<<<<
            ''')
        log.info_m("initiating billboard search")

        self.songs_dict = self.billboard_search.souped_songs()

        if self.songs_dict != None  or len(self.songs_dict['songs_names']) > 90:
            print('''
                >SONGS FINDED!!             
                ''')
            log.info_m(f'{len(self.songs_dict["songs_names"])} songs scrapped')
            self.spotify_authentification()

        elif self.songs_dict == None or len(self.songs_dict['songs_names']) < 90:
            log.info_m(f'{len(self.songs_dict["songs_name"])} songs scrapped')
            print('''
            Bad Request from BillBoard Site :(
            Try Again Later. 
            ''')

    def spotify_authentification(self):
        log.info_m('initializing spot_auth_ob')
        self.auth = Spot_Auth()


        print('''
        >Initializing the authentification with Spotify.
        
        **You may need to authorize the app to make changes in your account**
        >a popup in your browser will appear in this case.

        >>>>>>>>loading<<<<<<<<<
            ''')

        try:
            i = self.auth.engine()

        except:
            log.info_m('authentification error')
            print('''
            Authentification Failed
            ''')
        else:
            log.info_m(f'authentification ok > {i}')
            print('''
            Searching your songs in Spotify API... <3
            
                ''')
            log.info_m('Auth OK!')
            self.getting_songs_uri()

    def getting_songs_uri(self):

        log.info_m('initializing spot_search_uri')

        spotify_search = Spot_Search(sdict = self.songs_dict)

        while spotify_search.search_status == False:
            time.sleep(1)

        print(f'{spotify_search.number_songs_not_finded}/100 songs were not finded in Spotify :(')
        print(f'>Creating the playlist and putting them into for you.\n>>>>>>>>>>>>>>>loading<<<<<<<<<<<<<<')

        time.sleep(2)


        print(f'''
			>Playlist Created!!!
			
			>link: {spotify_search.url}

			Enjoy!
			''')

















