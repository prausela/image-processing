%Restauracion de imagenes - Ejemplo 


% Blurred + Noised for testing refocusing algorithm.

clear all;


%degradation parameters


SNR_dB=10;                 %Signal to noise ratio 



%######################## Leo Imagen ####################################

%my_image = imread('barraxx.bmp');            %% Leo imagen 
%my_image = imread('barracuda_ok500.bmp');            %% Leo imagen 
%my_image = imread('d2.bmp');                           %% Leo imagen 
load lenna;
my_image = double(lenna)/256;

 

%############## Elimino color ##########################################

bw_my_image(:,:) = my_image(:,:,1);     %% Solo me quedo con la informacion  de grises


%#######################  P S F ' s  ###############################################

% ######################### My LOW PASS ################################################

% Creamos el nucleo de degradacion (Degradation kernel)
de_pix = 10;

for x = 1:(de_pix*2+1)
	for y = 1:(de_pix*2+1)
		if ((x-de_pix-1)^2+(y-de_pix-1)^2 <= de_pix*2);
			kernnel(x,y) = 1;
		else 
			kernnel(x,y) = 0;		
		end
	end
end

% Creamos una imagen del mismo tamanio de la imagen original para poder operar con la FFT.

imsize = size(bw_my_image);                  %Determino el  tamanio de la imagen original
rect_kernnel = zeros(imsize);                %La pongo en cero y le copio el Kernel . Esto es la PSF 
rect_kernnel(round(imsize(1)/2)-de_pix:round(imsize(1)/2)+de_pix,round(imsize(2)/2)-de_pix:round(imsize(2)/2)+de_pix) = kernnel;

%################################## Low pass Filters #######################

lpass=    [0  0  0;
           0  1  0;
           0  0  0];

lpass=1/9*[1  1  1;
           1  1  1;
           1  1  1];
       
lpass=1/5*[1/2  1/2  1/2;
           1/2  1    1/2;
           1/2  1/2  1/2];
       
lpass=1/16*[1  1  1;
            1  8  1;
            1  1  1];
       
lpass=1/12*[1  1  1;
            1  4  1;
            1  1  1];
       

h_Low_Pass=zeros(imsize);
h_Low_Pass(ceil(imsize(1)/2)-1:ceil(imsize(1)/2)+1,ceil(imsize(2)/2)-1:ceil(imsize(2)/2)+1)=lpass;


%################### Gausian PSF #############################

gks = 80;
gk = gausswin(max(imsize),gks);
gauss_kernnel = gk*gk';
gauss_kernnel = gauss_kernnel(round((max(imsize)-imsize(1))/2)+1:round((max(imsize)-imsize(1))/2)+imsize(1),round((max(imsize)-imsize(2))/2)+1:round((max(imsize)-imsize(2))/2)+imsize(2));


%################### PSF Selector  ###########################################



%blur_kernnel=rect_kernnel;
blur_kernnel=h_Low_Pass;
%blur_kernnel=gauss_kernnel;

%######################## Blurred Image =  H(w) * IMAGE(w) #############################################

% Convoluciono la imagen con la PSF (OTF) el dominio de la frecuencia y posteriormente antitransformo.
blurred_my_image = abs(ifft2c(fft2c(bw_my_image).*fft2c(blur_kernnel)));

%#############################  N O I S E  #############################################

sigma_burrled_image=std2(blurred_my_image);             % Encuentro la desviacion std de mi imagen
sigma_noise=sqrt((sigma_burrled_image)^2*10^(-SNR_dB/10));  % y junto con la SNR saco la desviacion std del ruido
noise=my_random(0,sigma_noise,imsize(1),imsize(2));               % para luego generar el ruido  
degraded_my_image = blurred_my_image + noise;      % Senial mas ruido !!!

%%%%%%%%%%%%%%%%%%%%%%%% Imagen Original %%%%%%%%%%%%%%%%%%%
figure(1) 
subplot(2,2,1)
imshow(bw_my_image,[]);
xlabel('Fig.2 a) Original image')

%%%%%%%%%%%%%%%%%%%%%%%% Imagen distorsionada mas ruido %%%%%%%%%%%%%%%%%%%

subplot(2,2,2)
imshow(degraded_my_image,[]);  
xlabel('Fig.2 b) Blurred and noised image')

%%%%%%%%%%%%%%%%%%%%%R E S T O R A T I O N (Wiener) %%%%%%%%%%%%%%%%%%%%%

% Deblurr the image using various kernnel

fft_kernnel = fft2c(blur_kernnel);
fft_degraded_my_image = fft2c(degraded_my_image);


%To implement the Wiener filter in practice we have to estimate the power spectra 
%of the original image and the additive noise.

%Power Spectra Density
psd_noise=fft2(corrcoef(noise));
psd_my_image=fft2(corrcoef(my_image));
inv_SNR=psd_noise./psd_my_image;

SNX_ESTIMATE=abs(inv_SNR)+25;


%SNX_ESTIMATE = mean(mean(abs(fft_kernnel.*conj(fft_kernnel))));



% Restore BY WIENER
restored_my_image = abs(ifft2c((fft_degraded_my_image.*conj(fft_kernnel))./(fft_kernnel.*conj(fft_kernnel)+SNX_ESTIMATE)));


subplot(2,2,3)
imshow(restored_my_image,[]);
xlabel('Fig.2 c) WIENER filter')



% Mediciones
SNR_improvement=10*log10(nmse(bw_my_image,degraded_my_image)/nmse(bw_my_image,restored_my_image)) % JAE S LIM pag 529


SNR_R=10*log10(std2(restored_my_image)^2/std2(noise)^2)
SNR_D=10*log10(std2(degraded_my_image)^2/std2(noise)^2)


diff = abs(restored_my_image - bw_my_image);
diffsqr = diff'*diff;
meandiffsqr = mean(mean(diffsqr));
SNR_restored_original = 10*log10(max(max(bw_my_image))/meandiffsqr)


std_err_Restored= std2(restored_my_image - bw_my_image)
std_err_Degraded= std2(degraded_my_image - bw_my_image)

% Calculate MSE of degraded image
error = degraded_my_image - bw_my_image;
sqerr = sum(sum(error.^2));
DMSE = sqerr/(imsize(1)^2)


% Calculate MSE of restored image
error = abs(restored_my_image) - bw_my_image;
sqerr = sum(sum(error.^2));
RMSE = sqerr/(imsize(1)^2)
