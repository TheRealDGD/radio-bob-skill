from mycroft import MycroftSkill, intent_file_handler


class RadioBob(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('bob.radio.intent')
    def handle_bob_radio(self, message):
        self.speak_dialog('bob.radio')


def create_skill():
    return RadioBob()

