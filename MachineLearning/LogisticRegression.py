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
    if image[0] == 0 or image[0] == 1:
        train_x[i,:] = np.reshape(image[1],(1,n))
        train_y[i] = image[0]
        i += 1
m = i
train_x = train_x[:i,:]
train_y = train_y[:i]
mean_x = np.mean(train_x, axis=0)
std_x  = np.std(train_x,  axis=0) + 0.1

train_x = (train_x - mean_x)/std_x
train_x = np.concatenate( (np.ones( (m,1) ),train_x), axis=1 )
# pdb.set_trace()
print 'No. of training examples: m = {}'.format(train_x.shape[0])
# testing images
m_test = 10000 #No of test sets, max: 10000
test_images = read("testing",cwd)
test_y = np.empty([m,1])
test_x = np.empty([m_test,n])
i = 0
for image in test_images:
    if image[0] == 0 or image[0] == 1:
        test_x[i,:] = np.reshape(image[1],(1,n))
        test_y[i] = image[0]
        i += 1
m_test = i
test_x = test_x[:i,:]
test_y = test_y[:i]
test_x = (test_x - mean_x)/std_x
test_x = np.concatenate( (np.ones( (m_test,1) ),test_x), axis=1 )
print 'No. of testing examples: m = {}'.format(test_x.shape[0])
    