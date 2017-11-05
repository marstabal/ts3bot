import datetime
#import random
import stale
import kom
#import odp
import czas
from ts3querry import Query
from ts3logger import Logger
#from HTMLhandler import PlikHTMLHandler
from ts3event import TS3EventHnd


    #try:
    #Init
MojLog = Logger()
Eventy = TS3EventHnd(MojLog)
TS3 = Query(MojLog, stale.HOST, stale.PORT)
TS3.zaloguj(kom.LOGIN, kom.PASSY)

MojLog.pisz("Koniec inicjalizacji. Poczatek petli.")

while True:
    if(TS3.obsluz_odp(stale.TIMEOUT, Eventy)):
        break

    Eventy.sprawdz_eventy(TS3)
    czas.delay()

MojLog.pisz("Zwalnianie pamieci. Koniec programu.")
Query.wiadomosc("Wylaczanie Bota.")
TS3.zakoncz()
'''
except Exception as blad:
    ErrLog = open("errlog.txt", "a")
    if(not MojLog is None):
        MojLog.pisz("Napotkano blad!")
    print "ERR!"
    ErrLog.write(str(datetime.datetime.now()) \
                  + " - Napotkano blad! " \
                  + str(blad) \
                  + "\n"\
                  )
'''