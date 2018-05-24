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
sites = [
'http://www.mareano.no/nyheter/nyheter-2018',
'http://www.npd.no',
'http://www.kystverket.no/Maritime-tjenester/Meldings--og-informasjonstjenester/AIS/',
'https://www.ogauthority.co.uk/data-centre/data-downloads-and-publications/seismic-data/',
'http://www.miljodirektoratet.no/no/Horinger/Petroleum/'
]

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
dato_og_tid_naa = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

for url in sites:
    #Skriv ut hvilken url som blir behandlet
    print("\033[36mJobber med URL: " + url + "\033[0;37;40m")
    #Finn ny hash til websiden. Denne må vi uansett ha
    new_hash = hash(url)
    #Finn gammel hash til siden
    sqlite_connection = sqlite3.connect(db_navn)
    c = sqlite_connection.cursor()
    query_oldhash = "SELECT hash FROM webside WHERE url='" + url + "' ORDER BY date DESC LIMIT 1"
    old_hash = c.execute(query_oldhash).fetchall()
    #print(old_hash)
    sqlite_connection.commit()
    sqlite_connection.close()

    #Dersom gammel hash eksisterer så sjekker vi mot ny
    if old_hash:
        sqlite_connection = sqlite3.connect(db_navn)
        c = sqlite_connection.cursor()
        print("Gammel hash funnet.")
        print("Query for aa hente gammel hash:", query_oldhash)
        old_hash = c.execute(query_oldhash).fetchall()
        sqlite_connection.commit()
        sqlite_connection.close()

        print("Gammel hash er: ", old_hash[0][0])
        #print("Her er old hash ")

        #Dette skal skje om hashen er ULIK
        if not (old_hash[0][0] == new_hash):

            sqlite_connection = sqlite3.connect(db_navn)
            c = sqlite_connection.cursor()
            todo = [dato_og_tid_naa, url, new_hash]
            c.execute("INSERT INTO webside VALUES (?,?,?)", todo)
            print("\033[32mOppdatert - ny hash er: " + new_hash, "\033[0;37;40m\n")
            sqlite_connection.commit()
            sqlite_connection.close()

            #Send epost om at ny hash ble funnet

            # Import smtplib for the actual sending function
            import smtplib

            # Import the email modules we'll need
            from email.mime.text import MIMEText

            # Open a plain text file for reading.  For this example, assume that
            # the text file contains only ASCII characters.
            #textfile="test.txt"
            #with open(textfile) as fp:
            # Create a text/plain message
            eposttekst = url + " har blitt oppdatert.\n\nNy/gammel hash er\n" + new_hash + "\n" + old_hash[0][0]
            msg = MIMEText(eposttekst)


            # me == the sender's email address
            # you == the recipient's email address
            msg['Subject'] = url + " er oppdatert"
            msg['From'] = "server@mail.mail"
            msg['To'] = "mail@mail.mail"
            # Send the message via our own SMTP server.
            s = smtplib.SMTP('localhost')
            s.send_message(msg)
            s.quit()


        else:
            print("\033[31mIkke oppdatert - gammel hash beholdes!\033[0;37;40m\n")

    else:
        print("Gammel hash ikke funnet.")
        sqlite_connection = sqlite3.connect(db_navn)
        c = sqlite_connection.cursor()
        todo = [dato_og_tid_naa, url, new_hash]
        c.execute("INSERT INTO webside VALUES (?,?,?)", todo)
        print("\033[32mFørste hash for " + url + " er " + new_hash + "\033[0;37;40m\n")
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
