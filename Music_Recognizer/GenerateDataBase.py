import json
import os
from tempfile import mktemp
from xml.etree.ElementTree import dump
from librosa.feature.spectral import chroma_stft
import matplotlib.pyplot as plt
import scipy as sp
from scipy.io import wavfile
from pydub import AudioSegment
import librosa
from PIL import Image
import imagehash
import json
#D:\DSP\MIIIXEER\Music_Recognizer\Group09\Group09_song1_full.mp3
directory= 'D:\DSP\MIIIXEER\Music_Recognizer\songs'
resultDirectory = 'D:\DSP\MIIIXEER\Music_Recognizer\spectrogram'
def spectrogram(audioData ,samplingFreq,filename ):
    fig = plt.figure()
    plt.specgram(audioData ,Fs=samplingFreq,NFFT=128 ,noverlap=0)
    savepath= resultDirectory+'\\' + filename + '.png'
    plt.savefig( savepath)

def mffcc_feature(audioData ,samplingFreq,filename):
    mfcc =librosa.feature.mfcc(audioData.astype('float64'), sr=samplingFreq)
    mfcc2= Image.fromarray(mfcc)
    #mfccHash = imagehash.phash(mfcc2)
    #mfccHash = str(mfccHash)
    return mfcc2


def mel_specgram_Feature(audioData , samplingFreq):
    mel_spectrogram=librosa.feature.melspectrogram(audioData.astype('float64') , sr=samplingFreq)
    mel_spectrogram2=Image.fromarray(mel_spectrogram)
    #mel_spectrogramHash= imagehash.phash(mel_spectrogram2)
    #mel_spectrogramHash=str(mel_spectrogramHash)
    return mel_spectrogram2

def generateHash(feature):
    featureHash= imagehash.phash(feature)
    featureHash= str(featureHash)
    return featureHash

def saveHashed(filename,mfccHash,melSpecgram):
    songHash ={
        'name' : filename,
        'mfcc': mfccHash,
        'mel_spec': melSpecgram
        
    }
    with open('DataBase.json','a') as jsonFile:
        json.dump(songHash ,jsonFile)
        jsonFile.write(os.linesep)

for filename in os.listdir(directory):
    path= directory + '\\' +filename
    #print(path)
    mp3Audio = AudioSegment.from_file(path, format="mp3")
    wname = mktemp('.wav')
    mp3Audio.export(wname,format="wav", parameters=[ "-ac", "1"])
    samplingFreq , audioData = wavfile.read(wname)
    #spectrogram(audioData,samplingFreq,filename)
    mfcc= mffcc_feature(audioData,samplingFreq ,filename)
    melSpecgram= mel_specgram_Feature(audioData , samplingFreq)
    mfccHash=generateHash(mfcc)
    melSpecgramHash = generateHash(melSpecgram)
    saveHashed(filename,mfccHash,melSpecgramHash)
print('finish')


    
    

