#TS3LOGGER
import datetime



class Logger:
    
    plik = None

    def __init__(self):
        self.plik = open("log.txt", "a")
        self.plik.write("----------------\n")
        self.plik.write(str(datetime.datetime.now()) \
                         + " - Inicjalizacja\n")

    def pisz(self, napis):
        self.plik.write( \
                         str(datetime.datetime.now()) \
                         + " - " \
                         + napis \
                         + "\n" \
                         )
        print napis
