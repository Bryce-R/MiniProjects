import numpy as np
import pylab as pl
import Car
import pickle
import random
import os

def cont_2_dist(current_pos):
    current_cell = (np.floor(current_pos[0]/0.01), np.floor(current_pos[1]/0.01), np.floor(current_pos[2]/(0.5/180.*np.pi)) )
    return current_cell

def dist_2_cont(current_cell):
    current_pos = (current_cell[0]*0.01, current_cell[1]*0.01, current_cell[2]*(0.5/180.*np.pi) )
    return current_pos

def main():
    start = (0.0, 0.0, 0.0)
    myCar = Car.Car(2.66, 1.5, -1.0, start) 
    myCar.visualize_as_center = False
    control_actions = [ i/180.*np.pi for i in xrange(1,11) ]
    control_actions += [ -i/180.*np.pi for i in xrange(1,11) ]
    control_actions += [0.0]
    
    dt = 0.2
    
    if not os.path.isfile('cost_func.pickle') :
        cost_func = {start: 0.0}
        for action in control_actions:
            next_state = myCar.integrate_car(start, action, dt)
            print next_state
            next_cell = cont_2_dist(next_state)
            cost_func[ next_cell ] = action*2.+ 0.01
        with open('cost_func.pickle', 'wb') as handle:
            print 'dump:'
            print cost_func
            pickle.dump(cost_func, handle, protocol=pickle.HIGHEST_PROTOCOL)
        

    ct = 0
    while True:
        if os.path.isfile('cost_func.pickle') :
            with open('cost_func.pickle', 'rb') as handle:
                cost_func = pickle.load(handle)
                os.remove('cost_func.pickle')
                print 'load', ct
                # print cost_func
        current_cell = random.choice(cost_func.keys())
        current_pos = dist_2_cont(current_cell)
        for action in control_actions:
            next_state = tuple( myCar.integrate_car(current_pos, action, dt) )
            next_cell = cont_2_dist(next_state)
            if next_cell in cost_func:
                cost_func[ next_cell ] = min( cost_func[current_cell]+ action*2.+ 0.01, cost_func[ next_cell ])
            else:
                cost_func[ next_cell ] = cost_func[current_cell]+ action*2.+ 0.01
        ct += 1
        if ct%1000 == 0:
            print ('length of cost_func: {} .'.format( len(cost_func) ))
            ans = raw_input('Keep calculating or not?  (y/n)')
            if ans == 'n':
                with open('cost_func.pickle', 'wb') as handle:
                    pickle.dump(cost_func, handle, protocol=pickle.HIGHEST_PROTOCOL)
                break
    
    
if __name__ == '__main__':

    main()  
