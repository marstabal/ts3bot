#ts3helper

def na_ts3str(napis):
    return napis.replace(" ", "\\s")

def na_str(ts3napis):
    return ts3napis.replace("\\s", " ")

def czas_na_str(czas):
    dni = int(czas / (24 * 3600))
    godziny = int((czas - (dni*24*3600)) / 3600)
    minuty = int((czas - (dni*24*3600) - (godziny * 3600))/60)
    sekundy = int((czas - (dni*24*3600) - (godziny * 3600) - (minuty * 60)))
    return str(dni) + " dni, " \
         + str(godziny) + " godzin, " \
         + str(minuty) + " minut, " \
         + str(sekundy) + " sekund"
            
def czy_liczba_calk(liczba):
    try:
        int(liczba)
        return True
    except ValueError:
        return False
    
def na_int(liczba):
    if czy_liczba_calk(liczba):
        return int(liczba)
    else:
        return -1