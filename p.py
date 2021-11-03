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
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm
import numpy as np

DOWNLOAD_ROOT = "http://spamassassin.apache.org/old/publiccorpus/"
HAM_URL = DOWNLOAD_ROOT + "20030228_easy_ham.tar.bz2"
SPAM_URL = DOWNLOAD_ROOT + "20030228_spam.tar.bz2"
SPAM_PATH = os.path.join("/Users/trishagupta/Desktop/SpamBayes/datasets", "spam")
HAM_PATH = os.path.join("/Users/trishagupta/Desktop/SpamBayes/datasets","ham")
#contains the elements of the emails to be used as training set

#all the words
words_ham=[]
words_spam=[]

# words in ham per email - words_email_ham, words_email_spam

vocabulary_ham = dict()
vocabulary_spam = dict()


def main():

    #downloading dictionaries and global variables
    nltk.download("stopwords")
    nltk.download('punkt')
    globals.initialize()

    clean_emails()
    counter_ham(words_ham)
    counter_spam(words_spam)
    #parse_emails_words()
    print(len(globals.words_email_ham))


    return 0;


    '''
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print(globals.df_all_ham_words)

    print(len(globals.df_all_ham_words['Frequency']))
    '''



'''
Purpose: to prepare the words for each email
globals.words_email_ham, globals.words_email_spam
'''
'''
def parse_emails_words():

#frequency_distribution = FreqDist(globals.words_email_ham)
print(len(globals.words_email_ham))
#globals.df_all_ham_words = pd.DataFrame(list(frequency_distribution.items()), columns = ['Word','Frequency'])




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

'''
Purpose: this function makes vocubulary of equal lengths for spam and ham
'''
def make_vocabulary():

    length_ham = globals.df_all_ham_words['Frequency'] - 1
    length_spam = globals.df_all_spam_words['Frequency'] - 1
    length = min(length_ham , length_spam)
    globals.df_all_ham_words.drop(globals.df_all_ham_words[length: length_ham], axis = 0, inplace = True)
    globals.df_all_spam_words.drop(globals.df_all_spam_words[length: length_spam], axis = 0, inplace = True)



'''
flag = 0 -> ham
flag = 1 -> spam
'''
def counter_ham(words_ham):

    #outcomes
    #print(frequency_distribution.N())
    frequency_distribution = FreqDist(words_ham)
    globals.df_all_ham_words = pd.DataFrame(list(frequency_distribution.items()), columns = ['Word','Frequency'])
    #sort the frequency distribution by descending order
    globals.df_all_ham_words.sort_values(by = 'Frequency', ascending = False, inplace = True, ignore_index = True)

    globals.df_all_ham_words['Word'] = globals.df_all_ham_words['Word'].str.lower()

    #print(len(globals.df_all_ham_words))
    '''
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print(globals.df_all_ham_words)
    '''

    #If the stop word in is top 40% of the the most common words then we should include it
    vals_to_be_included = int(0.1 * frequency_distribution.B())-1

    words_top = list(globals.df_all_ham_words['Word'].iloc[0:vals_to_be_included])
    stop_words = list(stopwords.words("english"))
    print(words_top)

    for word in stop_words:
        if word in words_top:
            stop_words.remove(word)


    #for loop begins
    for index, row in globals.df_all_ham_words.iterrows():
        word = row['Word']

        # if the word is in the word_top then it should be added even if it is a stop word
        if (word.casefold() in stop_words):
            globals.df_all_ham_words.drop(index, axis = 0, inplace = True)
            globals.df_all_ham_words.reset_index()
    #for loop ends



    #keep only top 60%
    vals_to_be_included = int(0.6 * len(globals.df_all_ham_words))
    globals.df_all_ham_words.drop( globals.df_all_ham_words.index[vals_to_be_included:len(globals.df_all_ham_words['Frequency']-1)], axis = 0 ,inplace = True)
    globals.df_all_ham_words.reset_index()
    #print(len(globals.df_all_ham_words))



def counter_spam(words_spam):

    #outcomes
    #print(frequency_distribution.N())
    frequency_distribution = FreqDist(words_spam)
    globals.df_all_spam_words = pd.DataFrame(list(frequency_distribution.items()), columns = ['Word','Frequency'])
    #sort the frequency distribution by descending order
    globals.df_all_spam_words.sort_values(by = 'Frequency', ascending = False, inplace = True, ignore_index = True)
    globals.df_all_spam_words['Word'] = globals.df_all_spam_words['Word'].str.lower()

    #If the stop word in is top 40% of the the most common words then we should include it
    vals_to_be_included = int(0.1 * frequency_distribution.B())-1

    words_top = globals.df_all_spam_words['Word'].iloc[0:vals_to_be_included]
    stop_words = list(stopwords.words("english"))


    for index, row in globals.df_all_spam_words.iterrows():
        word = row['Word']
        #print(globals.df_all_ham_words[word])
        #print(word)

        # if the word is in the word_top then it should be added even if it is a stop word
        if (word.casefold() not in stop_words or word.casefold() in words_top):
            continue
        else:
            globals.df_all_spam_words.drop(index, axis=0, inplace = True)

    #print(len(globals.df_all_ham_words))

    vals_to_be_included = int(0.6 * len(globals.df_all_spam_words))
    globals.df_all_spam_words.drop( globals.df_all_spam_words.index[vals_to_be_included:len(globals.df_all_spam_words['Frequency']-1)], axis = 0 ,inplace = True)






'''
**************************************************************************************************************************************************************************
'''


'''
Purpose: downloads the files and parses each email in spam and ham
'''
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



#for loop starts here
    for x in ham_emails:
        curr_email =[]

        if x.is_multipart == True:
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


        elif x.get_content_type() == 'text/plain':
            content  = x.get_payload(decode=True).decode('utf-8', 'ignore')
            globals.ham_emails_set.append(append_val_ham(content))
            curr_email.append(append_val_ham(content))


        globals.words_email_ham.append(curr_email)
#for loop ends here







#for loop starts here
    for x in spam_emails:

            if x.is_multipart == True:
                for m in x.iter_parts():

                        if m.get_content_type() == 'text/plain':
                            globals.spam_emails_set.append(append_val_spam(str(m)))
                            curr_email.append(append_val_spam(str(m)))
                        elif m.get_content_type() == 'text/html':
                            # 1 for spam
                            parse_html(m.get_content(),1)
                            curr_email.append(globals.spam_emails_set[len(globals.spam_emails_set)-1])
                        elif m.get_content_type() == 'application/pgp-signature':
                            globals.spam_emails_set.append(append_val_spam(str(m.get_content())))
                            curr_email.append(append_val_spam(str(m.get_content())))


            elif x.get_content_type() == 'text/plain':
                content  = x.get_payload(decode=True).decode('utf-8', 'ignore')
                globals.spam_emails_set.append(append_val_spam(content))
                curr_email.append(append_val_spam(content))


            globals.words_email_spam.append(curr_email)
        #for loop ends here


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


'''
Function: append_val_ham
Inputs: soup
Outputs: words_temp
Purpose: returns the value to be appended to the emails
'''
def append_val_ham(soup):

    #bad style rmeove multiple res
    soup2 = re.sub(r"\n", " ",soup)
    soup3 = re.sub(r"\t", " ", soup2)
    soup4 = re.sub(r"\r", " ",soup3)
    soup5 = re.sub(">", " ",soup4)
    soup6 = re.sub("<", " ", soup5)
    soup7 = re.sub(r'[.,"\'-?:!;]', '', soup6)
    words_temp = soup7.split(' ')


    try:
        while True:
            words_temp.remove('')
    except ValueError:
        pass


    words_ham.extend(words_temp)

    return words_temp


'''
Function: append_val_spa,
Inputs: soup
Outputs: words_temp
Purpose: returns the value to be appended to the emails
'''
def append_val_spam(soup):

    #bad style rmeove multiple res
    soup2 = re.sub(r"\n", " ",soup)
    soup3 = re.sub(r"\t", " ", soup2)
    soup4 = re.sub(r"\r", " ",soup3)
    soup5 = re.sub(">", " ",soup4)
    soup6 = re.sub("<", " ", soup5)
    soup7 = re.sub(r'[.,"\'-?:!;]', '', soup6)
    words_temp = soup7.split(' ')


    try:
        while True:
            words_temp.remove('')
    except ValueError:
        pass

    #print(words_temp)
    words_spam.extend(words_temp)

    return words_temp



if __name__ == "__main__":
    main()
