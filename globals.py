

'''
Contains all the global variables used in this project
'''
def initialize():

    global spam_emails_set
    spam_emails_set = []

    global ham_emails_set
    ham_emails_set = []

    global ham_dict
    ham_dict = {}

    global freqword_ham
    freqword_ham = dict()

    global freqword_spam
    freqword_spam = dict()

    global words_email_ham
    words_email_ham = []

    global words_email_spam
    words_email_spam =[]

    global df_all_ham_words
    df_all_ham_words =[]

    global df_all_spam_words
    df_all_spam_words =[]

    global df_words_per_ham
    df_words_per_ham =[]

    global df_words_per_spam
    df_words_per_spam =[]
