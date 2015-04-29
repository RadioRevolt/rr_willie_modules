#Moduler skrevet for Radio Revolt

Willie ligger på hemingway. All moduler som legges i /home/boyebn/.willie/modules blir automatisk lastet inn når willie starter. Dersom du har lagt inn en ny modul må du restarte willie. Du kan stoppe willie med ``willie -q`` eller med ``kill <pid>`` (du finner pid'en til willie i /home/boyebn/.willie/willie.pid).

##dab.py
Bruk: ``.dab``

Sier hvilket program som går nå, og hvilket program som går etterpå. Dersom det ikke er en reprise som går sier den også hva som spilles akkurat nå (musikk, jingle, lydsak eller stikk), og hva den eventuelle låten heter o.l.

Utfører også en enkel sjekk av elementene i autoavvikler, og sier i fra dersom den finner noe mistenkelig. F.eks. at det ikke ligger elementer både i autoavvikler og i et av studioene i en live-slot (ikke planlagt reprise), at det ligger mer enn ett element i autoavvikler, at det ikke ligger elementer i hverken et av studioene eller i autoavvikler o.l. 

##listeners.py
Bruk: ``.lyttere``

Sier hvor mange lyttere det er på de ulike monteringspunktene i IceCast-serveren. De viktigste:

__/revolt__ - Dette er nettstreamen

__/revolt_dab__ - Dette er den dedikerte streamen til SBS. Det skal være akkurat én lytter der. Dersom det er 0 betyr det at SBS (de som sender streamen vår videre til Tyholt, slik at vi kommer på lufta) ikke lytter på streamen vår, og antagelig at vi ikke er på lufta.

##user_search.py
Bruk ``.finn <fritekst>``

Finner Navn, brukernavn, telefonnummer og epost til medlemmer i Studentmediene. Du kan søke etter både navn, brukernavn, telefonnummer og epost. Viser maksimalt syv resultater for å unngå "flooding" (se: http://en.wikipedia.org/wiki/Internet_Relay_Chat_flood)

