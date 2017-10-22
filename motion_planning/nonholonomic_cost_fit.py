import numpy as np
import pylab as pl
import Car
import pickle
import random
import os
import nonholonomic_cost_func


def main():
    
    pl.figure(figsize=(8*1.1, 6*1.1))
    pl.axis('equal')
    pl.grid('on')
    pl.xlabel('x (meters)')
    pl.ylabel('y (meters)')
    pl.legend(fancybox=True, framealpha=0.5)
    pl.xlim([-20., 20.])
    pl.ylim([-20., 20.])
    
    start = (0.0, 0.0, 0.0)
    myCar = Car.Car(2.66, 1.5, -1.0, start, 5.5) 
    myCar.visualize_as_center = False
    if os.path.isfile('cost_func.pickle') :
        with open('cost_func.pickle', 'rb') as handle:
            cost_func = pickle.load(handle)
    for current_cell in cost_func:
        current_pos = nonholonomic_cost_func.dist_2_cont(current_cell)
        # myCar.visualize(current_pos, 'c:')
        pl.plot(current_pos[0], current_pos[1], '+c', label = 'start')
        # 
        # pl.pause(0.01)
    pl.show()
    print 'End.'


    
if __name__ == '__main__':
    main()  
