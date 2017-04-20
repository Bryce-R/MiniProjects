function dx = bicycle_est_fun(t,x,L,delta)
state = x(1:5,1);
P = reshape(x(6:end,1),5,5);

v = state(5);
theta = state(3);
dstate = [v*cos(theta); v*sin(theta); v/L*tan(delta); v; 0];

F = [0 0 -v*sin(theta) 0 cos(theta);
    0 0 v*cos(theta) 0 sin(theta);
    0 0 0 0 tan(delta)/L;
    0 0 0 0 1;
    0 0 0 0 0];
dP = F*P + P*F';

dx = [dstate; reshape(dP,25,1)];

end