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
        self.Car = Car.Car(2.66, 1.5, 1.0, start, 5.5) 
        self.Car.visualize_as_center = False
        self.model = self.Car.integrate_car
        self.visualize = self.Car.visualize
        self.heuristic_func = 'norm_dis_augmented'
        self.reconstruct = True

    def set_start(self, start):
        self.start = start
        self.start_cell = self.cont_2_dist(start)
        
    def set_goal(self, goal):
        self.goal = goal
        self.goal_cell = self.cont_2_dist(goal)
        
    def cont_2_dist(self, current_pos):
        current_cell = (np.floor(current_pos[0]/self.cellsize[0]), np.floor(current_pos[1]/self.cellsize[1]), np.floor(current_pos[2]/self.cellsize[2]) )
        return current_cell
    
    def euclidean_dis(self, current):
        cost = np.sqrt( (current[0] - self.goal[0])**2 + (current[1] - self.goal[1])**2 )
        return cost
    def norm_dis(self, current):
        theta = self.goal[2]
        current = list(current)
        current[2] -= theta
        current[0] -= self.goal[0]
        current[1] -= self.goal[1]
        current[0], current[1] = (np.cos(theta)*current[0]+np.sin(theta)*current[1],  -np.sin(theta)*current[0]+np.cos(theta)*current[1]) 
        print current 
        w_x, w_y, w_theta = 10.0, 10.0*2., 35.0*2.
    
        if current[0] <=0:
            cost_h = np.sqrt( (current[0])**2*w_x**2 + (current[1])**2*w_y**2 ++ (current[2])**2*(w_theta)**2 )
        else:
            cost_h = float('inf')
        return cost_h
    def norm_dis_augmented(self, current):
        theta = self.goal[2]
        current = list(current)
        current[0] -= self.goal[0] #x
        current[1] -= self.goal[1] #y
        current[2] -= theta #heading 
        current[0], current[1] = (np.cos(theta)*current[0]+np.sin(theta)*current[1],  -np.sin(theta)*current[0]+np.cos(theta)*current[1]) 
        # w_x, w_y, w_theta = 10.0, 10.0, 35.0
        # # w_x, w_y, w_theta = 10.0, 15.0, 35.0
        w_x, w_y, w_theta = 10.0, 10.0*3, 35.0*3
        # print current 
        # assert False
        if abs(current[1]) > self.Car.min_turn_radius:
            print 'outside min turning radius'
            w_x, w_y, w_theta = 10.0, 300.0, 35.0
            cost_h = np.sqrt( (current[0] - np.sin(current[2])*self.Car.min_turn_radius )**2*w_x**2 + (current[1])**2*w_y**2 ++ (current[2])**2*(w_theta)**2 )
        elif current[0] <=0 and abs(current[0]) > np.sin(current[2])*self.Car.min_turn_radius :
            print 'inside turning radius'
            cost_h = np.sqrt( (current[0])**2*w_x**2 + (current[1])**2*w_y**2 ++ (current[2])**2*(w_theta)**2 )
        else:
            cost_h = float('inf')
        print current, cost_h
        return cost_h
    
    def heuristic(self, current):
        if self.heuristic_func == 'norm_dis':
            return self.norm_dis(current)
        elif self.heuristic_func == 'norm_dis_augmented':
            return self.norm_dis_augmented(current)
        elif self.heuristic_func == 'euclidean_dis':
            return self.euclidean_dis(current)
    def moving_cost(self, current):
        theta = self.start[2]
        current = list(current)
        current[0] -= self.start[0]
        current[1] -= self.start[1]
        current[2] -= theta
        current[0], current[1] = (np.cos(theta)*current[0]+np.sin(theta)*current[1],  -np.sin(theta)*current[0]+np.cos(theta)*current[1]) 
        w_x, w_y, w_theta = 10.0, 20.0, 35.0*2
        # cost_h = np.sqrt( (current[0]- self.start[0])**2*w_x**2 + (current[1] - self.start[1])**2*w_y**2 ++ (current[2]- self.start[2])**2*(w_theta)**2 )
        cost_h = np.sqrt( (current[0])**2*w_x**2 + (current[1])**2*w_y**2 ++ (current[2])**2*(w_theta)**2 )
        return cost_h
    
    def euler_int_model(self, current_pos, steering):
        next_pos_x = current_pos[0]+np.cos(current_pos[2])*self.v
        next_pos_y = current_pos[1]+np.sin(current_pos[2])*self.v
        next_pos_heading = current_pos[2] + steering
        next_pos = (next_pos_x, next_pos_y, next_pos_heading)
        return next_pos
    
    def get_neighbors(self, current_pos):
        # neighbors = [ self.model(current_pos, 0.0), self.model(current_pos, self.steering_change/180.0*np.pi), self.model(current_pos, -self.steering_change/180.0*np.pi) ]
        max_turn = 1/2.66*(np.tan(25./180.0*np.pi))
        neighbors = [ self.model(current_pos, 0.0, 0.2), self.model(current_pos, max_turn, 0.2), self.model(current_pos, -max_turn, 0.2) ]        
        return neighbors
    
    def close_to_goal(self, current_cell):
        for i in xrange(3):
            if abs(current_cell[i] - self.goal_cell[i])>2:
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
            if current_cell in close_set:
                continue

            self.visualize(current_pos, 'c:')
            print current_cell, self.goal_cell, current_pos
            if self.close_to_goal(current_cell) :
                if self.reconstruct is True:
                    self.reconstruct_path(current_pos, current_cell, ancestor)
                return True
            current_moving_cost = moving_cost[ current_cell ]
            del open_set[current_cell]
            close_set[ current_cell] = current_pos
            for neighbor in self.get_neighbors(current_pos):
                neighbor = tuple(neighbor)
                neighbor_cell = self.cont_2_dist(neighbor)
                
                neighbor_moving_cost = self.moving_cost(neighbor) #current_moving_cost + self.f_cost
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
        # pl.show()
        return 
    
def main():
    start = (0.0, 0.0, np.pi/2.0)
    goal =  (16.0, 16.0, 0.)

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
    
    
    goal_set = []
    goal_set+= [(11.0, 0.0, -np.pi/2.), (-5.5, 5.5, np.pi) ,(12.5, 5.5, 0.) ]
    # goal_set+= [ (5.5, 16.5, 0.) ]
    # goal_set+= [ (5.5, 6.5, 0.) ]
    # goal_set += [(0.0, 3.0, np.pi/2.)]
    planner.heuristic_func = 'norm_dis'
    
    
    
    
    # planner.heuristic_func = 'norm_dis'
    # goal =  (5.5, 2.5, 0.)
    # goal = (1.0, 5.0, np.pi/2.0)
    planner.visualize(start)
    planner.reconstruct = False
    for goal in goal_set:
        print '----------New goal--------'
        planner.set_goal( goal ) 
        planner.visualize(goal)
        path = planner.Astar_path_generation()
        
    pl.show()

    
    # print path
    
if __name__ == '__main__':
    main()  
