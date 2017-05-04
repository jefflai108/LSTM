function [l, Fs] = random(clean_speech, noise, vad)
%% Combine the given clean speech and noise files and return the combined signal 

    clean_speech = '/Users/jefflai108/clsp/spoken/noise/flac_data_1/103/1240/103-1240-0000.flac';
    noise =  '/Users/jefflai108/clsp/spoken/noise/noise_data/airport/100842__lonemonk__las-vegas-airport-lounge-section-1.wav';
    vad = '/Users/jefflai108/clsp/spoken/noise/vad_data_1/103-1240-0000.txt'; 

    %% Extract the same length of noise signal as the clean speech signal from the noise files
    [s, Fs] = audioread(clean_speech);
    [n, Fn] = audioread(noise); 
    
    assert(length(n)>length(s),'clean speech files is larger than noise file');
    
    rand = randi(length(n)-length(s));
    n = n(rand:rand+length(s)-1);
    
    %% Choose a random Signal to Noise Ratio between uniform distribution (-3dB,30dB). 
    SNR = randi([-3,30]);
    SNR = 0;
    
    %power for each frame 
    M = Fs/1000*25; %number of sample per 25ms frame 
    N = Fn/1000*10; %number of sample per 10ms frame_shift
    N_frame = (length(s)-M)/N+1; %number of frames
    s_frame_power = [];
    n_frame_power = [];
    
    for i=1:N_frame
        s_frame_power(end+1) = mean(s((i-1)*N+1:(i-1)*N+M).^2);
        n_frame_power(end+1) = mean(n((i-1)*N+1:(i-1)*N+M).^2);
    end
    
    %signal power and noise power 
    vad = transpose(importdata(vad));
    
    if length(vad) > length(s_frame_power)
        vad = vad(1:length(s_frame_power));
    end 

    Ps = mean(s_frame_power(vad==1));
    Pn = mean(n_frame_power(vad==1));

    %% Calculate the gain A from SNR; SNR = 10*log(Ps/A^2*Pn)
    A = sqrt(Ps/Pn/10^(SNR/10));
    
    %% Combine the signals using Ps, Pn
    l = s + A*n;
    
    subplot(3,1,1)
    x = linspace(1,10,length(s));  
    plot(x,s)
    title('clean speech');
    subplot(3,1,2)
    x = linspace(1,10,length(n));  
    plot(x,n)
    title('noise');
    subplot(3,1,3)
    x = linspace(1,10,length(l));  
    plot(x,l)
    title('Combined');
    
    savefig('exp1_result.fig');