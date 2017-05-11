// http://code.eng.buffalo.edu/dat/sites/model/bicycle.html
/*
compile using
gcc main.cpp  -std=c++0x -o main_terminal -lm -lsfml-graphics -lsfml-window -lsfml-audio -lsfml-network -lsfml-system -lstdc++
 */

#include <iostream>
#include "car.h"
#include <SFML/Graphics.hpp>
#include <random>
#include <chrono>
#include <thread>

double l2_norm(const std::vector<double> & v)
{
	double accum = 0.0;
	accum += v[0]*v[0] + v[1]*v[1];
	if (abs(v[2]) > M_PI)
	{
		accum += pow( 2*M_PI - abs(v[2]), 2); 
	}else
	{
		accum += pow(v[2], 2);
	}
	
	return sqrt(accum);
}

int main()
{
    // Create the main window
    sf::RenderWindow app(sf::VideoMode(800, 800), "Car RRT");

    double scale = 10.0;
	double car_width = 1.75*scale, car_length = 4.6*scale;
    // define a car_shape
    sf::RectangleShape car_shape(sf::Vector2f(car_width, car_length));
    car_shape.setOutlineColor(sf::Color(255,20,147));
    car_shape.setOutlineThickness(2);
    car_shape.setOrigin(car_width*0.5, car_length*0.5);

    // border
    sf::RectangleShape border(sf::Vector2f(700, 700));
    border.setOutlineColor(sf::Color(255,255,153)); //light yellow
    border.setOutlineThickness(1);
    border.setPosition(50,50);
    border.setFillColor(sf::Color(60,179,113));
    //path
	sf::Vertex line[] =
	{
    	sf::Vertex(sf::Vector2f(0, 0)),
    	sf::Vertex(sf::Vector2f(0, 0))
	};




    car sentra(car_width, car_length);
    std::vector<double> state {50.0+2*car_width, 50.0+car_length, -45.0/180.0*M_PI};
    std::vector<double> goal_state {300.00, 300.00, 180.0/180.0*M_PI};
    std::vector< std::vector<double> > control_actions;
    std::vector<double> speed_actions {-1.0, -0.5, 0.0, 0.5, 1.0};
    std::vector<double> turning_actions {0.0};
    std::vector<int> path;
    for (int i= 0; i<10; i++)
    {
    	turning_actions.push_back((static_cast<double>(i)+1.0)*2.0/180*M_PI);
    	turning_actions.push_back(-(static_cast<double>(i)+1.0)*5.0/180*M_PI);
    }

    for (double speed: speed_actions)
    {
    	for (double turning_angle: turning_actions)
    	{
    		std::cout << "turning_actions: "<<turning_angle << "\n";
    		control_actions.push_back( std::vector<double> {speed, turning_angle} );
    	}
    }


    std::mt19937 rng;
    rng.seed(std::random_device()());
    std::uniform_int_distribution<std::mt19937::result_type> dist6(0,control_actions.size()-1); 
    double dt = 2.0;

    // RRT tree nodes generation
    double x_lowerbound = 100.0, y_lowerbound = 100.0;
    double x_upperbound = 350.0, y_upperbound = 350.0;
    std::uniform_real_distribution<double> unif_x(x_lowerbound,x_upperbound);
    std::uniform_real_distribution<double> unif_y(y_lowerbound,y_upperbound);
    std::uniform_real_distribution<double> unif_theta(0.0,360.0/180.0*M_PI);



    std::vector< std::vector<double> > nodes; 
    nodes.push_back(state);
    std::map <int, int> ancestor;
    int path_index = 0;




	// Start the game loop
    while (app.isOpen())
    {
        // Process events
        sf::Event event;
        while (app.pollEvent(event))
        {
            // Close window : exit
            if (event.type == sf::Event::Closed)
                app.close();
        }

        if (path.size() == 0)
        {  

        int i = dist6(rng); 
    	std::random_device rd;  //Will be used to obtain a seed for the random number engine
    	std::mt19937 gen(rd()); //Standard mersenne_twister_engine seeded with rd()
        vector<double> point_random;
        point_random.push_back(unif_x(gen));
        point_random.push_back(unif_y(gen));
        point_random.push_back(unif_theta(gen)/180*M_PI);
         // {unif_x(gen), unif_y(gen), unif_theta(gen)/180*M_PI};
        std::cout << "Random point: "<<point_random[0] << " " <<point_random[1] << " " << point_random[2]/M_PI*180.0 <<"\n";

        int i_closest = 0, i_next = 0;
        double min_dis = 1600.0;
        std::vector<double> closest_pt(3,0);
        for (int i =0; i< nodes.size(); i++)
        {
        	if (l2_norm(nodes[i]-point_random) < min_dis)
        	{
        		min_dis = l2_norm(nodes[i] - point_random);
        		i_closest = i;
        	}
        }
        min_dis = 1600.0;
        std::vector<double> node_next(3,0);
        for (int i = 0; i<control_actions.size(); i++)
        {
        	std::vector<double> state_next = sentra.car_int(dt, nodes[i_closest], control_actions[i][0], control_actions[i][1]);
        	if (l2_norm(state_next - point_random) < min_dis)
        	{
        		min_dis = l2_norm(state_next - point_random);
        		node_next = state_next;
        	}
        }
        nodes.push_back(node_next);
        std::cout << "Next point: "<<node_next[0] << " " <<node_next[1]<<"\n";
		ancestor[nodes.size()-1] = i_closest;


    	// execute control
        std::cout <<"x = " <<state[0] << ". y = " << state[1] << ". heading: " << state[2]/M_PI*180.0 << " \n"; 
        std::cout <<"Vel = " <<control_actions[i][0] << ". Turning angle = " << control_actions[i][1]/M_PI*180.0 << " \n"; 
        state = sentra.car_int(dt, state, 0.00*control_actions[i][0], control_actions[i][1]);


        if ( l2_norm(node_next - goal_state) <8 )
        {
        	int i = nodes.size()-1;
        	while (i!=0)
        	{
        		path.insert(path.begin(),i);
        		i = ancestor[i];
        	}
        }

    	}else{
    		if (path_index >= path.size())
    		{
    			path_index = 0;
    			std::this_thread::sleep_for(std::chrono::milliseconds(200));
    		}
    	    	car_shape.setPosition(nodes[path[path_index]][0], nodes[path[path_index]][1]);
        		car_shape.setRotation(static_cast<int>(nodes[path[path_index]][2]/M_PI*180.0));
        		car_shape.setFillColor(sf::Color::Blue);
        		app.display();
        		path_index += 1;
        		std::cout << "Current node: " << path_index << "\n";
        		std::this_thread::sleep_for(std::chrono::milliseconds(20));
        		// int fakenum;
        		// std::cin >> fakenum;
    		}



        // Clear screen
        app.clear();
        app.draw(border);
        // draw path
        app.draw(car_shape);
        // draw car
        car_shape.setPosition(state[0], state[1]);
        car_shape.setRotation(static_cast<int>(state[2]/M_PI*180.0));
        car_shape.setFillColor(sf::Color::Blue);
        app.draw(car_shape);

        car_shape.setPosition(goal_state[0], goal_state[1]);
        car_shape.setRotation(static_cast<int>(goal_state[2]/M_PI*180.0));
        car_shape.setFillColor(sf::Color::Transparent);
        app.draw(car_shape);

        // if (path.size() >0)
        // {
        // 	for (int i: path)
        // 	{
        // 		car_shape.setPosition(nodes[i][0], nodes[i][1]);
        // 		car_shape.setRotation(static_cast<int>(nodes[i][2]/M_PI*180.0));
        // 		car_shape.setFillColor(sf::Color::Blue);
        // 		app.draw(car_shape);
        // 		app.display();
        // 	}
        // }

        std::cout << "-----------No. of nodes in RRT: " << nodes.size() << "\n";
        for (int i =0; i< nodes.size()-1; i++)
        {
        	sf::Vertex line[] =
			{
    			sf::Vertex( sf::Vector2f(nodes[i][0], nodes[i][1]) ),
    			sf::Vertex( sf::Vector2f(nodes[ancestor[i]][0], nodes[ancestor[i]][1]) )
			};
			app.draw(line,2,sf::Lines);
        }
        // Update the window
        app.display();



    }

    return EXIT_SUCCESS;
}
