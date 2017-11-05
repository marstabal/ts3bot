#TS3IO
import telnetlib
import stale
import kom
import czas
import ts3event

class TS3IO:

    Serwer = None
    Log = None
    INIT_LINES = 2
    
    def __init__(self, _Log, _Host, _Port):
        _Log.pisz("TS3IO - INIT")
        
        self.Serwer = self.polacz(_Host, _Port)
        self.Log = _Log

        for x in xrange(self.INIT_LINES):
            self.czytaj_linie()
        
        
        czas.delay()

    def polacz(self, _Host, _Port):
        return telnetlib.Telnet(_Host, _Port)

    def zakoncz(self):
        self.wyslij_linie(kom.WYJDZ)
        self.czytaj_linie()

    def czytaj_linie(self):
        linia = self.Serwer.read_until(stale.NL, stale.TIMEOUT)
        if(len(linia) > 0):
            self.Log.pisz("<<:" + linia) 
        return linia

    def wyslij_linie(self, linia):
        self.Log.pisz(">>:" + linia)
        self.Serwer.write(linia + stale.NL)

    def olej_linie(self):
        self.Serwer.read_until(stale.NL, stale.TIMEOUT)
        
    def na_ts3str(self, napis):
        return napis.replace(" ", "\\s")

class Query:
    
    InOut = None
    MojLog = None
    ListaEventow = []
    
    def __init__(self, _Log, _Host, _Port):
        _Log.pisz("Query - INIT")
        
        self.InOut = TS3IO(_Log, _Host, _Port)
        self.MojLog = _Log
        self.inicjuj_eventy()
        
    def zaloguj(self, _Login, _Passwd):
        self.MojLog.pisz("Przygotowanie sesji")
        self.InOut.wyslij_linie(_Login + _Passwd)
        self.InOut.czytaj_linie()
        czas.delay()

        self.InOut.wyslij_linie(kom.USE)
        self.InOut.czytaj_linie()
        czas.delay()
    
        self.InOut.wyslij_linie(kom.POWIADOMIENIA_GLOB)
        self.InOut.czytaj_linie()
        czas.delay()
    
    def obsluz_odp(self, Timeout):
        Odp = self.InOut.czytaj_linie()
        
        if(Odp != ""):
            if(kom.TIMEOUT in Odp):
                return True         #Dodac probe reconnecta
            if(kom.WYJDZ in Odp):
                return True

            Podzial = Odp.split()
            for Chunk in Podzial:
                if kom.MSG in Chunk:
                    Temp = Chunk.replace(kom.MSG, "")
                    self.obsluz_komende(Temp)
                    czas.delay()
                    
        return False
    
    
    def zakoncz(self):
        self.MojLog.pisz("Query - ZAKONCZENIE")
        self.InOut.zakoncz()
    
    def obsluz_komende(self, komenda):
        
        if "!dajGlos" in komenda:
            self.InOut.wyslij_linie(kom.GLOB_MSG \
                                + "HauHau")
        if "!komendy" in komenda:
            self.InOut.wyslij_linie(kom.GLOB_MSG \
                                + "Dostepne\\skomendy\\s!dajGlos\\s!K6\\\s")
            self.InOut.czytaj_linie()
        if "!K6" in komenda:
            self.InOut.wyslij_linie(kom.GLOB_MSG \
                                + "Los\\szdecydowal\\s:\\s" \
                                + str(random.randint(1,6)))
        if "!afk" in komenda:
            self.InOut.wyslij_linie(kom.GLOB_MSG \
                                + "AFK")
    
    def inicjuj_eventy(self):
        self.MojLog.pisz("Query - INICJALIZACJA EVENTOW")
        EventHTML = ts3event.TS3_Event(3*czas.MIN, ts3event.event_HTML, True, "Tworzenie strony HTML")
        self.ListaEventow.append(EventHTML)
        
        EventMSG = ts3event.TS3_Event(czas.GODZ, ts3event.event_Info, True, "Cykliczna informacja globalna")
        self.ListaEventow.append(EventMSG)
        
    
    def sprawdz_eventy(self):
        
        if self.ListaEventow.count == 0:
            return
        
        for ObecnyEvent in self.ListaEventow:
            
            if ObecnyEvent.czy_przyszedl_czas():
                ObecnyEvent.przeprowadz_event(self.InOut)
                
                if not ObecnyEvent.CzyCykliczny:
                    self.ListaEventow.remove(ObecnyEvent)
                else:
                    ObecnyEvent.odnow_event()
        
             