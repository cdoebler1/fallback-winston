# fallback-aiml
# Copyright (C) 2017  Mycroft AI
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import aiml
import os
from os import listdir, remove as remove_file
from os.path import dirname, isfile

# from mycroft.api import DeviceApi
from mycroft.skills.core import FallbackSkill
from mycroft.skills.core import intent_handler
from adapt.intent import IntentBuilder


class WinstonFallback(FallbackSkill):

    def __init__(self):
        super(WinstonFallback, self).__init__(name='WinstonFallback')
        self.kernel = aiml.Kernel()
        chatbot_brain = self.settings.get('chatbot_brain', 'AnnaL')
        self.aiml_path = os.path.join(dirname(__file__), chatbot_brain)
        self.brain_path = os.path.join(self.file_system.path,
                                       chatbot_brain+'.brn')
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
            aimls = listdir(self.aiml_path)
            for aiml_file in aimls:
                self.kernel.learn(os.path.join(self.aiml_path, aiml_file))
            self.kernel.saveBrain(self.brain_path)

        self.kernel.setBotPredicate("name", "Winston")
        self.kernel.setBotPredicate("species", "animatronic")
        self.kernel.setBotPredicate("genus", "Mycroft")
        self.kernel.setBotPredicate("family", "virtual personal assistant")
        self.kernel.setBotPredicate("order", "artificial intelligence")
        self.kernel.setBotPredicate("class", "computer program")
        self.kernel.setBotPredicate("kingdom", "machine")
        self.kernel.setBotPredicate("hometown", "Bellefonte")
        self.kernel.setBotPredicate("botmaster", "master")
        self.kernel.setBotPredicate("master", "the community")
        self.kernel.setBotPredicate("age", "1")
        self.kernel.setBotPredicate("location", "Bellefonte")
        self.kernel.setBotPredicate("sport", "boxing")
        self.kernel.setBotPredicate("favoritecolor", "green")
        self.kernel.setBotPredicate("birthday",  "November 6, 2019")
        self.kernel.setBotPredicate("birthplace", "Bellefonte, Pennsylvania")
        self.kernel.setBotPredicate("favoritefood", "tacos")
        self.kernel.setBotPredicate("favoritemovie", "War Games")
        self.brain_loaded = True
        return

    @intent_handler(IntentBuilder("ResetMemoryIntent").require("Reset")
                                                      .require("Memory"))
    def handle_reset_brain(self, message):
        """Delete the stored memory, effectively resetting the brain state."""
        self.log.debug('Deleting brain file')
        # delete the brain file and reset memory
        self.speak_dialog("reset.memory")
        remove_file(self.brain_path)
        self.soft_reset_brain()
        return

    def ask_brain(self, utterance):
        """Send a query to the AIML brain. Saves the state to disk."""
        response = self.kernel.respond(utterance)
        self.kernel.saveBrain(self.brain_path)
        return response

    def soft_reset_brain(self):
        # Only reset the active kernel memory
        self.kernel.resetBrain()
        self.brain_loaded = False
        return

    def handle_fallback(self, message):
        """Mycroft fallback handler interfacing the AIML.

        If enabled in home, this will parse a sentence and return answer from
        the AIML engine.
        """
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
