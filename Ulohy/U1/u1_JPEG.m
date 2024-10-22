clc; clear all; format long g;

%Load image
ras1 = imread("Image2.bmp");
imshow(ras1);

q=100

%get RGB components
R=double(ras1(:,:,1));
G=double(ras1(:,:,2));
B=double(ras1(:,:,3));

%trasnformation RGB to YCC

Y=0.2990 * R + 0.5870 *  G + 0.1140 * B;
CB = -0.1687*R -0.3313 * G + 0.5000 *B +128;
CR = 0.5 * R -0.4187 * G - 0.0813*B +128;

%quantization matrix

Qy = [16 11 10 16 24 40 51 61
12 12 14 19 26 58 60 55
14 13 16 24 40 87 69 56
14 17 22 29 51 87 80 62
18 22 37 26 68 109 103 77
24 35 55 64 81 104 113 92
49 64 78 87 103 121 120 101
72 92 95 98 112 100 103 99];


%chrominance matrix

Qc = [17 18 24 47 66 99 99 99
18 21 26 66 99 99 99 99
24 26 56 99 99 99 99 99
47 69 99 99 99 99 99 99
99 99 99 99 99 99 99 99
99 99 99 99 99 99 99 99
99 99 99 99 99 99 99 99
99 99 99 99 99 99 99 99];

%update quantization matrices according to q

Qy = (50*Qy)/q;
Qc = (50*Qc)/q;
%proces input raster by sub-matrices
[m,n] = size(Y);

for i =1:8:m-7
    for j = 1:8:m-7

        %create tiles submatrices
        Ys = Y(i:i+7,j:j+7);
        CBs= CB(i:i+7,j:j+7);
        CRs= CR(i:i+7,j:j+7);
        %Apply DCT
        Ydct = mydct(Ys);
        CBdct = mydct(CBs);
        CRdct = mydct(CRs);

        
        %Quantization

        Yq = Ydct./Qc;
        CBq = CBdct./Qc;
        CRq = CRdct./Qc;
        
        %Round values
        Yqr = round(Yq);
        CBqr = round(CBq);
        CRqr = round(CRq);

        %Overwrite tile with the compressed one

        YT(i:i+7,j:j+7) = Yqr;
        CBT(i:i+7,j:j+7) = CBqr;
        CRT(i:i+7,j:j+7) = CRqr;

        

    end
end

%JPEG decompression

for i =1:8:m-7
    for j = 1:8:m-7

        %create tiles (submatrices)
        Ys = YT(i:i+7,j:j+7);
        CBs= CBT(i:i+7,j:j+7);
        CRs= CRT(i:i+7,j:j+7);
        
        %Dequantization
        Ysd = Ys./Qc;
        CBd = CBs./Qc;
        CRd = CRs./Qc;
        
        %Apply IDCT
        Yidct = myidct(Ysd);
        CBidct = myidct(CBd);
        CRidct = myidct(CRd);


        %Overwrite tile with the compressed one
        Y(i:i+7,j:j+7) = Yidct;
        CB(i:i+7,j:j+7) = CBidct;
        CR(i:i+7,j:j+7) = CRidct;
    end
end

%YCBCR to RGB

Rd = Y+1.4020*(CR-128);
Gd = Y-0.3441*(CB-128)-0.7141*(CR-128);
Bd = Y+1.7720*(CB-128)-0.0001*(CR-128);

%convert double to uint8

Ri = uint8(Rd);
Gi = uint8(Gd);
Bi = uint8(Bd);

%assembly raster from components
ras2(:,:,1)=Ri;
ras2(:,:,2)=Gi;
ras2(:,:,3)=Bi;

imshow(ras2);

%Compute standarts deviations
dR = R-Rd;
dG = G-Gd;
dB = B-Bd;

dR2 = dR.^2;
dG2 = dG.^2;
dB2 = dB.^2;

sigR=sqrt(sum(sum(dR2))/(m*n));
sigG=sqrt(sum(sum(dG2))/(m*n));
sigB=sqrt(sum(sum(dB2))/(m*n));




function Rt = mydct(R)
Rt = R;

%process input raster
for u = 0:7;
    %Cu
    if u ==0;
        Cu = sqrt(2)/2;
    else
        Cu =1;
    end
    
    %output raster: columns

 for v = 0:7
    %Cu
    if v == 0 
        Cv = sqrt(2)/2;
    else
        Cv =1;
    end

    %input raster: rows
    F = 0;
    for x = 0:7
        %input raster: columns
        for y = 0:7
            F=F+1/4*Cu*Cv*(R(x+1,y+1)*cos((2*x+1)*u*pi)/16)*cos((2*y+1)*v*pi/16);
        end
    end
    %Output raster
    Rt(u+1,v+1)=F;
  end
end

end






function Rt = myidct(R)
Rt = R;

%process input raster
for x = 0:7   
    %output raster: columns

 for y = 0:7
    

    %input raster: rows
    F = 0;
    for u = 0:7
        %Cu
    if u ==0
        Cu = sqrt(2)/2;
    else
        Cu =1;
    end
        %input raster: columns
        for v = 0:7
            %Cu
        if v == 0 
        Cv = sqrt(2)/2;
        else
        Cv =1;
        end
            F=F+1/4*Cu*Cv*(R(x+1,y+1)*cos((2*x+1)*u*pi)/16)*cos((2*y+1)*v*pi/16);
        end
    end
    %Output raster
    Rt(u+1,v+1)=F;
  end
end

end



