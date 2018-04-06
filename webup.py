###
#Import bib for å laste ned ting
import urllib.request
import hashlib

url = 'http://npd.no'
response = urllib.request.urlopen(url)
data = response.read()      # a `bytes` object

#m = hashlib.sha256(data)
#m.update(data)
file = open("hashtest.txt", "r") as fil
print(hashlib.sha256(fil.read()).hexdigest())
#print(m.hexdigest())

#print(m.digest_size) #32
#print(m.block_size) #64
#print("H")
