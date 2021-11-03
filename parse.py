import os
import tarfile
import urllib.request
import requests
import email
import email.policy
import re
from bs4 import BeautifulSoup
from collections import Counter, defaultdict
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import FreqDist
from nltk.tokenize import wordpunct_tokenize
import globals

DOWNLOAD_ROOT = "http://spamassassin.apache.org/old/publiccorpus/"
HAM_URL = DOWNLOAD_ROOT + "20030228_easy_ham.tar.bz2"
SPAM_URL = DOWNLOAD_ROOT + "20030228_spam.tar.bz2"
SPAM_PATH = os.path.join("/Users/trishagupta/Desktop/SpamBayes/datasets", "spam")
HAM_PATH = os.path.join("/Users/trishagupta/Desktop/SpamBayes/datasets","ham")
#contains the elements of the emails to be used as training set

words_ham=[]
words_spam=[]


vocabulary_ham = dict()
vocabulary_spam = dict()


def main():

    nltk.download("stopwords")
    nltk.download('punkt')
    globals.initialize()
    clean_emails()
    counter_ham(words_ham)
    counter_spam(words_spam)
    #print(words_email_ham)
    parse_emails_words()




    return 0;



def clean_emails():

    download_emails();
    #contains the emails
    ham_emails = []
    spam_emails = []



    #first go through the ham emails
    for file in os.listdir(os.path.join(HAM_PATH, "easy_ham")):
        #open each file in the dir
        with open(os.path.join(HAM_PATH, "easy_ham",file), "rb") as f:
            #parse using the defaul line break(\n)
            ham_emails.append(email.parser.BytesParser(policy=email.policy.default).parse(f))


    for file in os.listdir(os.path.join(SPAM_PATH, "spam")):
        #open each file in the dir
        with open(os.path.join(SPAM_PATH, "spam",file), "rb") as f:
            #parse using the defaul line break(\n)
            spam_emails.append(email.parser.BytesParser(policy=email.policy.default).parse(f))


    for x in ham_emails:
        curr_email =[]

        if x.get_content_type != 'text/plain':
            for m in x.iter_parts():

                    if m.get_content_type() == 'text/plain':
                        globals.ham_emails_set.append(append_val_ham(str(m)))
                        curr_email.append(append_val_ham(str(m)))
                    elif m.get_content_type() == 'text/html':
                        parse_html(m.get_content(),0)
                        curr_email.append(globals.ham_emails_set[len(globals.ham_emails_set)-1])
                    elif m.get_content_type() == 'application/pgp-signature':
                        globals.ham_emails_set.append(append_val_ham(str(m.get_content())))
                        curr_email.append(append_val_ham(str(m.get_content())))


        else:
            globals.ham_emails_set.append_val_ham(str(x))
            curr_email.append(append_val_ham(str(x)))
            print(x.get_content_type())


        globals.words_email_ham.append(curr_email)
        #if len(curr_email) == 0:
            #print(x.get_content_type())
        #print(curr_email)





    for x in spam_emails:

        if x.iter_parts() != None:
            for m in x.iter_parts():

                #print(type(m))

                if m.get_content_type() == 'text/plain':
                    globals.spam_emails_set.append(append_val_spam(str(m)))
                elif m.get_content_type() == 'text/html':
                    parse_html(m.get_content(),1)


                    '''
                    TO DO: deal with different content types such as images, etc. For now ignore
                    '''
        else:
            globals.spam_emails_set.append_val_spam(x)

    #(spam_emails_set)


'''
Function: parse_html
Inputs: body, flag
Outputs: None
Purpose: this function parses the HTML text in the email and appends it to the appropriate set depending on the flag

flag = 0 -> ham
flag = 1 -> spam
'''
def parse_html(body, flag):

    soup = BeautifulSoup(body,features="html.parser")

    if flag == 1:
        globals.spam_emails_set.append(append_val_spam(soup.text))
    else:
        globals.ham_emails_set.append(append_val_ham(soup.text))






def append_val_ham(soup):

    #bad style rmeove multiple res
    soup2 = re.sub(r"\n", " ",soup)
    soup3 = re.sub(r"\t", " ", soup2)
    soup4 = re.sub(r"\r", " ",soup3)
    soup5 = re.sub(">", " ",soup4)
    soup6 = re.sub("<", " ", soup5)
    words_temp = soup6.split(' ')


    try:
        while True:
            words_temp.remove('')
    except ValueError:
        pass

    #print(words_temp)
    words_ham.extend(words_temp)

    return words_temp



def append_val_spam(soup):

    #bad style rmeove multiple res
    soup2 = re.sub(r"\n", " ",soup)
    soup3 = re.sub(r"\t", " ", soup2)
    soup4 = re.sub(r"\r", " ",soup3)
    soup5 = re.sub(">", " ",soup4)
    soup6 = re.sub("<", " ", soup5)
    words_temp = soup6.split(' ')


    try:
        while True:
            words_temp.remove('')
    except ValueError:
        pass

    #print(words_temp)
    words_spam.extend(words_temp)

    return words_temp

'''
flag = 0 -> ham
flag = 1 -> spam
'''
def counter_ham(words):

    #outcomes
    #print(frequency_distribution.N())
    frequency_distribution = FreqDist(words_ham)

    #If the stop word in is top 40% of the the most common words then we should include it
    vals_to_be_included = int(0.4 * frequency_distribution.B())

    words_top = frequency_distribution.most_common(vals_to_be_included)
    stop_words = list(stopwords.words("english"))
    stop_words.append(words_top)

    filtered_words = []
    track_word =[]
    freqword_ham_temp = dict()

    for word in words_ham:
        if word.casefold() not in stop_words and word.casefold() not in track_word:
            track_word.append(word.lower())
            if int(frequency_distribution.freq(word)*frequency_distribution.N()) in freqword_ham_temp:
                freqword_ham_temp[int(frequency_distribution.freq(word)*frequency_distribution.N())].append(word)
            else:
                freqword_ham_temp[int(frequency_distribution.freq(word)*frequency_distribution.N())] = [word]


    #print(freqword_ham_temp)
    globals.freqword_ham = sorted(freqword_ham_temp)




def counter_spam(words):

    frequency_distribution = FreqDist(words_spam)

    #If the stop word in is top 40% of the the most common words then we should include it
    vals_to_be_included = int(0.4 * frequency_distribution.B())

    words_top = frequency_distribution.most_common(vals_to_be_included)
    stop_words = list(stopwords.words("english"))
    stop_words.append(words_top)

    filtered_words = []
    track_word =[]
    freqword_spam_temp = dict()

    for word in words_ham:
        if word.casefold() not in stop_words and word.casefold() not in track_word:
            track_word.append(word.lower())
            if int(frequency_distribution.freq(word)*frequency_distribution.N()) in freqword_spam_temp:
                freqword_spam_temp[int(frequency_distribution.freq(word)*frequency_distribution.N())].append(word)
            else:
                freqword_spam_temp[int(frequency_distribution.freq(word)*frequency_distribution.N())] = [word]


    globals.freqword_spam = sorted(freqword_spam_temp)


'''
Purpose: thsi function makes vocubulary of equal lengths for spam and ham
'''
def make_vocabulary():

    length = min(len(globals.freqword_ham),len(globals.freqword_spam))
    vocabulary_ham = globals.freqword_ham[0:length]
    vocabulary_spam = globals.freqword_spam[0:length]

'''
Purpose: to prepare the words for each email
'''
def parse_emails_words():

    words_temp =[]
    for content in globals.words_email_ham:

        if len(content)!= 0:
            words = word_tokenize(str(content))

            words_temp.append(FreqDist(words))
        else:
            words_temp.append([])



    globals.words_email_ham = words_temp

    #print(globals.words_email_ham)





'''
Function: download_emails
Inputs: None
Outputs: None
Purpose: this function downloads and unzips the spam and email emails and saves them in the path specified
'''

def download_emails():

    if os.path.isdir("/Users/trishagupta/Desktop/SpamBayes/datasets") == False:
        os.mkdir("/Users/trishagupta/Desktop/SpamBayes/datasets")

    if os.path.isdir(SPAM_PATH) == False:
        os.mkdir(SPAM_PATH)


    if os.path.isdir(HAM_PATH) == False:
        os.mkdir(HAM_PATH)


    for url, path, temp in [(HAM_URL,HAM_PATH, "ham.tar.bz2") , (SPAM_URL,SPAM_PATH,"spam.tar.bz2")]:

        #get the file from the url
        urllib.request.urlretrieve(url, temp)
        #open
        files = tarfile.open(temp)
        files.extractall(os.path.join(path))
        files.close()





if __name__ == "__main__":
    main()
