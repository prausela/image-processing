
%devueve una matriz 2D numero aleatoreo entre 0 y 1 
%primer parametro:mu segundo:sigma
% tercero y cuarto las dimensiones de la matiriz

function x=my_random(mu,sigma,N,M)

            x=normrnd(mu,sigma,N,M);
            %x=x/max(max(abs(x)));