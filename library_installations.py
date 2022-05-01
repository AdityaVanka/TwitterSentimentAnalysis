
import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install("nltk")
install("sklearn")
install("spacy")
install("pandas")
install("nltk")
install("charts")
install("vaderSentiment")
install("plotly")
install("kaleido")
install("matplotlib")
from spacy.cli import download
import nltk
download('en_core_web_sm')
nltk.download('punkt')
nltk.download('stopwords')