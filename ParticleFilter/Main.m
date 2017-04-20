%% Position estimation of a bicycle using map data

clc;
close all;
clear;

%% 
X0 = [0; 0.8; pi/6];
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
% Corridor

C_XUp = [XR(1:2,1)+[0; -c_width] XR(1:2,floor(k/3))+c_width*[1; -1] XR(1:2,floor(2*k/3))+c_width*[1; -1] XR(1:2,k)+c_width*[0; -1]];
C_XLow = [XR(1:2,1)+[0; c_width] XR(1:2,floor(k/3))+c_width*[-1; 1] XR(1:2,floor(2*k/3))+c_width*[-1; 1] XR(1:2,k)+c_width*[0; 1] ];


%% Bicycle parameter
L = 1;
kp_pos = 2;

kp = 0.5; 
ki = 0.01;
kd = 0.2;
for i = 1:k-1
    Xk  = X(:,i);
    dx_des = -kp_pos*(Xk(1) - XR(1,i));
    dy_des = -kp_pos*(Xk(2) - XR(2,i));
    the_des = atan2(dy_des,dx_des);
    delta(i) = -( kp*(Xk(3) - the_des) + kd*Xk(3) );
    [T,Y] = ode45(@bicycle_fun,[0 dt],Xk,[],L,v,delta(i));
    X(:,i+1) = Y(end,:)';
end

figure
plot(XR(1,:),XR(2,:),'r--','linewidth',1);
hold on;
plot(C_XUp(1,:),C_XUp(2,:),'-b','linewidth',3);
plot(C_XLow(1,:),C_XLow(2,:),'-b','linewidth',3);
xlabel('x'); ylabel('y'); grid on;
plot(X(1,:),X(2,:),'r-','linewidth',1.5);

const_pts_x = [0  XR(1,floor(k/3))-c_width  XR(1,floor(2*k/3))+c_width  XR(1,k)];  
const_pts_y = [0 0 0 XR(2,k)-c_width;
               c_width*2 c_width*2 XR(2,k)+c_width XR(2,k)+c_width]; 

% constriants([5;2.8;0], const_pts_x, const_pts_y, L)

%% particle filter initialization

particles = [0:0.1:9.9      10*ones(1,100)         10:0.1:19.9;
        c_width*ones(1,100) c_width:0.1:c_width+9.9 (c_width+10)*ones(1,100);
        X(3,1)*ones(1,300)];
plot(particles(1,:),particles(2,:),'k.','linewidth',1.5);
Est = zeros(3,k);    
Est(:,1) = mean(particles,2);
N = size(particles,2);
    
for i = 1:k-1
    i
    index = [];
    prtcls_up = [];
    for j = 1:N
        [T,Y] = ode45(@bicycle_fun,[0 dt],particles(:,j),[],L,v,delta(i)); 
        if ~(constriants(Y(end,:)', const_pts_x, const_pts_y, L))
            index = [index j];
            prtcls_up = [prtcls_up Y(end,:)'];
        end
    end
    N_post = size(index,2);
    
    Est(:,i+1) = mean(particles(:,index),2);
    plot(prtcls_up(1,:),prtcls_up(2,:),'.','color',[92 120 204]/255,'linewidth',1);
    plot(Est(1,i+1), Est(2,i+1), 'r+','linewidth',2);
    plot(X(1,i+1), X(2,i+1), 'b+','linewidth',2);
    title('Estimation: red +. True: blue +');
    N_toadd = N - N_post;
%     prtcls_up = [prtcls_up particles(:,index)];
    for jj = 1:N_toadd
        prtcls_up = [prtcls_up add_prtcls(prtcls_up, jj,N_post,const_pts_x, const_pts_y, L)];
    end
    particles = prtcls_up;
    drawnow;
    pause(0.01);
end

figure
plot(X(1,:),X(2,:),'r--','linewidth',2);
hold on;
plot(Est(1,:), Est(2,:), 'b--','linewidth',2);
plot(XR(1,:),XR(2,:),'r:','linewidth',1);
plot(C_XUp(1,:),C_XUp(2,:),'-b','linewidth',3);
plot(C_XLow(1,:),C_XLow(2,:),'-b','linewidth',3);
xlabel('x'); ylabel('y'); grid on;
legend('True','Estimation')
% plot(Est(1,:), Est(2,:), 'k+');





    

