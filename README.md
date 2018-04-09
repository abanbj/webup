webup - en util for å sjekke websider
=====================================
webup er en liten *utility* som skal hjelpe til med å finne ut om en websiden er
oppdatert. Dette gjør vi ved å beregne og sammenligne hash.

Skrevet i Python.

Et stort poeng med dette programmer er også å lære seg litt Python.Python er
tydeligvis veldig **populært** og **moderne**.

To-do
=====
Hash er nå kalkulert og lagt inn inn i databasen. Dersom hashen endres blir den nye hashen lagt inn (i tillegg til den gamle som forbli liggende - får da et arkiv). I tillegg

* Lag en fin grafisk unidiff som viser hva som er endret?
* Send epost! Alternativer
  * [sendemail](http://caspian.dotconf.net/menu/Software/SendEmail/)
  * mutt
  * Python sin innebygde måte å sende mail på?
