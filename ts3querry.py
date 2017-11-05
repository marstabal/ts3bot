#TS3IO
import telnetlib
import stale
import kom
import odp
import czas
import ts3helper
import ts3event
import random
import ts3cmdhnd

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
        self.wyslij_linie(kom.QUIT)
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
        


class Query:
    
    InOut = None
    MojLog = None
    CmdHnd = None
    
    def __init__(self, _Log, _Host, _Port):
        _Log.pisz("Query - INIT")
        
        self.InOut = TS3IO(_Log, _Host, _Port)
        self.MojLog = _Log
        self.CmdHnd = ts3cmdhnd.CmdHandler(self.MojLog)
        czas.delay()
        
        
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
    
    def obsluz_odp(self, Timeout, Eventy):
        Odp = self.InOut.czytaj_linie()
        ClientID = -1
        ClientName = ""
        
        if(Odp != ""):
            if(kom.TIMEOUT in Odp):
                return True         #Dodac probe reconnecta
            if(kom.WYJDZ in Odp):
                return True
            if("invokername=Sever" in Odp):
                return False
            
            Podzial = Odp.split()
            
            for Chunk in Podzial:
                if kom.INVOKERID in Chunk:
                    ClientID = ts3helper.na_int(Chunk.replace(kom.INVOKERID, ""))
                if kom.INVOKER_NAME in Chunk:                          
                    ClientName = Chunk.replace(kom.INVOKER_NAME, "")

            for Chunk in Podzial:
                if kom.MSG in Chunk:
                    strHelp = self.CmdHnd.obsluz_komende(self, \
                                                         Chunk.replace(kom.MSG, ""), \
                                                         Eventy,\
                                                         ClientID,\
                                                         ClientName)
                    if not (strHelp is None) and strHelp != stale.STR_OK:
                        self.wiadomosc(strHelp)
                    czas.delay()
                    return False
                
        return False
    
    #wyslij wiadomosc globalna
    def wiadomosc(self, napis):
        self.MojLog.pisz("Serwer: " + napis)
        napisTS3 = ts3helper.na_ts3str(napis)
        self.InOut.wyslij_linie(kom.GLOB_MSG + napisTS3)
        self.olej_linie()
    
    def podaj_liste_uzytkownikow_online(self):
        ListaKlientow = []
        
        self.InOut.wyslij_linie(kom.LISTA_KLIENTOW)
        Odp = self.InOut.czytaj_linie()
        self.InOut.olej_linie()
        
        OdpSplit = Odp.split("|")
        
        for Linia in OdpSplit:
            Podzial = Linia.split()
        
            for Chunk in Podzial:

                if odp.NICKNAME in Chunk:
                    if stale.ADMIN in Chunk:
                        break
                        
                    ListaKlientow.append( \
                                    Chunk[len(odp.NICKNAME)+1:])
                    break
                    
        return ListaKlientow

    def podaj_liste_info_serwera(self):
        ListaInfo = []
        
        self.InOut.wyslij_linie(kom.INFO_SERWERA)
        Odp = self.InOut.czytaj_linie()
        self.InOut.olej_linie()
        
        OdpSplit = Odp.split()
        
        for InfoVar in OdpSplit:
            if("=" in InfoVar):
                ListaInfo.append(ts3helper.na_str(InfoVar))
                
        return ListaInfo
    
    def zmien_opis_klienta(self, ClientID, Opis):
        OpisTS3 = ts3helper.na_ts3str(Opis)
        
        self.InOut.wyslij_linie(kom.EDYTUJ_KLIENTA + kom.CLID + str(ClientID) + " " + kom.OPIS_KLIENTA + OpisTS3)
        self.InOut.olej_linie()
        czas.delay()
    
    def wycisz_klienta(self, ClientID):
        
        self.InOut.wyslij_linie(kom.EDYTUJ_KLIENTA + kom.CLID + str(ClientID) + " " + kom.CZY_MOZE_MOWIC + kom.NO)
        self.InOut.olej_linie()
        czas.delay()
        
    def odcisz_klienta(self, ClientID):
        self.InOut.wyslij_linie(kom.EDYTUJ_KLIENTA + kom.CLID + str(ClientID) + " " + kom.CZY_MOZE_MOWIC + kom.YES)
        self.InOut.olej_linie()
        czas.delay()
        
    def przenies_klienta(self, ClientID, ChannelID):
        self.InOut.wyslij_linie(kom.PRZENIES_KLIENTA + kom.CLID + str(ClientID) + " " + kom.CID + str(ChannelID))
        self.InOut.olej_linie()
        czas.delay()
        
    def olej_linie(self):
        self.InOut.olej_linie()
    
    def zakoncz(self):
        self.MojLog.pisz("Query - ZAKONCZENIE")
        self.InOut.zakoncz()
        