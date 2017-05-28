import numpy as np
import pdb
import matplotlib.pyplot as plt
import sys

if __name__ == '__main__':
    f = open('housing.data')
    data = []
    for line in f:
        data += [map(float, line.split())]
    f.close()
    data_arr = np.array(data)
    data_arr = data_arr.T
    # print data_arr.shape
    data_arr = np.append(np.ones((1,data_arr.shape[1])), data_arr,  axis=0)
    original_data = np.copy(data_arr)
    ind = original_data[14,:].argsort()
    original_data = original_data[:,ind]
    # print data_arr.shape
    np.random.permutation(data_arr)
    # split data into training set and testing set
    train = (data_arr[0:(data_arr.shape[0]-1), 0:400],
             data_arr[data_arr.shape[0]-1,  0:400 ])
    test = (data_arr[0:(data_arr.shape[0]-1), 400:],
             data_arr[data_arr.shape[0]-1,  400: ])
    n, m = train[0].shape
    print 'Training set dimensions: m = {}, parameters: n = {}.'.format(m,n)

    # theta init
    # theta = np.zeros((n,1))
    theta = np.random.rand(n,1)
    alpha = 0.000001
    ct = 200
    while(ct >0):
        ct -= 1
        sys.stdout.write( 'Iteration {}: \r'.format(ct) )
        sys.stdout.flush()
        # print err
        for i in xrange(m):
            # pdb.set_trace()
            for j in xrange(n):
                err = train[1][i] - np.dot(train[0][:,i], theta)
                theta[j] +=  alpha*err*train[0][j,i]
    # pdb.set_trace()
    train_RMS = np.linalg.norm(theta.T.dot(train[0]) - train[1], 2)/m
    test_RMS = np.linalg.norm(theta.T.dot(test[0]) - test[1], 2)/test[0].shape[1]
    print 'Training set RMS error: {}'.format(train_RMS)
    print 'Testing set RMS error: {}'.format(test_RMS)
    
    
    predic = ( np.matmul(theta.T, original_data[0:original_data.shape[0]-1,:]) ).T

    plt.plot(original_data[-1,:],'b.-',label='Actual')
    plt.plot(predic,'r.-',label='Predicted')
    plt.legend()
    plt.show()





