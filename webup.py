#Import bib for å laste ned ting
import urllib.request
#Import bib for å kalkulere hash
import hashlib
#Add sqlite capability
import sqlite3
#Vi trenger også dato og klokkeslett
import datetime
#For å sjekke om fil eksisterer
import os

def hash(url_hash):
	response = urllib.request.urlopen(url_hash)
	data = response.read()
	m = hashlib.sha256(data).hexdigest()
	return m

#Sites som skal fingerprintes. MÅ ha med http(s):// ellers klager python
sites = ['http://www.mareano.no/nyheter/nyheter-2018',
'http://www.npd.no','http://www.kystverket.no/Maritime-tjenester/Meldings--og-informasjonstjenester/AIS/','https://www.ogauthority.co.uk/data-centre/data-downloads-and-publications/seismic-data/']

#Åpne connection til sqlite3.
#Først finn stien til skripttet og der databasen skal legges
sti_til_db = os.path.dirname(os.path.abspath(__file__))

#Print for å teste
#print(sti_til_db)
db_navn = sti_til_db + "/site_fingerprints.db"
#print ("Navn paa db er " + str(db_navn))

#Opprett forbindelse til database og opprett tabell om den ikke finnes fra før
sqlite_connection = sqlite3.connect(db_navn)
c = sqlite_connection.cursor()
c.execute('CREATE TABLE IF NOT EXISTS webside (date text, url text, hash text)')

#sqlite_connection = sqlite3.connect(db_navn)
dato_og_tid_naa = datetime.datetime.now()

for url in sites:
 #Finn gammel hash til siden
 sqlite_connection = sqlite3.connect(db_navn)
 c = sqlite_connection.cursor()
 query_oldhash = "SELECT hash FROM webside WHERE url='" + url + "' LIMIT 1"
 old_hash = c.execute(query_oldhash).fetchall()
 #print(old_hash)
 sqlite_connection.commit()
 sqlite_connection.close()

 #Dersom gammel hash eksisterer så sjekker vi mot ny
 if old_hash:
  sqlite_connection = sqlite3.connect(db_navn)
  c = sqlite_connection.cursor()
  print("Gammel hash for:", url, "funnet.")
  print("Query for aa hente gammel hash er:", query_oldhash)
  old_hash = c.execute(query_oldhash).fetchall()
  sqlite_connection.commit()
  sqlite_connection.close()
 
  print("Gammel hash er ", old_hash[0][0])
  #print("Her er old hash ")
  #Dette skal skje om hashen er ULIK
  if not (old_hash[0][0] == hash(url)):
 
   sqlite_connection = sqlite3.connect(db_navn)
   c = sqlite_connection.cursor()
   todo = [dato_og_tid_naa, url, hash(url)]
   c.execute("INSERT INTO webside VALUES (?,?,?)", todo)
   print("La inn hash fra ", url)
   sqlite_connection.commit()
   sqlite_connection.close()

 else:
  print("Gammel hash ikke funnet.")
  sqlite_connection = sqlite3.connect(db_navn)
  c = sqlite_connection.cursor()
  todo = [dato_og_tid_naa, url, hash(url)]
  c.execute("INSERT INTO webside VALUES (?,?,?)", todo)
  print("La inn hash fra ", url)
  sqlite_connection.commit()
  sqlite_connection.close()

#Commit alle endringer til databasen
#sqlite_connection.commit()

#sqlite_connection.close()

##Testseksjon - skriptet er egentlig ferdig med for å teste har vi ting liggende her

print("\n\nLooper naa gjennom og skriver innholdet ut fra databasen for aa teste:")

sqlite_connection = sqlite3.connect(db_navn)
c = sqlite_connection.cursor()

for row in c.execute('SELECT * FROM webside'):
	print(row)

#Lukk sqlite connection
sqlite_connection.close()

#Vi kan komponere og sende epost direkte fra Python?!
