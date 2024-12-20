clc, clear variables, format longG, close all;
%% JPEG komprese a dekomprese rastru
% loads images
img = imread("vzor1.jpg");
img = double(img);

q = 25; % compression factor %

[m, n, ~] = size(img);
m_pad = ceil(m / 8) * 8;  % Next multiple of 8 for rows
n_pad = ceil(n / 8) * 8;  % Next multiple of 8 for columns

% Pad the image to match the new dimensions
img_pad = padarray(img, [m_pad - m, n_pad - n], 'replicate', 'post');

%% COMPRESSION

% get RGB components
R = img_pad(:,:,1);
G = img_pad(:,:,2);
B = img_pad(:,:,3);

% conversion RGB to YCBCR
Y =   0.2990 * R + 0.5870*G + 0.1140 * B;
Cb = -0.1687 * R - 0.3313*G + 0.5    * B + 128;
Cr =  0.5    * R - 0.4187*G - 0.0813  *B + 128;

% interval transformation - roztáhnutí intervalu pro menší změny
% Y = 2* Y -255;
% Cb = 2* Cb - 255;
% Cr = 2*Cr - 255;

% resampling - ze zájmu

% DCT - +body za diskr. fast furier

% quantization matrix
Qy = [16 11 10 16 24 40 51 61
     12 12 14 19 26 58 60 55
     14 13 16 24 40 87 69 56
     14 17 22 29 51 87 80 62
     18 22 37 26 68 109 103 77
     24 35 55 64 81 104 113 92
     49 64 78 87 103 121 120 101
     72 92 95 98 112 100 103 99 ];
% chrominance matrix
Qc = [17 18 24 47 66 99 99 99
      18 21 26 66 99 99 99 99
      24 26 56 99 99 99 99 99
      47 69 99 99 99 99 99 99
      99 99 99 99 99 99 99 99
      99 99 99 99 99 99 99 99
      99 99 99 99 99 99 99 99
      99 99 99 99 99 99 99 99];

% updates qantisation matrices according to q
Q_y = (50*Qy)/q;
Q_c = (50*Qc)/q;

%[m,n] = size(Y);  % initialize compressed matrices

% process matrix by submatrices
for i = 1:8:m-7
    for j = 1:8:n-7
        % create submatrices
        Ysub = Y(i:i+7, j:j+7);
        Cbsub = Cb(i:i+7, j:j+7);
        Crsub = Cr(i:i+7, j:j+7);

        % apply myDCT
        Ydct = myDCT(Ysub);
        Cbdct = myDCT(Cbsub);
        Crdct = myDCT(Crsub);

        % quantisation
        Yq = Ydct./Q_c;
        Cbq = Cbdct./Q_y;
        Crq = Crdct./Q_y;

        % round and overwrite
        Yr(i:i+7, j:j+7) = round(Yq);
        Cbr(i:i+7, j:j+7) = round(Cbq);
        Crr(i:i+7, j:j+7) = round(Crq);

    end
end

%% DECOMPRESSION

% Dequantization and iDCT
for i = 1:8:m-7
    for j = 1:8:n-7

        % create submatrices
        Ysub = Yr(i:i+7,j:j+7);
        Cbsub= Cbr(i:i+7,j:j+7);
        CRsub= Crr(i:i+7,j:j+7);

        % dequantize
        Ydeq = Yq   .* Q_y;
        Cbdeq = Cbq .* Q_c;
        Crdeq = Crq .* Q_c;

        % apply iDCT
        YiDCT = myiDCT(Ydeq);
        CbiDCT = myiDCT(Cbdeq);
        CriDCT = myiDCT(Crdeq);

        % overwrite
        Y(i:i+7,j:j+7) = YiDCT;
        CB(i:i+7,j:j+7) = CbiDCT;
        CR(i:i+7,j:j+7) = CriDCT;    
    
    end
end

% YCbCr back to RGB
R2 = YiDCT + 1.402 * (CriDCT - 128);
G2 = YiDCT - 0.344136 * (CbiDCT - 128) - 0.714136 * (CriDCT - 128);
B2 = YiDCT + 1.772 * (CbiDCT - 128);

% decompressed image
img_rec = cat(3, R2, G2, B2);
img_rec = uint8(img_rec);  % Convert back to uint8 for display


%% display of resoults
figure;
subplot(1, 2, 1), imshow(uint8(img)), title('Original Image');
subplot(1, 2, 2), imshow(img_rec), title('Decompressed Image');

%%
%% funkce

function [RT]= myDCT(R)
RT = R;
% Output raster: rows
for u = 0:7
    if u == 0
        Cu = sqrt(2)/2;
    else Cu = 1;
    end
    % Output raster: columns
    for v = 0:7
        if v == 0
            Cv = sqrt(2)/2;
        else Cv = 1;
        end
    %Input raster: rows
    F = 0;
    for x = 0:7

        %Input raster: columns
        for y = 0:7
            F = F+ 1/4*Cu*Cv * (R(x+1,y+1) * cos(((2*x+1)*u*pi())/16) * cos(((2*y+1)*v*pi())/16));
        end
    end
    % output raster
    Rt(u+1,v+1) = F;

    end
end

end


function [R]= myiDCT(RT)
R = RT;
% Output raster: rows
for x = 0:7
    
    % Output raster: columns
    for y = 0:7
        
    %Input raster: rows
    F = 0;
    for u = 0:7
        if u == 0
             Cu = sqrt(2)/2;
        else 
            Cu = 1;
        end
        %Input raster: columns
        for v = 0:7
            if v == 0
                 Cv = sqrt(2)/2;
            else 
                Cv = 1;
            end
            F = F+ 1/4*Cu*Cv * (R(x+1,y+1) * cos(((2*x+1)*u*pi())/16) * cos(((2*y+1)*v*pi())/16));
        end
    end
    % output raster
    Rt(u+1,v+1) = F;

    end
end

end