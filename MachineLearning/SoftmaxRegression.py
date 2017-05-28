from mnist import read, show
import numpy as np
import os
import pdb

cwd = os.getcwd()
# "training" or "testing" 
train_images = read("training",cwd)

n = 28*28
m = 60000 #No of training sets, max: 60000
train_y = np.empty([m,1])
train_x = np.empty([m,n])
i = 0
for image in train_images:
    if i >= m: break
    train_x[i,:] = np.reshape(image[1],(1,n))
    train_y[i] = image[0]
    i += 1
mean_x = np.mean(train_x, axis=0)
std_x  = np.std(train_x,  axis=0)
pdb.set_trace()
train_x = (train_x - mean_x)/std_x
train_x = np.concatenate( (np.ones( (m,1) ),train_x), axis=1 )
# testing images
m_test = 10000 #No of test sets, max: 10000
test_images = read("testing",cwd)
text_y = np.empty([m,1])
test_x = np.empty([m_test,n])
i = 0
for image in test_images:
    if i >= m_test: break
    test_x[i,:] = np.reshape(image[1],(1,n))
    text_y[i] = image[0]
    i += 1
test_x = (test_x - mean_x)/std_x
test_x = np.concatenate( (np.ones( (m,1) ),test_x), axis=1 )

    