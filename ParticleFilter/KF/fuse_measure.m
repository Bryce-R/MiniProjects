function y = fuse_measure(Xk,v,i,dt,R_pos,R_vel)

y = [v*i*dt;
    v*cos(Xk(3))+sqrt(R_vel(1,1))*randn;
    v*sin(Xk(3))+sqrt(R_vel(2,2))*randn;
    Xk(1:2) + sqrtm(R_pos)*randn(2,1);
    ];

% y = [v*i*dt;
%     v*cos(Xk(3));
%     v*sin(Xk(3));
%     Xk(1:2) ;
%     ];



end