#Import bib for å laste ned ting
import urllib.request
#Import bib for å kalkulere hash
import hashlib
#Add sqlite capability
import sqlite3

#Sites som skal fingerprintes. MÅ ha med http(s):// ellers klager python
sites = ['http://www.mareano.no/nyheter/nyheter-2018', 'http://www.npd.no']

#Åpne connection til sqlite3
sqlite_connection = sqlite3.connect('site_fingerprints.db')

for url in sites:
 #Åpne URL
 response = urllib.request.urlopen(url)
 #Les inn innholdet fra URL inn i variabelen data
 data = response.read()      # a `bytes` object
 
 #Beregn sha256 checksum og lagre som hex.
 #Denne ser ut som noe slik: 18e8606918705524af8f0c80b0ddb7cf0340038be8da79fccaa617b0c266f7ce
 m = hashlib.sha256(data).hexdigest()
 #Skriv ut checksumen
 print(m)
  
#Commit alle endringer
sqlite_connection.commit()

#Lukk sqlite connection
sqlite_connection.close()
