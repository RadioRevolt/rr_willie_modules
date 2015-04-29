
__author__ = 'boye'

import urllib2
import json
from willie import module

URL = 'https://bruker.smint.no/search/index.php'

@module.commands('finn')
def search_user(bot, trigger):
    """
    Bukes til å søke etter personer i Studentmediene
    Du kan søke med navn, brukernavn, telefonnummer eller epost
    Viser maksimat 7 resultater
    """
    term = trigger.group(2).encode('utf-8')

    result = json.load(urllib2.urlopen(URL + '?s=' + urllib2.quote(term)))

    count = 0    

    for person in result:
        count += 1
        
        if count > 7:
            bot.say('Viser maks 7 resultater')
            break
        
        name = person['cn']
        if name is None:
            name = 'ukjent navn'

        username = person['uid']

        phone = person['tlf']
        if phone is None:
            phone = 'ukjent tlf.'

        mail = person['mail']
        if mail is None:
            mail = 'ukjent mail'

        bot.say(name + '(' + username + '): ' + phone + ' // ' + mail)
