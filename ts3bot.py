import datetime
import random
import stale
import kom
import odp
import czas
from ts3querry import Query
from ts3logger import Logger
from HTMLhandler import PlikHTMLHandler

        
try:
    #Init
    MojLog = Logger()
    TS3 = Query(MojLog, stale.HOST, stale.PORT)
    czas.delay()
    TS3.zaloguj(kom.LOGIN, kom.PASSY)

    MojLog.pisz("URUCHAMIAM PETLE.")
    while True:
        if(TS3.obsluz_odp(stale.TIMEOUT)):
            break
            
        TS3.sprawdz_eventy()
        czas.delay()

    MojLog.pisz("Zamykam BOTa")
    TS3.zakoncz()

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
