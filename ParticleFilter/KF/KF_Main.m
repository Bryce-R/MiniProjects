%% Using Kalman filter to fuse info from wheel encoder
% steering position, GPS velocity and gps position
clc;
clear;
close all;


X0 = [0; 1.2; 0];
t0 =0;
dt= 0.05;
tf =15;
tt = t0:dt:tf;
k = length(tt);

X = zeros(3,k);
X(:,1) = X0;
v = 2;
delta = zeros(1,k-1);
c_width = 1.5;
XR = zeros(3,k);
for i = 1:floor(k/3)
    XR(:,i) = [2*i*dt; c_width ; 0];
end

for i = 1+floor(k/3):floor(2*k/3)
    XR(:,i) = [2*floor(k/3)*dt; c_width+2*(i-floor(k/3))*dt ; pi/2];
end

for i = 1+floor(2*k/3):k
    XR(:,i) = [2*floor(k/3)*dt+ 2*(i-floor(2*k/3))*dt; c_width+2*(floor(2*k/3)-floor(k/3))*dt ; 0];
end

%% Bicycle parameter
L = 1;
kp_pos = 2;

kp = 0.5; 
ki = 0.01;
kd = 0.2;
%% Measurement parameter
R_pos = diag([25 25]);
R_vel = diag([1 1]);
R = diag([1 1 1 25 25]);
%% EKF initialization
% x,y,theta,d(total distance traveled),v(parameter estimation)
Xhat0 = [0; 2.0; 0;0;1];
Xhat = zeros(5,k);
Xhat(:,1) = Xhat0;
Xh_pre = Xhat(:,1);
P0 = diag([10 10 0.2 1 1]);
P_pre = P0;
for i = 1:k-1
    Xk  = X(:,i);
    %%
    y = fuse_measure(Xk,v,(i-1),dt,R_pos,R_vel);
%     y = fuse_measure(Xk,v,i,dt,[0 0;0 0],[0 0;0 0]);
    vhat = Xhat(5,i); the_hat = Xhat(3,i);
    H = [0 0 0 1 0;
        0 0 -vhat*sin(the_hat) 0 cos(the_hat);
        0 0  vhat*cos(the_hat) 0 sin(the_hat);
        1 0 0 0 0;
        0 1 0 0 0];
    K = P_pre*H'/(H*P_pre*H' + R);
    %% Update 
    Xh_post = Xh_pre + K*(y - [Xh_pre(4); Xh_pre(5)*cos(Xh_pre(3)); Xh_pre(5)*sin(Xh_pre(3)); Xh_pre(1); Xh_pre(2)]);
    P_post = (eye(5) - K*H)*P_pre;

    %% System propagation
    
    dx_des = -kp_pos*(Xk(1) - XR(1,i));
    dy_des = -kp_pos*(Xk(2) - XR(2,i));
    the_des = atan2(dy_des,dx_des);
    delta(i) = -( kp*(Xk(3) - the_des) + kd*Xk(3) );
    [T,Y] = ode45(@bicycle_fun,[0 dt],Xk,[],L,v,delta(i));
    X(:,i+1) = Y(end,:)';
    %% Estimation propagation
    [T_est,Y_est] = ode45(@bicycle_est_fun,[0 dt],[Xh_post; reshape(P_post,25,1)],[],L,delta(i));
    Xh_pre = Y_est(end,1:5)';
    P_pre = reshape(Y_est(end,6:end),5,5);
    Xhat(:,i+1)= Xh_pre;


end

figure
plot(XR(1,:),XR(2,:),'r--','linewidth',1);
hold on;
xlabel('x'); ylabel('y'); grid on;
plot(X(1,:),X(2,:),'r-','linewidth',1.5);
plot(Xhat(1,:),Xhat(2,:),'b-','linewidth',1.5);



    
