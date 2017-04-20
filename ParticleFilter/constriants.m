function violation = constriants(Xk, const_pts_x, const_pts_y, L)
violation = 0;
Bicycle = [Xk(1:2) Xk(1:2)+[L*cos(Xk(3)); L*sin(Xk(3))] Xk(1:2)-[L*cos(Xk(3)); L*sin(Xk(3))]];
for i = 1:3
    X = Bicycle(:,i);
    if X(1)>= const_pts_x(1)-2 && X(1)<= const_pts_x(2)
        if X(2)< const_pts_y(1,1) || X(2)> const_pts_y(2,1)
            violation = 1;
        end
    elseif X(1)> const_pts_x(2) && X(1)<= const_pts_x(3)
        if X(2)< const_pts_y(1,3) || X(2)> const_pts_y(2,3)
            violation = 1;
        end
    elseif X(1)> const_pts_x(3) && X(1)<= const_pts_x(4)
        if X(2)< const_pts_y(1,4) || X(2)> const_pts_y(2,4)
            violation = 1;
        end
    else
        violation = 1;
    end
end

end