import kom
import stale
import odp
import czas


class PlikHTMLHandler:
    plik = None
    parametr = ["virtualserver_name", \
                "virtualserver_platform", \
                "virtualserver_version", \
                "virtualserver_clientsonline", \
                "virtualserver_uptime"]
    
    
    def __init__(self):
        self.plik = open("/var/www/html/ts3.html","w")
    
    def utworz_naglowek(self):
        self.plik.write("<HTML>" \
                        + "<HEAD>" \
                        + "<TITLE>" \
                        + "Dane TS3" \
                        + "</TITLE>" \
                        + "</HEAD>" \
                        + "<BODY>")

    def utworz_stopke(self):
        self.plik.write("</BODY>" \
                        + "</HTML>")

    def utworz_liste_uzytkownikow_online(self, ListaKlientow):
        self.plik.write("<h3>UZYTKOWNICY ONLINE:</h3><ul>")
        
        for Klient in ListaKlientow:
            self.plik.write("<li>" + Klient + "</li>")

        self.plik.write("</ul>")
		
    def utworz_liste_info_serwera(self, ListaInfo):

        self.plik.write("<h3>Informacje o serwerze</h3>")

        
        self.plik.write('<table>' \
                        + '<tr style="border:solid">' \
                        + '<th style="border:solid">Wlasciwosc</th>' \
                        + '<th style="border:solid">Wartosc</th></tr>')
        
        for InfoVar in ListaInfo:
            InfoSplit = InfoVar.split("=")
            if(InfoSplit[0] in self.parametr):

                self.plik.write('<tr style="border:solid">' \
                                + '<th>' \
                                + InfoSplit[0] 
                                + '</th><th>' 
                                + InfoSplit[1] + "</th></tr>")

        
        self.plik.write("</table>")

