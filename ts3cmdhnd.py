#ts3cmdhnd
import kom
import usrkom
import ts3helper
import ts3event
import stale
import random
import czas
import datetime
from datetime import timedelta

STR_HELP_AFK = "Poprawna formula afk: !afk MM OPIS (MM - il. minut)"
STR_HELP_TEST = "Test dzialania"
STR_HELP_HELP = "Wpisz !help"
STR_HELP_KOSTKA = "Poprawna formula kostka: !kostka ## (gdzie ## - ilosc scian)"
STR_HELP_ODLICZ = "Poprawna formula odlicz: !odlicz ## opis (gdzie ## - ilosc sekund)"
STR_HELP_JJ = "Wpisz sama komende bez udziwnien :v"
STR_HELP_STD = "Standardowy tekst pomocy"

PODZIAL_LINKU="|||"

iloscNaboi = -1


def dajGlos_hnd(Query, KomSplit, Eventy, ClientID, ClientName):
    Query.wiadomosc("HauHau")
    return stale.STR_OK
    
def help_hnd(Query, KomSplit, Eventy, ClientID, ClientName):
    Query.wiadomosc("Dostepne komendy !dajGlos !Kostka " \
                    + "!afk !zw !brb !odlicz")
    Query.olej_linie()
    return stale.STR_OK
    
def kostka_hnd(Query, KomSplit, Eventy, ClientID, ClientName):
    Max = int(KomSplit[1])
    
    Query.wiadomosc("Los zdecydowal: " \
                    + str(random.randint(1, Max)))
    return stale.STR_OK
    
def afk_hnd(Query, KomSplit, Eventy, ClientID, ClientName):
    if ClientID == -1:
        return "BLAD! Niepoprawny numer klienta!"
    
    CzasPowrotu = (datetime.datetime.now() + datetime.timedelta(minutes=int(KomSplit[1]))).strftime("%H:%M")
    
    Query.zmien_opis_klienta(ClientID, "Jestem AFK do:   " \
                             +  CzasPowrotu \
                             + "     Opis: " + KomSplit[2])
    Query.wycisz_klienta(ClientID)
    Query.wiadomosc(ClientName + " jest AFK do " + CzasPowrotu) 
    return stale.STR_OK

def jj_hnd(Query, KomSplit, Eventy, ClientID, ClientName):
    if ClientID == -1:
        return "BLAD! Niepoprawny numer klienta!"
    
    Query.zmien_opis_klienta(ClientID, "Hehehe" )
    Query.odcisz_klienta(ClientID)
    
    Query.wiadomosc(ClientName + " powrocil!")

def random_link_hnd(Query, KomSplit, Eventy, ClientID, ClientName):
    plik = open("linki.txt")
    linki = plik.readlines()
    liczba = random.randint(0, len(linki))
    link = linki[liczba].replace("\n", "")
    info = ""
    
    if PODZIAL_LINKU in linki[liczba]:
        podzial = linki[liczba].split(PODZIAL_LINKU)
        link = podzial[0]
        if "H" in podzial[1]:
            info = info + "(Uwaga, glosne!)"
        if "C" in podzial[1]:
            info = info + "(zawiera sladowe ilosci kotow)"
        if "B" in podzial[1]:
            info = info + "(moze spowodowac smierc komorek mozgowych)"
    
    Query.wiadomosc("[url=" + link + "]Internety " + info + "[/url]")
    
def cycki_hnd(Query, KomSplit, Eventy, ClientID, ClientName):
    plik = open("cycki.txt")
    linki = plik.readlines()
    liczba = random.randint(0, len(linki))
    link = linki[liczba].replace("\n", "")

    Query.wiadomosc("[url=" + link + "]Cycki C:[/url]")
    
def odlicz_hnd(Query, KomSplit, Eventy, ClientID, ClientName):
    NowyEvent = ts3event.TS3_Event(float(KomSplit[1]), ts3event.event_Odliczanie, False, KomSplit[2])
    Eventy.dodaj_event(NowyEvent)
    return stale.STR_OK
    
def rosyjska_rul_hnd(Query, KomSplit, Eventy, ClientID, ClientName):
    global iloscNaboi
    iloscNaboi = iloscNaboi - 1
    if iloscNaboi <= 0:
        Query.wiadomosc("PIZD! " + ClientName + " trafia do kostnicy!")
        Query.przenies_klienta(ClientID, 10)
        przeladuj_hnd(Query, KomSplit, Eventy, ClientID, ClientName)
    else:
        Query.wiadomosc("KLIK! " + ClientName + " ma dzis szczescie.")
        
def przeladuj_hnd(Query, KomSplit, Eventy, ClientID, ClientName):
    global iloscNaboi
    iloscNaboi = random.randint(1,6)
    Query.wiadomosc("Rewolwer przeladowany!")
    
class Komenda:
    handler = None
    Keywords = None
    StrHelp = ""
    ListaPoprawnosc = ""
    
    
    def __init__(self, _handler, _keywords, _str_help, _lista_poprawnosc):
        self.handler = _handler
        self.Keywords = _keywords
        self.StrHelp = _str_help
        self.ListaPoprawnosc = _lista_poprawnosc
        
    def sprawdz_poprawnosc(self, komenda):
        Podzial = komenda.split()
        LenKom = len(Podzial)
        LenPopr = len(self.ListaPoprawnosc)
        if LenPopr + 1 != LenKom:
            return False
        
        if LenPopr == 0:
            return True
        
        for i in range(LenPopr):
            if self.ListaPoprawnosc[i] == "*":
                continue
            if self.ListaPoprawnosc[i] == "#":
                if not Podzial[i+1].isdigit():
                    return False
        
        return True
        

class CmdHandler:
    Komendy = None
    MojLog = None
    
    def __init__(self, _logger):
        global counter
        self.Komendy = self.uzupelnij_komendy()
        self.MojLog = _logger
        iloscNaboi = random.randint(1,6)
        
    def uzupelnij_komendy(self):
        KomList = []
        KomList.append(Komenda(dajGlos_hnd, [usrkom.dajGlos, usrkom.test], STR_HELP_TEST, []))
        KomList.append(Komenda(help_hnd, [usrkom.hilfe], STR_HELP_HELP, []))
        KomList.append(Komenda(kostka_hnd, [usrkom.kostka], STR_HELP_KOSTKA, ["#"]))
        KomList.append(Komenda(odlicz_hnd, [usrkom.odlicz], STR_HELP_ODLICZ, ["#", "*"]))
        KomList.append(Komenda(afk_hnd, [usrkom.afk, usrkom.zw], STR_HELP_AFK, ["#", "*"]))
        KomList.append(Komenda(jj_hnd, [usrkom.jj], STR_HELP_JJ, []))
        KomList.append(Komenda(random_link_hnd, [usrkom.randLink], STR_HELP_STD, []))
        KomList.append(Komenda(rosyjska_rul_hnd, [usrkom.rosyjska], STR_HELP_STD, []))
        KomList.append(Komenda(przeladuj_hnd, [usrkom.przeladuj], STR_HELP_STD, []))
        KomList.append(Komenda(cycki_hnd, [usrkom.cycki], STR_HELP_STD, []))        
        
        return KomList
        
    def obsluz_komende(self, Query, Komenda, Eventy, ClientID, ClientName):
        Komenda = ts3helper.na_str(Komenda)
        
        for KomVar in self.Komendy:
            for Key in KomVar.Keywords:
                if Key in Komenda:
                    if not KomVar.sprawdz_poprawnosc(Komenda):
                        return KomVar.StrHelp
                    
                    Podzial = Komenda.split()
                    return KomVar.handler(Query, Podzial, Eventy, ClientID, ClientName)
                
        return stale.STR_OK
