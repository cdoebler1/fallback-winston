from mycroft.skills.core import FallbackSkill, intent_handler

from aiml import Kernel
from os import listdir, remove as remove_file
from os.path import dirname, isfile, join
from fnmatch import filter
import json


class WinstonFallback(FallbackSkill):

    def __init__(self):
        super(WinstonFallback, self).__init__(name='WinstonFallback')
        self.kernel = Kernel()
        chatbot = self.settings.get('chatbot_brain', 'Winston')
        chatbot_brain = chatbot + ".brn"
        chatbot_variables = chatbot + ".json"
        local = dirname(__file__)
        self.aiml_path = join(local, chatbot)
        self.brain_path = join(local, chatbot, chatbot_brain)
        self.variables_path = join(local, chatbot, chatbot_variables)
        self.brain_loaded = False

    def initialize(self):
        self.register_fallback(self.handle_fallback, 10)
        return

    def load_brain(self):
        """Set up the aiml engine using available device information."""
        self.log.info('Loading Brain')
        if isfile(self.brain_path):
            self.kernel.bootstrap(brainFile=self.brain_path)
        else:
            aimls = filter(listdir(self.aiml_path), "*.aiml")
            for aiml_file in aimls:
                self.kernel.learn(join(self.aiml_path, aiml_file))
            self.kernel.saveBrain(self.brain_path)

        with open(self.variables_path) as f:
            variables = json.load(f)

        for key, value in variables.items():
            self.kernel.setBotPredicate(key, value)

        self.brain_loaded = True
        return

    @intent_handler('reset.intent')
    def handle_reset_brain(self, message):
        """Delete the stored memory, effectively resetting the brain state."""
        self.log.debug('Deleting brain file')
        self.speak_dialog("reset")
        remove_file(self.brain_path)
        self.soft_reset_brain()
        return

    def ask_brain(self, utterance):
        """Send a query to the AIML brain. Saves the state to disk."""
        response = self.kernel.respond(utterance)
        self.kernel.saveBrain(self.brain_path)
        return response

    def soft_reset_brain(self):
        """Only reset the active kernel memory"""
        self.kernel.resetBrain()
        self.brain_loaded = False
        return

    def handle_fallback(self, message):
        """Mycroft fallback handler interfacing the AIML."""
        if self.settings.get("enabled"):
            if not self.brain_loaded:
                self.load_brain()
            utterance = message.data.get("utterance")
            answer = self.ask_brain(utterance)
            if answer != "":
                asked_question = False
                if answer.endswith("?"):
                    asked_question = True
                self.speak(answer, expect_response=asked_question)
                return True
        return False

    def shutdown(self):
        """Shut down any loaded brain."""
        if self.brain_loaded:
            self.kernel.saveBrain(self.brain_path)
            self.kernel.resetBrain()  # Manual remove
        self.remove_fallback(self.handle_fallback)
        super(WinstonFallback, self).shutdown()


def create_skill():
    return WinstonFallback()
