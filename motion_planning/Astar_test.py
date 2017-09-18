import math
import numpy as np
import Queue
import pylab as pl
import Car


class Astar(object):
    def __init__(self, start, goal):
        self.start = start
        self.goal = goal
        self.cellsize = (0.2, 0.2, 2./180*np.pi )
        self.start_cell = self.cont_2_dist(start)
        self.goal_cell = self.cont_2_dist(goal)
        self.f_cost = 0.1
        self.v = 0.5
        self.steering_change = 2.0
        self.Car = Car.Car(2.66, 1.5, 1.0, start) 
        self.Car.visualize_as_center = False
        self.model = self.Car.integrate_car
        self.visualize = self.Car.visualize

    def cont_2_dist(self, current_pos):
        current_cell = (np.floor(current_pos[0]/self.cellsize[0]), np.floor(current_pos[1]/self.cellsize[1]), np.floor(current_pos[2]/self.cellsize[2]) )
        return current_cell
    
    def heuristic(self, current):
        # cost_h = (current[0] - self.goal[0])**2 + (current[1] - self.goal[1])**2 + (current[2] - self.goal[2])**2
        w_x = 30.0
        w_y = 10.0
        w_theta = 10.0
        # if current[0] < self.goal[0]:
        cost_h = np.sqrt( (current[0] - self.goal[0])**2*w_x**2 + (current[1] - self.goal[1])**2*w_y**2 ++ (current[2] - self.goal[2])**2*(w_theta)**2 )
        # else:
        #     cost_h = float('inf')
        # cost_h = current[0] - self.goal[0] + np.sqrt( (current[1] - self.goal[1])**2*w_y**2 ++ (current[2] - self.goal[2])**2*(w_theta)**2)
        return cost_h
    
    def euler_int_model(self, current_pos, steering):
        next_pos_x = current_pos[0]+np.cos(current_pos[2])*self.v
        next_pos_y = current_pos[1]+np.sin(current_pos[2])*self.v
        next_pos_heading = current_pos[2] + steering
        next_pos = (next_pos_x, next_pos_y, next_pos_heading)
        return next_pos
    
    def get_neighbors(self, current_pos):
        # neighbors = [ self.model(current_pos, 0.0), self.model(current_pos, self.steering_change/180.0*np.pi), self.model(current_pos, -self.steering_change/180.0*np.pi) ]
        neighbors = [ self.model(current_pos, 0.0, 0.2), self.model(current_pos, 20./180.0*np.pi, 0.2), self.model(current_pos, -20./180.0*np.pi, 0.2) ]        
        return neighbors
    
    def close_to_goal(self, current_cell):
        for i in xrange(3):
            if abs(current_cell[i] - self.goal_cell[i])>1:
                return False
        return True
        
    def Astar_path_generation(self):
        close_set = {}
        open_set = {self.start_cell: self.start} 
        ancestor = { (self.start, self.start_cell): None }
        moving_cost = { self.start_cell: 0.0 }
        total_cost = { (self.start, self.start_cell): self.heuristic(self.start) }
        open_q = Queue.PriorityQueue()
        open_q.put( ( total_cost[(self.start, self.start_cell)], self.start, self.start_cell ) )
        while len(open_set) > 0:
            current_node = open_q.get()
            current_pos = current_node[1]
            current_cell = current_node[2]

            self.visualize(current_pos, 'c:')
            print current_cell, self.goal_cell
            if self.close_to_goal(current_cell) :
                return self.reconstruct_path(current_pos, current_cell, ancestor)
            current_moving_cost = moving_cost[ current_cell ]
            del open_set[current_cell]
            close_set[ current_cell] = current_pos
            for neighbor in self.get_neighbors(current_pos):
                neighbor = tuple(neighbor)
                neighbor_cell = self.cont_2_dist(neighbor)
                
                neighbor_moving_cost = current_moving_cost + self.f_cost
                if neighbor_cell not in close_set:
                    if neighbor_cell in open_set:
                        if neighbor_moving_cost < moving_cost[ neighbor_cell ]:
                            moving_cost[ neighbor_cell] = neighbor_moving_cost
                            total_cost[ (neighbor, neighbor_cell) ] = neighbor_moving_cost + self.heuristic(neighbor)
                            open_q.put( (total_cost[ (neighbor, neighbor_cell) ], neighbor, neighbor_cell ) )    
                            ancestor[(neighbor, neighbor_cell)] =   (current_pos, current_cell)     

                    else:
                        open_set[neighbor_cell] = neighbor
                        moving_cost[ neighbor_cell] = neighbor_moving_cost
                        total_cost[ (neighbor, neighbor_cell) ] = neighbor_moving_cost + self.heuristic(neighbor)
                        open_q.put( (total_cost[ (neighbor, neighbor_cell) ], neighbor, neighbor_cell ) )    
                        ancestor[(neighbor, neighbor_cell)] =   (current_pos, current_cell)    
        print 'Path not found!!!!!!!!! '
        return False 
    def reconstruct_path(self, current_pos, current_cell, ancestor):
        print '------------Path found!'
        total_path = [current_pos]
        while ancestor[(current_pos, current_cell)] is not None:
            current_pos, current_cell = ancestor[(current_pos, current_cell)]
            # print current_pos, current_cell
            total_path += [ current_pos ]
        # print total_path
        for pos in reversed(total_path):
            self.visualize(pos, 'r--')
        pl.show()
    
def main():
    start = (0.0, 0.0, np.pi/2.0)
    goal =  (15.0, 15.0, np.pi/2.)
    planner = Astar(start, goal)
    # set up plotting 
    pl.figure(figsize=(8*1.1, 6*1.1))
    pl.plot(start[0], start[1], 'og', label = 'start')
    pl.plot(goal[0],  goal[1], '+g', label = 'end')
    pl.axis('equal')
    pl.grid('on')
    pl.xlabel('x (meters)')
    pl.ylabel('y (meters)')
    pl.legend(fancybox=True, framealpha=0.5)
    planner.visualize(start)
    planner.visualize(goal)
    

    path = planner.Astar_path_generation()
    print path
    
if __name__ == '__main__':
    main()  
