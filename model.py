import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline
import globals
import parse





def main():
    globals.initialize()
    parse.main()
    split_dataset()


'''
Function: split_dataset
Inputs: None
Outputs: None
Purpose: splits the dataset into training and testing sets
'''
def split_dataset():

    X = np.array(globals.ham_emails_set + globals.spam_emails_set)
    Y = np.array([0]* len(globals.ham_emails_set) + [1]*len(spam_emails_set))

    X_train, Y_train, X_test, Y_test = train_test_split(X,Y, test_size =0.2, random_state = 42)


'''
Function: test_set_check
Inputs: identifier, test_ratio, hash
Outputs: hash_val
Purpose: this function checks the hash value of the input and only return true if its less than 245*test ratio so that the samples don;t chan ge with new datasets
'''
def test_set_check(identifier, test_ratio, hash):

    hash_val = hash(np.int64(identifier)).digest()[-1] < 256 * test_ratio
    return hash_val




def pipeline():



def linear_reg():

    log_clf = LogisticRegression(solver="liblinear", random_state=42)
    score = cross_val_score(log_clf, X_train_transformed, y_train, cv=3, verbose=3)
    score.mean()




if __name__ == "__main__":
    main()
