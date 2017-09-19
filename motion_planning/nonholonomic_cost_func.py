import numpy as np
import pylab as pl
import Car
import pickle
import random
import os.path

def cont_2_dist(self, current_pos):
    current_cell = (np.floor(current_pos[0]/self.cellsize[0]), np.floor(current_pos[1]/self.cellsize[1]), np.floor(current_pos[2]/self.cellsize[2]) )
    return current_cell

def main():
    start = (0.0, 0.0, np.pi/2.0)
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
            cost_func[ tuple(next_state) ] = action*2.+ 0.01
        with open('cost_func.pickle', 'wb') as handle:
            pickle.dump(cost_func, handle, protocol=pickle.HIGHEST_PROTOCOL)
        

    ct = 0
    while True:
        if os.path.isfile('cost_func.pickle') :
            with open('cost_func.pickle', 'rb') as handle:
                cost_func = pickle.load(handle)
        current_state = random.choice(cost_func.keys())
        for action in control_actions:
            next_state = tuple( myCar.integrate_car(current_state, action, dt) )
            if next_state in cost_func:
                cost_func[ next_state ] = min( cost_func[current_state]+ action*2.+ 0.01, cost_func[ next_state ])
            else:
                cost_func[ next_state ] = cost_func[current_state]+ action*2.+ 0.01
        ct += 1
        if ct%1000 == 0:
            ans = raw_input('Keep calculating or not?  (y/n)')
            if ans == 'n':
                with open('cost_func.pickle', 'wb') as handle:
                    pickle.dump(cost_func, handle, protocol=pickle.HIGHEST_PROTOCOL)
                break
    
    
if __name__ == '__main__':
    main()  
