#Import bib for å laste ned ting
import urllib.request
#Import bib for å kalkulere hash
import hashlib

#Velg URL som skal behandles
url = 'http://www.mareano.no/nyheter/nyheter-2018'
#Åpne URL
response = urllib.request.urlopen(url)
#Les inn innholdet fra URL inn i variabelen data
data = response.read()      # a `bytes` object

#Beregn sha256 checksum og lagre som hex.
#Denne ser ut som noe slik: 18e8606918705524af8f0c80b0ddb7cf0340038be8da79fccaa617b0c266f7ce
m = hashlib.sha256(data).hexdigest()
#Skriv ut checksumen
print(m)
