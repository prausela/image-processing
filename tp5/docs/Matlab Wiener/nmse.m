function norm_mse = NMSE(original,procesada)

            var_erro=std2(original-procesada)^2;
            var_orig=std2(original)^2;
            
            norm_mse=100*var_erro/var_orig; %JAE S LIM pag 529
            