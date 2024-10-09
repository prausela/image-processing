function im = ifft2c(d)
% im = ifft2c(d)
%
% ifft2c performs a centered ifft2
%
im = ifftshift(ifft2(ifftshift(d)));

