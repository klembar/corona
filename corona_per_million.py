import functools
import itertools

import requests
#from matplotlib import pyplot
from collections import namedtuple
import matplotlib.pyplot as pl
import time
URL_BASE = "https://api.covid19api.com/total/country/"
SLEEP = 5 #tyle sekund odczeka skrypt gdy API powie że pytamy za często. Gdyby pojawił się znowu problem, możesz tą
# wartość zwiększyć np. do 5,

# mala "klasa" ktora ma pola name i country
Country = namedtuple("Country", ["name", "citizens"])


def confirmed_in_country(country_name: str):
    response = requests.get(URL_BASE + country_name)
    if response.status_code != 200: # zapytanie zakonczyło nie sie sukcesem (kod 200 oznacza sukces)
        print(f"Request failed, retrying after {SLEEP} seconds")
        time.sleep(SLEEP) # odczekaj kilka sekund
        response = requests.get(URL_BASE + country_name) # i wywolaj jeszcze raz to samo zapytanie
    response_json = response.json()
    confirmed = map(lambda day: day["Confirmed"], response_json)
    return list(confirmed)


def confirmed_per_million(country: Country):  # podalem typ zmiennej
    confirmed = confirmed_in_country(country.name)
    conf_per_mill = []
    for c in confirmed:
        conf_per_mill.append(c / country.citizens)
    return conf_per_mill

def deaths_in_country(country_name: str):
    response = requests.get(URL_BASE + country_name)
    if response.status_code != 200: # zapytanie zakonczyło nie sie sukcesem (kod 200 oznacza sukces)
        print(f"Request failed, retrying after {SLEEP} seconds")
        time.sleep(SLEEP) # odczekaj
        response = requests.get(URL_BASE + country_name) # i wywolaj jeszcze raz to samo zapytanie
    response_json = response.json()
    deaths = map(lambda day: day["Deaths"], response_json)
    return list(deaths)

def deaths_per_million(country: Country):  # podalem typ zmiennej
    deaths = deaths_in_country(country.name)
    deaths_per_mill = []
    for c in deaths:
        deaths_per_mill.append(c / country.citizens)
    return deaths_per_mill



def calculate_daily(country_name):
    poland = confirmed_in_country(country_name)
    diff = [j - i for i, j in zip(poland[:-1], poland[1:])]
    return list(diff)

def deaths_daily(country_name):
    deaths_poland = deaths_in_country(country_name)
    diff = [j - i for i, j in zip(deaths_poland[:-1], deaths_poland[1:])]
    return list(diff)
countries = [
    Country("germany", 83.0),
    Country("poland", 38.5),
    Country("italy", 60.4),
    #Country("sweden", 10.23),
    Country("france", 80.23),
    # Country("belgium", 11.46),
    Country("spain", 46.94),
]
fig, (countries_plot1, countries_plot) = pl.subplots(2)
fig.tight_layout(pad=2)  # odstep miedzy subplotami

for country in countries:
    countries_plot1.plot(confirmed_in_country(country.name), label=country.name)

countries_plot1.set_title("All confirmed cases")
countries_plot1.legend()


# rysowanie wykresow dla sumy przypadkow  w krajach
for country in countries:
    countries_plot.plot(confirmed_per_million(country), label=country.name)
countries_plot.set_title("Confirmed cases per million")
countries_plot.legend()


fig, (deaths_plot1, deaths_plot2) = pl.subplots(2)
fig.tight_layout(pad=2)  # odstep miedzy subplotami

for country in countries:
    deaths_plot1.plot(deaths_in_country(country.name), label=country.name)

deaths_plot1.set_title("All deaths cases")
deaths_plot1.legend()

for country in countries:
    deaths_plot2.plot(deaths_per_million(country), label=country.name)

deaths_plot2.set_title("Deaths cases per million")
deaths_plot2.legend()



fig, (daily_plot) = pl.subplots(1)
# rysowanie dziennych nowych przypadkow
daily = calculate_daily("poland")
daily_plot.set_title("Daily new cases")
x_axis = list(range(len(daily)))
daily_plot.bar(x_axis, daily, label="Poland")
daily_plot.legend()
pl.show()



#poniżej moje zabawy
# --------------------zachorowania w Polsce-------------------
zachorowania_pl=confirmed_in_country("poland")
deaths_pl = deaths_in_country("poland")
#deaths_per_mil_pl = deaths_per_million("poland")

zachorowanych6=zachorowania_pl[-6:]
zachorowanych1 = zachorowanych6[5]

zmarlych2 = deaths_pl[-2:]
zmarlych1 = zmarlych2[1]
zmarlych0 = zmarlych2[0]

# ------------------------------------------dzienne zachorowania----------------------
dzienne6=daily[-6:]
dzienne1=dzienne6[5]

srednia_zach=sum(daily[-6:-1])/5
# print(zachorowanych1)
# print(srednia_zach)

#------------------ofiary w Polsce----------------------------------------
deaths_daily_pl=deaths_daily("poland")
deaths_daily_pl6=deaths_daily_pl[-6:]

wczoraj_zmarlo = deaths_daily_pl6[5] #ile zmarło wczoraj
srednia_ofiar=int(sum(deaths_daily_pl6[-6:])/5)
#print(srednia_ofiar)

#print(deaths_daily_pl6)
#print(deaths_daily_pl6[5])




print('Sześć ostatnich dziennych zachorowań')
print(dzienne6)
print('                                                    ')
print('Sześć ostatnich dziennych ofiar')
print(deaths_daily_pl6)
print('                                                    ')
print('Liczba zachorowań do wczoraj wynosiła %d , a wczoraj zachorowało %d' % (zachorowanych1, dzienne1))
print('Średnia z poprzednich 5 dni wynośi %d, wygląda więc, że liczba dziennych zachorowań'% srednia_zach)
if srednia_zach > dzienne1:
    print('maleje')
elif srednia_zach==dzienne1:
    print('Nie zmienia się')
else:
    print('rośnie')


print('                                                    ')
print('Liczba wszystkich ofiar śmiertelnych wynosi %d , a wczoraj zmarło %d osób' % (zmarlych1,wczoraj_zmarlo))
print('Średnia ofiar śmiertelnych z poprzednich 5 dni wynośi %d, wygląda więc, że liczba dziennych ofiar'% srednia_ofiar)
if srednia_ofiar>wczoraj_zmarlo:
    print('maleje')
elif srednia_ofiar==wczoraj_zmarlo:
    print('Nie zmienia się')
else:
    print('Rośnie')

