function pt = add_prtcls(prtcls_up, jj, N_post, const_pts_x, const_pts_y, L)
while (1)
    k = mod(jj,N_post);
    if k == 0
        k = k+1;
    end
    new_pt = prtcls_up(:,k)+ [3*randn(1,1);3*randn(1,1);0];
    if ~(constriants(new_pt, const_pts_x, const_pts_y, L))
        pt = new_pt;
        break;
    end
end

end