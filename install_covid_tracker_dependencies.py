import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

module_names = ['pandas','numpy','requests','pyqt5','pyqtgraph','scipy','SpeechRecognition','sounddevice','json','urllib']
import importlib


for i in module_names:
    module_name = importlib.util.find_spec(i)
    if module_name is not None:
        pass
    else:
        install(i)