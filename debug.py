from sklearn.model_selection import train_test_split
import numpy as np
import hashlib



def main():

    split()


def test_set_check(identifier, test_ratio, hash):
    return hash(np.int64(identifier)).digest()[-1] < 256 * test_ratio




def split():
    X = np.array([1,2,3,4,5,6,7,8,9,10]).reshape(-1,1)
    y = np.array([11,12,13,14,15,16,17,18,19,20])


    X_train, X_test, y_train, y_test =  train_test_split(X,y, test_size =0.2, random_state = 42)


    X_train2, X_test2, y_train2, y_test2 =  train_test_split(X,y, test_size =0.2)


    for x in X:
        print(test_set_check(x, 0.2, hashlib.md5))

    '''
    print(X_train2)
    print(y_train2)
    print(X_test2)
    print(y_test2)
    '''


if __name__ == "__main__":
    main()
