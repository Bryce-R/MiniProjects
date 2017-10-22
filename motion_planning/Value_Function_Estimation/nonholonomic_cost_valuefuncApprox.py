import numpy as np
import pylab as pl

import pickle
import random
import os

def cont_2_dist(current_pos):
    current_cell = (np.floor(current_pos[0]/0.01), np.floor(current_pos[1]/0.01), np.floor(current_pos[2]/(0.5/180.*np.pi)) )
    return current_cell

def dist_2_cont(current_cell):
    current_pos = (current_cell[0]*0.01, current_cell[1]*0.01, current_cell[2]*(0.5/180.*np.pi) )
    return current_pos

def create_neighbors():
    L = 2.65
    neighbors = np.zeros( (3, 11), np.double );
    # neighbors = [ (L/np.tan(delta/180.*np.pi)*np.sin(5./180.*np.pi), L/np.tan(delta/180.*np.pi)*(1.0 - np.cos(5./180.*np.pi)), 5./180.*np.pi)  for delta in xrange(-25, 25, 5) and delta == 0]
    delta_list = [25, 20, 15, 10, 5]
    for i in xrange( len(delta_list) ):
        delta = delta_list[i]
        r = L/np.tan(delta/180.*np.pi)
        neighbors[:,2*i]   = [ r*np.sin(5./180.*np.pi), r*(1.0 - np.cos(5./180.*np.pi)), 5./180.*np.pi ]
        neighbors[:,2*i+1] = [ r*np.sin(5./180.*np.pi), -r*(1.0 - np.cos(5./180.*np.pi)), 5./180.*np.pi ]
    
    neighbors[:,-1] = [ 0.1*L/np.tan(25./180.*np.pi), 0.0, 0.0 ]
    return neighbors
        

    

def main():
    start = (0.0, 0.0, 0.0)
    neighbors = create_neighbors()
    degree_to_neighbors = {0.0: neighbors}
    print neighbors.T
    
    pl.figure(figsize=(8*1.1, 6*1.1))
    pl.axis('equal')
    pl.grid('on')
    pl.xlabel('x (meters)')
    pl.ylabel('y (meters)')
    pl.legend(fancybox=True, framealpha=0.5)
    pl.plot( neighbors[0,:], neighbors[1,:], '+' )
    pl.show()
    for i in np.linspace(0, 2*np.pi, 180, False):
        pass
        

    
    # dt = 0.2
    # 
    # if not os.path.isfile('cost_func.pickle') :
    #     cost_func = {start: 0.0}
    #     for action in control_actions:
    #         next_state = myCar.integrate_car(start, action, dt)
    #         print next_state
    #         next_cell = cont_2_dist(next_state)
    #         cost_func[ next_cell ] = action*2.+ 0.01
    #     with open('cost_func.pickle', 'wb') as handle:
    #         print 'dump:'
    #         print cost_func
    #         pickle.dump(cost_func, handle, protocol=pickle.HIGHEST_PROTOCOL)
    #     
    # 
    # ct = 0
    # while True:
    #     if os.path.isfile('cost_func.pickle') :
    #         with open('cost_func.pickle', 'rb') as handle:
    #             cost_func = pickle.load(handle)
    #             os.remove('cost_func.pickle')
    #             print 'load', ct
    #             # print cost_func
    #     # rand_num = np.random.rand(3,1)
    #     # rand_goal = ( rand_num[0][0]*20.0-10.0, rand_num[1][0]*20.0-10.0, rand_num[2][0]*np.pi*2.0-np.pi )
    #     if os.path.isfile('close_set.pickle') :
    #         with open('close_set.pickle', 'rb') as handle:
    #             close_set = pickle.load(handle)
    #             os.remove('close_set.pickle')
    #             print 'load close_set'
    #     else:
    #         close_set = {}
    #     current_cell = random.choice(cost_func.keys())
    #     if close_set.get(current_cell, False) :
    #         print 'Already explored this point'
    #         continue
    #     current_pos = dist_2_cont(current_cell)
    #     for action in control_actions:
    #         next_state = tuple( myCar.integrate_car(current_pos, action, dt) )
    #         next_cell = cont_2_dist(next_state)
    #         if next_cell in cost_func:
    #             cost_func[ next_cell ] = min( cost_func[current_cell]+ action*2.+ 0.01, cost_func[ next_cell ])
    #             close_set[next_cell] = False
    #         else:
    #             cost_func[ next_cell ] = cost_func[current_cell]+ action*2.+ 0.01
    #     close_set[current_cell] = True
    #     ct += 1
    #     if ct%1000 == 0:
    #         print ('length of cost_func: {} .'.format( len(cost_func) ))
    #         ans = raw_input('Keep calculating or not?  (y/n)')
    #         if ans == 'n':
    #             with open('cost_func.pickle', 'wb') as handle:
    #                 pickle.dump(cost_func, handle, protocol=pickle.HIGHEST_PROTOCOL)
    #             with open('close_set.pickle', 'wb') as handle:
    #                 pickle.dump(close_set, handle, protocol=pickle.HIGHEST_PROTOCOL)
    #             break
    # 
    
if __name__ == '__main__':

    main()  
