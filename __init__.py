from mycroft import MycroftSkill, intent_file_handler
from mycroft.skills.common_play_skill import CommonPlaySkill, CPSMatchLevel
from mycroft.skills.audioservice import AudioService
import requests

class RadioBob(CommonPlaySkill):
    def __init__(self):
        CommonPlaySkill.__init__(self)


    def checkUrl(self,url):
        url = None

        r = requests.get(url,stream=True,timeout=5)
        if (r.status_code == 200):
            url = r.url

        r.close()
        return url

    def initialize(self):
        self.audio_service = AudioService(self.bus)

        self.streams = {}
        with self.file_system.open("streams.txt", "r") as streams_file:
            for entry in streams_file.readlines():
                values = entry.split(':',1)

                if len(values) == 2:
                    name = values[0].lower()
                    url = values[1].strip()

                    self.streams[name] = url
                    self.log.debug("Adding {} stream. URL = {}".format(name, url))
                else:
                    self.log.warning("Invalid Entry {}".format(entry))
                
            streams_file.close()


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
        else:
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
        self.log.info("resolved URL: {}".format(url))
        self.audio_service.play(url)


def create_skill():
    return RadioBob()
