from aiml import Kernel
from os import listdir
from os.path import dirname, isfile, join
from fnmatch import filter
import json

kernel = Kernel()

chatbot = "Winston"
chatbot_brain = chatbot + ".brn"
chatbot_variables = chatbot + ".json"

aiml_path = join(dirname(__file__), chatbot)
brain_path = join(dirname(__file__), chatbot, chatbot_brain)
variables_path = join(dirname(__file__), chatbot, chatbot_variables)

if isfile(brain_path):
    kernel.bootstrap(brainFile=brain_path)
else:
    aimls = filter(listdir(aiml_path), "*.aiml")
    for aiml_file in aimls:
        kernel.learn(join(aiml_path, aiml_file))
    kernel.saveBrain(brain_path)

with open(variables_path) as f:
    variables = json.load(f)

for key, value in variables.items():
    kernel.setBotPredicate(key, value)

# Press CTRL-C to break this loop
while True:
    print(kernel.respond(input("Enter your message >> ")))
    kernel.saveBrain(brain_path)
