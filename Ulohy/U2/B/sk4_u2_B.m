clc; clear all

% Načtení obrázku mapy
mapa = imread('TM25_sk4.jpg');  
figure, imshow(mapa), title('Původní mapa');

% Počet klastrů pro k-means segmentaci
numClusters = 8;  

% Segmentace obrazu pomocí k-means 
[pixel_labels, cluster_centers] = imsegkmeans(mapa, numClusters);

% Zobrazení výsledné segmentace v barevné formě
segmentedImage = label2rgb(pixel_labels);  
figure, imshow(segmentedImage), title(['Segmentace mapy']);

% Identifikace lesa:

[~, forestCluster] = min(mean(cluster_centers, 2));  


% Uložení výsledné masky jako obrázku
imwrite(segmentedImage, 'lesy_maska.png');

% lesy = mapa.*(uint8(pixel_labels==7));
% lesy(lesy==0) = 255;
% imshow(lesy);
% 
% save('lesy.mat','lesy','-mat')