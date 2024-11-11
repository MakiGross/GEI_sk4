clc; clear all;
% Načtení obrázku mapy
mapa = imread('MMC07_sk4.jpg');  

% Zobrazení obrázku mapy a interaktivní výběr šablony
figure, imshow(mapa);
title('Vyberte oblast obsahující kostel jako šablonu');
h = imrect;  % Nástroj pro výběr obdélníku
position = wait(h);  % Čekání na potvrzení výběru oblasti

% Vystřižení šablony na základě vybrané oblasti
sab = imcrop(mapa, position);
figure, imshow(sab);  % Zobrazení vybrané šablony
title('Vybraná šablona kostela');


if size(mapa, 3) == 3
    mapaGray = rgb2gray(mapa);  % Převod mapy na stupně šedi
else
    mapaGray = mapa;
end

if size(sab, 3) == 3
    sab = rgb2gray(sab);  % Převod šablony na stupně šedi
end

% Normalizace kontrastu pro zlepšení výsledků 
mapaGray = imadjust(mapaGray);
sab = imadjust(sab);

% Zmenšení obrázků pro snížení paměťových nároků
scaleFactor = 0.5; 
mapaGray = imresize(mapaGray, scaleFactor);
sab = imresize(sab, scaleFactor);

% Výpočet normalizované křížové korelace na zmenšené černobílé verzi mapy
correlation = normxcorr2(sab, mapaGray);

% Nastavení prahové hodnoty 
korel_koef = 0.6;  % j 0.5, 0.7 

% Najdeme všechny body, kde korelace překročí prahovou hodnotu
[ypeak, xpeak] = find(correlation >= korel_koef);


yoffSet = ypeak - size(sab, 1);
xoffSet = xpeak - size(sab, 2);

% Zobrazení původní barevné mapy s obdélníky označujícími nalezené obce s kostelem
figure, imshow(imresize(mapa, scaleFactor)), title('Nalezené obce s kostelem');
hold on;
for i = 1:length(xoffSet)
    rectangle('Position', [xoffSet(i), yoffSet(i), size(sab, 2), size(sab, 1)], ...
              'EdgeColor', 'r', 'LineWidth', 2);
end
hold off;

% Výpis souřadnic nalezených kostelů

fid = fopen("souradnice.txt", 'w');
fprintf(fid, 'Souřadnice nalezených kostelů (x, y):\n');
for i = 1:length(xoffSet)
    fprintf(fid, 'Kostel %d: (x: %d, y: %d)\n', i, xoffSet(i), yoffSet(i));
end

fclose(fid);