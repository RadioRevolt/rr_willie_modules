__author__ = 'boye'

import willie.module
import settings as s
from Icecast import IcecastServer


@willie.module.commands('lyttere')
def listeners(bot, trigger):
    """
    Viser antall lyttere på alle streamene våre.
    /revolt er nettstreamen
    /revolt_dab er streamen dedikert til SBS (den skal være 1, dersom den er 0 er vi av DAB)
    Alle andre er ikke så mye å bry seg om.
    """
    streamer = IcecastServer(s.ICECAST_NAME, s.ICECAST_URL, s.ICECAST_PORT, s.ICECAST_USERNAME, s.ICECAST_PASSWORD)
    s = list()
    
    for mount in streamer.Mounts:
        s.append(mount.Name + ': ' + str(len(mount.Listeners)))

    bot.say(' '.join(s))
