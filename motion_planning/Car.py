
import numpy as np
import pylab as pl
from scipy.integrate import odeint

class Car(object):
    def __init__(self, length, width, v, current_state, min_turn_radius):
        self._length = length
        self._width = width
        self._v = v
        self.current_state = current_state
        self.visualize_as_center = True
        self.min_turn_radius = min_turn_radius
    def kinematics(self, current_state, t, control):
        # current_state = [x, y, theta]
        dstate = [0.0, 0.0, 0.0]
        dstate[0] = np.cos(current_state[2])*self._v
        dstate[1] = np.sin(current_state[2])*self._v
        dstate[2] = control
        return dstate
    def integrate_car(self, current_state, control, dt):
        if current_state is None:
            current_state = self.current_state
        sol = odeint(self.kinematics, current_state, np.linspace(0, dt, 11), args = (control,) )
        next_state = [0.0, 0.0, 0.0]
        next_state[0], next_state[1], next_state[2] = sol[-1,0], sol[-1,1], sol[-1,2]
        self.current_state = next_state
        return next_state
        # r = ode(self.kinematics).set_integrator('dop853')
        # r.set_initial_value(current_state, 0.0)
        # r.integrate(r.t+dt)
        # assert (r.successful()), "integration failed."
    def visualize(self, current_state = None, color = 'b-'):
        if current_state is not None:
            self.current_state = current_state
        assert self.current_state is not None
        car_pts = np.zeros( (2,5), dtype = np.double )
        car_pts[:,0] = [ self._length/2.0,  self._width/2.0]
        car_pts[:,1] = [ self._length/2.0, -self._width/2.0]
        car_pts[:,2] = [-self._length/2.0, -self._width/2.0]
        car_pts[:,3] = [-self._length/2.0,  self._width/2.0]
        car_pts[:,4] = [ self._length/2.0,  self._width/2.0]
        transform = np.array( [ [np.cos(self.current_state[2]), -np.sin(self.current_state[2])],[np.sin(self.current_state[2]), np.cos(self.current_state[2])] ] )
        car_pts = np.dot(transform, car_pts)   
        car_pts += np.array( [[self.current_state[0]], [self.current_state[1]] ] )

        ax_car = pl.plot( car_pts[0,:], car_pts[1,:], color )
        ax_car = pl.plot( car_pts[0,:2], car_pts[1,:2], color, marker= '+' )
        if self.visualize_as_center:
            pl.xlim([self.current_state[0]-20., self.current_state[0]+20.])
            pl.ylim([self.current_state[1]-20., self.current_state[1]+20.])
        pl.pause(0.01)
        
if __name__ == '__main__':
    current_state = [0.0, 0.0, 0.0]
    print current_state
    myCar = Car(2.66, 1.5, 1.0, current_state) 
    myCar.visualize_as_center = True
    pl.figure(figsize=(8*1.1, 6*1.1))
    pl.axis('equal')
    pl.grid('on')
    pl.xlabel('x (meters)')
    pl.ylabel('y (meters)')
    # pl.legend(fancybox=True, framealpha=0.5)
    
    myCar.visualize()
    for i in xrange(20):
        next_state = myCar.integrate_car(None, 0.1, 0.5)
        myCar.visualize()
        print next_state
    
    pl.show()
    
