from bs4 import BeautifulSoup
import requests
from ballUn import getMatchStats


#section benchContainer class_="css-1ovb10-BenchesContainer elhbny511"

#getMatchStats('https://www.fotmob.com/match/3610249/matchfacts/arsenal-vs-brighton-&-hove-albion')

from FotMoby import FotMoby as fm

r_league = fm.getLeague()
print(r_league.json())