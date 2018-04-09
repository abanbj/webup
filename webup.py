#Import bib for å laste ned ting
import urllib.request
#Import bib for å kalkulere hash
import hashlib
#Add sqlite capability
import sqlite3
#Vi trenger også dato og klokkeslett
import datetime
#For å sjekke om databasefilen eksisterer
from pathlib import Path
#For å sjekke om fil eksisterer
import os

def hash(url_hash):
	response = urllib.request.urlopen(url_hash)
	data = response.read()
	m = hashlib.sha256(data).hexdigest()
	print(m)

#Sites som skal fingerprintes. MÅ ha med http(s):// ellers klager python
sites = ['http://www.mareano.no/nyheter/nyheter-2018', 'http://www.npd.no']

#Åpne connection til sqlite3.
db_navn = "site_fingerprints.db"

#Vi sletter databasefilen om den eksisterer
if os.path.exists(db_navn):
 os.remove(db_navn)

sqlite_connection = sqlite3.connect(db_navn)

dato_og_tid_naa = datetime.datetime.now()

#Lag en curser slik at vi kan kjøre SQL-kommandoer
c = sqlite_connection.cursor()

#Lag tabell
c.execute('CREATE TABLE webside (date text, url text, hash text)')

for url in sites:
 #Åpne URL
 response = urllib.request.urlopen(url)
 #Les inn innholdet fra URL inn i variabelen data
 data = response.read()      # a `bytes` object
 
 #Beregn sha256 checksum
 #Denne ser ut som noe slik: 18e8606918705524...
 m = hashlib.sha256(data).hexdigest()
 #Skriv ut dato og tid, url, og checksumen. Skriv også inn i databasen
 todo = [dato_og_tid_naa, url, m]
 c.execute("INSERT INTO webside VALUES (?,?,?)", todo)
 print("La inn hash fra ", url)

#Commit alle endringer til databasen
sqlite_connection.commit()

print("\n\nLooper nå gjennom og skriver innholdet ut fra databasen for å teste:")

for row in c.execute('SELECT * FROM webside'):
	print(row)

#Lukk sqlite connection
sqlite_connection.close()

#Vi kan komponere og sende epost direkte fra Python?!
