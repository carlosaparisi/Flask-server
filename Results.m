% Load prerecorded data
clc;
clear;
close all;

% folder=cd('Vuelo Real'); %vuelo 1
% Log=load('2021-05-14 16-17-47.log-8232.mat');

% folder=cd('Vuelo simulado'); %Vuelo 2
% Log=load('2021-06-05 13-34-53.bin-4617.mat');

folder=cd('vuelo 1'); %Vuelo 3
Log=load('2021-06-12 12-38-52.bin-6529.mat');


ATT = Log.ATT;
CTUN = Log.CTUN;
RAD = Log.RAD;
NTUN = Log.NTUN;

GPS = Log.GPS;

t = [0:(ATT(end,2)-ATT(1,2))*10^-3/(length(ATT(:,1))-1):(ATT(end,2)-ATT(1,2))*10^-3];

% Representacions ATT

% Roll
figure(1)
plot(t,ATT(:,4),'r',t,ATT(:,3),'b'); % Roll real(vermell), Roll desitjat (blau)
grid on
grid minor 
%hold on
%xlim([0 160])
title('Angle Roll vs angle Roll desitjat');
legend('Roll','DesRoll');
ylabel('Angle roll [º]');
xlabel('temps [s]');

% Pitch/roll error 
figure(2)
plot(t(1:end-1),ATT(1:end-1,9)); 
grid on
grid minor 
title('Error pitch/roll');
ylabel('Error [0-1]');
xlabel('temps [s]');

% Pitch 
figure(3)
plot(t,ATT(:,6),'r',t,ATT(:,5),'b'); grid; % Pitch real(vermell), Pitch desitjat (blau)
grid on
grid minor 
title('Angle pitch vs angle pitch desitjat');
legend('Pitch','DesPitch');
ylabel('Angle pitch [º]');
xlabel('temps [s]');

% Yaw
figure(4)
plot(t,ATT(:,8),'r',t,ATT(:,7),'b'); grid; % Yaw real(vermell), Yaw desired (blau)
grid on
grid minor 
title('Angle Yaw vs angle Yaw desitjat');
legend('Yaw','DesYaw');
ylabel('Angle Yaw [º]');
xlabel('temps [s]');

%%altura

t = [0:(CTUN(end,2)-CTUN(1,2))*10^-3/(length(CTUN(:,1))-1):(CTUN(end,2)-CTUN(1,2))*10^-3];

figure(5)
plot(t,CTUN(:,7),'b',t,CTUN(:,6),'r'); grid; % 'Altura real segons el GPS (blau), altura desitjada (vermell)
grid on
grid minor 
title('Altura real segons el GPS vs altura desitjada');
legend('Alt','DAlt');
ylabel('Altura [m]');
xlabel('temps [s]');

figure(6)
plot(t,CTUN(:,8),'b',t,CTUN(:,6),'r'); grid; % Altura real segons baròmetre (blau), altura dessitjada (vermell)
grid on
grid minor 
title('Altura real segons el baròmetre vs altura desitjada');
legend('BAlt','DAlt');
ylabel('Altura [m]');
xlabel('temps [s]');

%PosX i posY
t = [0:(NTUN(end,2)-NTUN(1,2))*10^-3/(length(NTUN(:,1))-1):(NTUN(end,2)-NTUN(1,2))*10^-3];
figure(9)
plot(t,NTUN(:,5),'b',t,NTUN(:,3),'r'); grid; % Pos x real vs Pos x dessitjat
grid on
grid minor 
title('Posició en X');
legend('PosX','DPosX');
ylabel('Pos X [m]');
xlabel('temps [s]');
figure(10)
plot(t,NTUN(:,6),'b',t,NTUN(:,4),'r'); grid;  % Pos y real vs Pos y dessitjat
grid on
grid minor 
title('Posició en Y');
legend('PosY','DPosY');
ylabel('Pos Y [m]');
xlabel('temps [s]');


%% GPS

figure(7)
t = [0:(GPS(end,3)-GPS(1,3))*10^-3/(length(GPS(:,1))-1):(GPS(end,3)-GPS(1,3))*10^-3];
plot(t,GPS(:,6),'b',t,GPS(:,5),'r');
grid on
grid minor 
title('GPS Hdop i número de satèl·lits captats');
legend('Hdop','NumSat');
xlabel('temps [s]');

%% Link quality
figure(8)
t = [0:(RAD(end,2)-RAD(1,2))*10^-3/(length(RAD(:,1))-1):(RAD(end,2)-RAD(1,2))*10^-3];
signal_dBm1 = (RAD(:,3) / 1.9) - 127;
signal_dBm2 = (RAD(:,4) / 1.9) - 127;
signal_dBm3 = (RAD(:,6) / 1.9) - 127;
signal_dBm4 = (RAD(:,7) / 1.9) - 127;
plot(t,signal_dBm1,'b',t,signal_dBm2,'r',t,signal_dBm3,'g',t,signal_dBm4,'y');
grid on
grid minor 
title('Qualitat del radioenllaç');
legend('RSSI','RemRSSI','Noise','RemNoise');
xlabel('temps [s]');
ylabel('Potència [dBm]');


