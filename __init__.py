from mycroft import MycroftSkill, intent_file_handler
from mycroft.skills.common_play_skill import CommonPlaySkill, CPSMatchLevel
from mycroft.skills.audioservice import AudioService
import requests

from .defaultstreams import getDefaultStreams
class RadioBob(CommonPlaySkill):
    def __init__(self):
        CommonPlaySkill.__init__(self)

    def checkUrl(self,url):
        checkedUrl = None

        self.log.debug("requested url = {}".format(url))

        r = requests.get(url,stream=True,timeout=5)

        self.log.debug("request status = {}".format(r.status_code))
        self.log.debug("returned url = {}".format(r.url))

        if (r.status_code == 200):
            checkedUrl = r.url

        r.close()
        return checkedUrl

    def initialize(self):
        STREAMS_FN = "streams.txt"
        self.audio_service = AudioService(self.bus)

        if not self.file_system.exists(STREAMS_FN):
            with self.file_system.open(STREAMS_FN, "w") as streams_file:
                streams_file.write(getDefaultStreams())
                streams_file.close()

        self.streams = {}
        with self.file_system.open(STREAMS_FN, "r") as streams_file:
            for entry in streams_file.readlines():
                values = entry.split(':',1)

                if len(values) == 2:
                    name = values[0].lower()
                    url = values[1].strip()

                    self.streams[name] = url
                    self.log.debug("adding {} stream. URL = {}".format(name, url))
                else:
                    self.log.warning("invalid entry {}".format(entry))
                
            streams_file.close()

        if len(self.streams) > 0:
            self.log.info("{} streams loaded".format(len(self.streams)))
        else:
            self.log.error("no streams loded, check streams.txt")


    def CPS_match_query_phrase(self, phrase):
        """ This method responds wether the skill can play the input phrase.

            The method is invoked by the PlayBackControlSkill.

            Returns: tuple (matched phrase(str),
                            match level(CPSMatchLevel),
                            optional data(dict))
                     or None if no match was found.
        """

        if phrase in self.streams:
            return (phrase,CPSMatchLevel.EXACT,self.streams[phrase])

        if self.voc_match(phrase,"bob.radio"):
            return (phrase,CPSMatchLevel.EXACT,self.streams["default"])

        return None

    def CPS_start(self, phrase, data):
        """ Starts playback.

            Called by the playback control skill to start playback if the
            skill is selected (has the best match level)
        """
        self.log.info("start playing {} stream from '{}'".format(phrase,data))
        self.speak_dialog('bob.radio')
        #self.audio_service.stop()

        url = self.checkUrl(data)
        if url != None:
            self.log.info("resolved URL: {}".format(url))
            self.audio_service.play(url)
        else:
            self.speak_dialog('bob.error')



def create_skill():
    return RadioBob()
