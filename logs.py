import logging
import traceback


class Log:

    def __int__(self):
       logging.basicConfig(filename='log.txt', 
            level=logging.DEBUG, encoding='utf-8', 
            format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')


    def info_m(self, msg):
        logging.info(msg)

    def error_m(self, erro):
        logging.error(erro)


