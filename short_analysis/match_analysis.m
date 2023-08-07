hdr = hdrread ('HDR files/new_matched_noise_hdrs/4_10_perlinLL_HM_abandoned_workshop_02_2k_gray.hdr');
x=repmat (1:size(hdr,2),size(hdr, 1),1);
y=repmat( (1:size(hdr, 1))',1,size(hdr,2));
s=surf(x,y,hdr(:,:,1))
s.EdgeColor = 'none';
colorbar
