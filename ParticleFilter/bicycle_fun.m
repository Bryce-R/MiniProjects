function dx = bicycle_fun(t,x,L,v,delta)

dx = [v*cos(x(3)); v*sin(x(3)); v/L*tan(delta)];


end