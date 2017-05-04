function noise() 
    clear; clc; 
    %% Import all noise wav files to a Cell array
    n_fileList = dirPlus('/Users/jefflai108/clsp/spoken/noise/noise_data', 'FileFilter', '\.wav$');
    n_noise = length(n_fileList);
    
    %% Loop over every clean speech files, randomly choose one noise file and combine them together
    s_fileList = dirPlus('/Users/jefflai108/clsp/spoken/noise/flac_data_1', 'FileFilter', '\.flac$');
    n_speech = length(s_fileList);
    
    v_fileList = dirPlus('/Users/jefflai108/clsp/spoken/noise/vad_data_1', 'FileFilter', '\.txt$');
    n_vad = length(v_fileList);
    
    assert(n_vad==n_speech);
%     class(s_fileList(1))
%     class(n_fileList(randi(length(n_noise))))
%     class(char(v_fileList(1)))
%     random(char(s_fileList(1)),char(n_fileList(randi(length(n_noise)))),char(v_fileList(1)))

%     temp1 = strsplit(char(v_fileList(1)),'/')
%     temp2 = strsplit(char(temp1(8)),'.')
%     char(temp2(1))
    
    for i=1:n_speech 
        vad = v_fileList(i); 
        clean_speech = s_fileList(i); 
        noise = n_fileList(randi(length(n_noise)));
        [l, Fs] = random(char(clean_speech), char(noise), char(vad));
        temp1 = strsplit(char(vad),'/');
        temp2 = strsplit(char(temp1(8)),'.');
%         disp(strcat('/Users/jefflai108/clsp/spoken/noise/combined_data/',num2str(i),'.wav'))
        audiowrite(strcat('/Users/jefflai108/clsp/spoken/noise/combined_data_1/',char(temp2(1)),'.wav'),l,Fs)
    end 
    
    
    
    