
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer, PorterStemmer
import re
import spacy
from spacy.cli import download

download('en_core_web_sm')
nlp = spacy.load('en_core_web_sm')

def tokenize(text):
    """This funciton tokeizes a sentence into a list of words. Eg 'This is a sentence' to ['This','is','a','sentence'] """
    return word_tokenize(text)

def remove_stop_words(text):
    """This funtion removes stop words such as 'he','i','it','and' 'if'"""
    stop_words = set(stopwords.words('english'))
    return([token.lower() for token in text if token not in stop_words])

def remove_punct(text):
    """This removes punctuations from the given input text which remove_PropNouns fails to remove, hence call this after remove_PropNouns"""
    puncts = "~`!@#€$%^&*()_-+={[}]|\:;'<,>.?/“”‘’"
    for indx in range(len(text)-1):
        tmp_val=text[indx]
        for punct in puncts:
            tmp_val = tmp_val.replace(punct,"")
        text[indx]=tmp_val
    text = list(filter(None, text))
    return text
#    return ([char for char in text if char not in char])

def stem_words(text):
    """This convertes a word to its root word. eg: Running will become Run"""
    stemmer = WordNetLemmatizer()
    return ([stemmer.lemmatize(token) for token in text])

def stem_words_more(text):
    """This convertes a word to its root word. eg: Running will become Run"""
    stemmer = PorterStemmer()
    return ([stemmer.stem(token) for token in text])

def regex_String_Identifier(text):
    """This funtion identifies strings using regex pattern match"""
    regex_lst = ['(@[\w]+)',# Pattern for words starting with @
                 '(#[\w]+)',# Pattern for words starting with #
                 '([.]{2,})',# Pattern matching full-stop which coccurs more than once in sequence
                 '(http(?:s)?\:\/\/[a-zA-Z0-9]+(?:(?:\.|\-)[a-zA-Z0-9]+)+(?:\:\d+)?(?:\/[\w\-]+)*(?:\/?|\/\w+\.[a-zA-Z]{2,4}(?:\?[\w]+\=[\w\-]+)?)?(?:\&[\w]+\=[\w\-]+))' #Pattern to identify url 1
                ,'((?:http[s])\://(?:[0-9a-zA-Z\-]+\.)+[a-zA-Z]{2,6}(?:\:[0-9]+)?(?:/\S*)?)' #Pattern to identify url 2
                ,'([\d]+)'] #Pattern to identify digits
    words_lst=[]
    final_words_lst = []
    for regex in regex_lst: # Iterate over the regex list
        words = re.findall(regex, text) # Identify matches using the regex pattern
        words_lst.extend(words) # Append the identified words to a list
        #print(regex,words_lst)
    for i in words_lst:
        if i not in final_words_lst:
            final_words_lst.append(i)
    return(final_words_lst)

def remove_pattersn(text,words):
    """This funtion removes words given in 'words' from 'text' """
    for i in words:
        #print(i)
        text = text.replace(i, "")
        #print(str(i)+str(text)+"\n")
    return(text)

def remove_Emoji(text):
    """This function removes emojis from the text input"""
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  # dingbats
                               u"\u3030"
                               "]+", flags=re.UNICODE)
    dat=emoji_pattern.sub(r'', text)
    return(dat)

def remove_PropNouns(text):
    """This funtion removes proper nouns, punctuations and symbols using Spacy"""
    doc=nlp(text)
    text_words=[]
    for token in doc:
        if token.pos_ != "PROPN" and token.pos_ != "X" and token.pos_ !='PUNCT' and token.pos_ !='SYM':
            text_words.append(token.text)
    return " ".join(text_words)


def data_digest(text):
    dat_tk=remove_Emoji(text)
    regexWords=regex_String_Identifier(dat_tk)
    dat_tk=remove_pattersn(dat_tk,regexWords)
    dat_tk=remove_PropNouns(dat_tk)
    dat_tk = tokenize(dat_tk)
    dat_tk = remove_punct(dat_tk)
    dat_tk = remove_stop_words(dat_tk)
    dat_tk = stem_words_more(dat_tk)
    dat_tk = " ".join(dat_tk)
    return(dat_tk)


