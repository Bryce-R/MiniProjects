#ifndef CAR_H
#define CAR_H

#include <vector>
#include <cmath>
#include <algorithm>
#include <functional>
using namespace std;
// overload vector operations for plus and multiplication
std::vector<double> operator+(const std::vector<double>& v1, const std::vector<double>& v2)
{
    std::vector<double> v_sum(v1.size(),0);
    std::transform(v1.begin(), v1.end(), v2.begin(), v_sum.begin(), std::plus<double>());
    return v_sum;
}

std::vector<double> operator-(const std::vector<double>& v1, const std::vector<double>& v2)
{
    std::vector<double> v_sum(v1.size(),0);
    std::transform(v1.begin(), v1.end(), v2.begin(), v_sum.begin(), std::minus<double>());
    return v_sum;
}

std::vector<double> operator*(const vector<double>& v1, const double scale)
{
    std::vector<double> v(v1.size(),0);
    std::transform(v1.begin(), v1.end(), v.begin(),
        std::bind1st(std::multiplies<double>(), scale));
    return v;
}

class car{
    double car_width, car_length;

public:
    car(double width, double length): car_width(width), car_length(length) {}
    double get_width() {return car_width;}
    double get_length() {return car_length;}
    vector<double> car_dyn(const vector<double>& state, const double & vel, const double& turn_angle);
    vector<double> car_int(const double &dt, const vector<double> & state, const double & vel, const double & turn_angle);
};

std::vector<double> car::car_dyn(const vector<double>& state, const double & vel, const double& turn_angle)
{
    vector <double> d_state(state.size(),0);
    double heading_angle = state[2];
    d_state[0] = (-vel*std::sin(heading_angle));
    d_state[1] = (vel*std::cos(heading_angle));
    d_state[2] = (vel/car_length)*std::tan(turn_angle);

    // std::cout << " Dyn: "<<d_state[0] << " " << d_state[1] << " " << d_state[2] << " \n"; 
    return d_state;
}

std::vector<double> car::car_int(const double& dt, const vector<double>& state, const double& vel, const double & turn_angle)
{
    int n = state.size();
    std::vector<double> k_1(n,0), k_2(n,0), k_3(n,0), k_4(n,0), state_next(n,0);
    k_1 = car_dyn(state, vel, turn_angle);
    k_2 = car_dyn(state + k_1*(dt/2.0), vel, turn_angle);
    k_3 = car_dyn(state + k_2*(dt/2.0), vel, turn_angle);
    k_4 = car_dyn(state + k_3*(dt), vel, turn_angle);
    state_next = state + (k_1 + k_2*2.0 + k_3*2.0 + k_4)*(dt/6);
    // std::cout << " int: "<<state_next[0] << " " << state_next[1] << " " << state_next[2] << " \n";  
    return state_next;
}
#endif // CAR_H
