import aiml
import os
from os import listdir
from os.path import dirname, isfile

kernel = aiml.Kernel()

chatbot_brain = "AnnaL"

aiml_path = os.path.join(dirname(__file__), chatbot_brain)
brain_path = os.path.join(dirname(__file__), 'brain/' + chatbot_brain + '.brn')
if isfile(brain_path):
    kernel.bootstrap(brainFile=brain_path)
else:
    aimls = listdir(aiml_path)
    for aiml_file in aimls:
        kernel.learn(os.path.join(aiml_path, aiml_file))
    kernel.saveBrain(brain_path)

kernel.setBotPredicate("name", "Winston")
kernel.setBotPredicate("species", "Feral Cat Robotics Animatronic")
kernel.setBotPredicate("genus", "Mycroft")
kernel.setBotPredicate("family", "virtual personal assistant")
kernel.setBotPredicate("order", "artificial intelligence")
kernel.setBotPredicate("class", "computer program")
kernel.setBotPredicate("kingdom", "machine")
kernel.setBotPredicate("hometown", "Bellefonte")
kernel.setBotPredicate("botmaster", "master")
kernel.setBotPredicate("master", "the community")
kernel.setBotPredicate("age", "20")

kernel.saveBrain(brain_path)

# Press CTRL-C to break this loop
while True:
    print(kernel.respond(input("Enter your message >> ")))
    kernel.saveBrain(brain_path)
