
import numpy as np
import pylab as pl
from scipy.integrate import odeint

class Car(object):
    def __init__(self, length, width, v, current_state= None):
        self._length = length
        self._width = width
        self._v = v
        self.current_state = current_state
    def kinematics(self, current_state, t, control):
        # current_state = [x, y, theta]
        dstate = [0.0, 0.0, 0.0]
        dstate[0] = np.cos(current_state[2])*self._v
        dstate[1] = np.sin(current_state[2])*self._v
        dstate[2] = control
        return dstate
    def integrate_car(self, current_state, control, dt):
        sol = odeint(self.kinematics, current_state, np.linspace(0, dt, 10), args = (control,) )
        next_state = [0.0, 0.0, 0.0]
        next_state[0], next_state[1], next_state[2] = sol[-1,0], sol[-1,1], sol[-1,2]
        self.current_state = next_state
        return next_state
        # r = ode(self.kinematics).set_integrator('dop853')
        # r.set_initial_value(current_state, 0.0)
        # r.integrate(r.t+dt)
        # assert (r.successful()), "integration failed."
    def visulize(self):
        assert self.current_state is not None
        car_pts = np.zeros( (2,5), dtype = np.double )
        car_pts[:,0] = np.array([self.current_state[0]+self._length/2.0, self.current_state[1]+self._width/2.0])
        car_pts[:,1] = np.array([self.current_state[0]+self._length/2.0, self.current_state[1]-self._width/2.0])
        car_pts[:,2] = np.array([self.current_state[0]-self._length/2.0, self.current_state[1]-self._width/2.0], ndmin = 2)
        car_pts[:,3] = [self.current_state[0]-self._length/2.0, self.current_state[1]+self._width/2.0]
        car_pts[:,4] = [self.current_state[0]+self._length/2.0, self.current_state[1]+self._width/2.0]
        transform = np.array( [ [np.cos(self.current_state[2]), np.sin(self.current_state[2])],[-np.sin(self.current_state[2]), np.cos(self.current_state[2])] ] )
        car_pts = np.dot(transform, car_pts)       
        pl.plot( car_pts[0,:], car_pts[1,:], 'b-' )

        pl.pause(0.01)
        
if __name__ == '__main__':
    current_state = [0.0, 0.0, 0.0]
    print current_state
    myCar = Car(2.66, 1.5, 1.0, current_state) 
    pl.figure(figsize=(8*1.1, 6*1.1))
    myCar.visulize()
    
    next_state = myCar.integrate_car(current_state, 0.1, 0.5)
    myCar.visulize()
    pl.show()
    
    
    print next_state
