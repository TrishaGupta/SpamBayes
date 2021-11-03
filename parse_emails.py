import math
import os
import numpy as np
import sklearn
from pandas import *





def main():


    #test = get_ham_emails()
    #print(test)

    #test = get_spam_emails()
    #print(test)

'''
Function: get_ham_emails
Inputs: None
Outputs: ham_dict
Purpose: this function parses the emails into a list and creates a dictionary for the words that occur in the ham emails
'''
def get_ham_emails():

    # contains dictionary which maps word->freq in the hams mails
    ham_dict  = {}

    #get data from ham csv file
    data = read_csv("Emails/spam_or_not_spam.csv")
    #print(data)
    emails = data['email'].tolist()

    for i in range(2502):

        entry = emails [i]
        words = entry.split(' ')

        for word in words:

            curr = word.lower()

            if curr in ham_dict:
                ham_dict[curr] +=1

            else:
                ham_dict[curr] =1

    return ham_dict


'''
Function: get_spam_emails
Inputs: None
Outputs: spam_dict
Purpose: this function parses the emails into a list and creates a dictionary for the words that occur in the spam emails
'''
def get_spam_emails():

    # contains dictionary which maps word->freq in the hams mails
    spam_dict  = {}

    #get data from ham csv file
    data = read_csv("Emails/spam_or_not_spam.csv")
    #print(data)
    emails = data['email'].tolist()

    for i in range(2502, 3000, 1):

        entry = str(emails[i])

        words = entry.split(' ')

        for word in words:

            curr = word.lower()

            if curr in spam_dict:
                spam_dict[curr] +=1

            else:
                spam_dict[curr] =1

    return spam_dict







if __name__ == "__main__":
    main()
