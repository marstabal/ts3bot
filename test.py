from time import time


def czas_na_str(czas):
    dni = int(czas / (24 * 3600))
    godziny = int((czas - (dni*24*3600)) / 3600)
    minuty = int((czas - (dni*24*3600) - (godziny * 3600))/60)
    sekundy = int((czas - (dni*24*3600) - (godziny * 3600) - (minuty * 60)))
    return str(dni) + " dni, " \
         + str(godziny) + " godzin, " \
         + str(minuty) + " minut, " \
         + str(sekundy) + " sekund"

print(czas_na_str(65459))