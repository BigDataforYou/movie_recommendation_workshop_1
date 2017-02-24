from lxml import html
import requests

page = requests.get('http://www.filmsenzalimiti.co')
tree = html.fromstring(page.content)

generi = tree.xpath('//a[starts-with(@href, "http://www.filmsenzalimiti.co/genere/dvd-rip/")/@href')

