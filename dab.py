# -*- coding: utf-8 -*-

__author__ = 'boye'

import urllib2
import json
from willie import module

def get_elements(studio):
    valid_studio_values = ['studio', 'teknikerrom']

    studio = studio.strip().lower()

    if studio not in valid_studio_values:
        return False

    elements_url = urllib2.urlopen('http://pappagorg.radiorevolt.no/v1/sendinger/currentelements/' + studio)
    elements = json.load(elements_url)

    if elements['current']:
        current_class = elements['current']['class']

        if current_class == 'music':
            return 'Låt: {0} - {1}'.format(elements['current']['title'], elements['current']['artist'])
        elif current_class == 'audio':
            return 'Lydsak: {0}'.format(elements['current']['title'])
        elif current_class == 'promotion':
            return 'Jingle: {0}'.format(elements['current']['title'])
        else:
            return 'Unknown ({0}): {1}'.format(current_class, elements['current']['title'])
    elif elements['previous'] or elements['next']:
        return 'Stikk'

    return False


def has_elements(studio):
    valid_studio_values = ['studio', 'teknikerrom', 'autoavvikler']

    studio = studio.strip().lower()

    if studio not in valid_studio_values:
        return False

    elements_url = urllib2.urlopen('http://pappagorg.radiorevolt.no/v1/sendinger/currentelements/' + studio)
    elements = json.load(elements_url)

    return elements['current'] or elements['next'] or elements['previous']


def debug():
    elements_url = urllib2.urlopen('http://pappagorg.radiorevolt.no/v1/sendinger/currentelements/autoavvikler')
    elements = json.load(elements_url)

    warnings = list()

    if scheduled_replay():
        if not elements['current']:
            if elements['previous']:
                warnings.append('Reprisen i autoavvikler er for kort, og har sluttet!')
            else:
                warnings.append('Planlagt reprise i autoavvikler, men ingen elementer i autoavvikler!')
        elif elements['next']:
            warnings.append('Det ligger mer enn ett element i autoavvikler. Nå: {0}({1}), neste: {2}({3}'.format(
                elements['current']['title'], get_type(elements['current']['class']), elements['next']['title'],
                get_type(elements['next']['class'])))
        elif elements['previous']:
            warnings.append(
                'Det lå et element før gjelende element i autoavvikler. Nå: {0}({1}), forige: {2}({3}'.format(
                    elements['current']['title'], get_type(elements['current']['class']), elements['previous']['title'],
                    get_type(elements['previous']['class'])
                ))
    else:
        stuio = has_elements('studio')
        tekrom = has_elements('teknikerrom')
        if stuio:
            if elements['current'] or elements['prevous']:
                warnings.append('Ligger elementer i både autoavvikler og i studio.')
        if tekrom:
            if elements['current'] or elements['prevous']:
                warnings.append('Ligger elementer i både autoavvikler og i teknikerrom.')

        if not tekrom and not stuio:
            if elements['current']:
                warnings.append('Ser ut som noen har slunteret unna og lagt inn reprise.')
            if elements['next']:
                warnings.append('Det ligger mer enn ett element i autoavvikler. Nå: {0}({1}), neste: {2}({3}'.format(
                    elements['current']['title'], get_type(elements['current']['class']), elements['next']['title'],
                    get_type(elements['next']['class'])))
            if not elements['current']:
                if elements['previous']:
                    warnings.append(
                        'Det er ingen elementer som spiller noe sted! (det lå et i autoavvikler, men det stoppet)')
                else:
                    warnings.append('Det er inten elementer som spiller noe sted!')

    return warnings


def get_type(class_type):
    if class_type == 'music':
        return 'låt'
    if class_type == 'audio':
        return 'lyd'
    if class_type == 'promotion':
        return 'jingle'
    return 'ukjent'


def scheduled_replay():
    current_shows_url = urllib2.urlopen('http://pappagorg.radiorevolt.no/v1/sendinger/currentshows')
    current_shows_data = json.load(current_shows_url)

    return '(R)' in current_shows_data['current']['title']


def get_show():
    current_shows_url = urllib2.urlopen('http://pappagorg.radiorevolt.no/v1/sendinger/currentshows')
    current_shows_data = json.load(current_shows_url)

    show_end = current_shows_data['current']['endtime'].split(' ')[-1]
    show_start = current_shows_data['current']['starttime'].split(' ')[-1]
    show_now = current_shows_data['current']['title']
    show_next = current_shows_data['next']['title']

    return 'Nå: {0} ({1} - {2}), Neste: {3}'.format(show_now, show_start, show_end, show_next)

@module.commands('dab')
def dab(bot, trigger):
    """
    Viser hva som sendes akkurat nå.
    Gjør også en enkel feilsøking, og viser dersom den finner noe rart.
    """
    for warning in debug():
        bot.say(warning)
    if scheduled_replay():
        bot.say(get_show())
    else:
        bot.say(get_show())
        studio = get_elements('studio')
        tekrom = get_elements('teknikerrom')
        if studio:
            bot.say(studio + ' i studio 1.')
        elif tekrom:
            bot.say(tekrom + ' i teknikerrom.')
