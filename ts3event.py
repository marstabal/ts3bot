#ts3Event
from HTMLhandler import PlikHTMLHandler
from time import time
import kom
import czas
import ts3helper

class TS3_Event:
    Utworzono = 0.0
    CzasRealizacji = 0.0
    Opis = ""
    CzyCykliczny = False
    Interwal = 0.0
    
    przeprowadz_event = None
    
    
    def __init__(self, _Interwal, _Metoda, _CzyCykl, _Opis):
        self.Utworzono = time()
        self.CzasRealizacji = self.Utworzono + _Interwal
        self.przeprowadz_event = _Metoda
        self.CzyCykliczny = _CzyCykl
        self.Interwal = _Interwal
        self.Opis = _Opis
    
    def czy_przyszedl_czas(self):
        return time() > self.CzasRealizacji
    
    def odnow_event(self):
        self.CzasRealizacji = time() + self.Interwal
    
    
    
class TS3EventHnd:
    ListaEventow = []
    MojLog = None
    
    def __init__(self, _log):
        self.MojLog = _log
        self.MojLog.pisz("Query - INICJALIZACJA EVENTOW")
        
        EventHTML = TS3_Event(3*czas.MIN, event_HTML, True, "Tworzenie strony HTML")
        self.ListaEventow.append(EventHTML)
        
        EventMSG = TS3_Event(czas.GODZ, event_Info, True, "Cykliczna informacja globalna")
        self.ListaEventow.append(EventMSG)
        
    def sprawdz_eventy(self, TS3):
        
        if self.ListaEventow.count == 0:
            return
        
        for ObecnyEvent in self.ListaEventow:
            
            if ObecnyEvent.czy_przyszedl_czas():
                ObecnyEvent.przeprowadz_event(ObecnyEvent, TS3)
                
                if not ObecnyEvent.CzyCykliczny:
                    self.ListaEventow.remove(ObecnyEvent)
                else:
                    ObecnyEvent.odnow_event()

    def dodaj_event(self, Event):
        self.ListaEventow.append(Event)


def event_HTML(Event, Query):
    PlikHTML = PlikHTMLHandler()
    PlikHTML.utworz_naglowek()

    #Tworzenie listy klientow online
    ListaKlientow = Query.podaj_liste_uzytkownikow_online()
    PlikHTML.utworz_liste_uzytkownikow_online(ListaKlientow)
    czas.delay()

    #Tworzenie listy informacji o serwerze
    ListaInfo = Query.podaj_liste_info_serwera()
    PlikHTML.utworz_liste_info_serwera(ListaInfo)
    czas.delay()

    PlikHTML.utworz_stopke()
    
def event_Info(Event, Query):
    Query.wiadomosc("Statystyki mozesz znalezc na www.blackys.pl/ts3.html")
    Query.olej_linie()
    
def event_Odliczanie(Event, Query):
    Query.wiadomosc(Event.Opis)
    Query.olej_linie()