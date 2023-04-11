import sys
import MeCab
import urllib.request
from bs4 import BeautifulSoup

r =  urllib.request.urlopen('https://cookpad.com/recipe/2221374')
html = r.read()
#print(html.decode())
soup = BeautifulSoup(html,'html.parser')
t = soup.get_text()
#print(t) 

m = MeCab.Tagger("-Ochasen")
a = m.parse(t)
words = [i.split()[0] for i in a.splitlines()]
print(words) 
