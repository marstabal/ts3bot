#ts3Event
from HTMLhandler import PlikHTMLHandler
from time import time
import kom
import czas

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
    
    
    
        
def event_HTML(serwer):
    PlikHTML = PlikHTMLHandler()
    PlikHTML.utworz_naglowek()

    #Tworzenie listy klientow online
    serwer.wyslij_linie(kom.LISTA_KLIENTOW)
    Odp = serwer.czytaj_linie()
    serwer.olej_linie()

    PlikHTML.utworz_liste_uzytkownikow_online(Odp)
    czas.delay()

    #Tworzenie listy informacji o serwerze

    serwer.wyslij_linie(kom.INFO_SERWERA)
    Odp = serwer.czytaj_linie()
    serwer.olej_linie()

    PlikHTML.utworz_liste_info_serwera(Odp)
    czas.delay()

    PlikHTML.utworz_stopke()
    
def event_Info(serwer):
    serwer.wyslij_linie(kom.WIADOMOSC + serwer.na_ts3str("Statystyki mozesz znalezc na www.blackys.pl/ts3.html"))
    serwer.olej_linie()
    