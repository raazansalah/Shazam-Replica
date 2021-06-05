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
directory= 'D:\DSP\DSP\Shazam\shazam finall inshallah\Music_Recognizer\songs'
resultDirectory = 'D:\DSP\DSP\Shazam\shazam finall inshallah\Music_Recognizer\spectrogram'
hash_array=[]
def spectrogram(audioData ,samplingFreq,filename ):
    fig = plt.figure()
    plt.specgram(audioData ,Fs=samplingFreq,NFFT=128 ,noverlap=0)
    savepath= resultDirectory+'\\' + filename + '.png'
    plt.savefig( savepath)

def mffcc_feature(audioData ,samplingFreq,filename):
    mfcc =librosa.feature.mfcc(audioData.astype('float64'), sr=samplingFreq)
    # mfcc2= Image.fromarray(mfcc)
    # mfccHash = imagehash.phash(mfcc2 ,hash_size=16)
    # mfccHash = str(mfccHash)
    return mfcc


def mel_specgram_Feature(audioData , samplingFreq):
    mel_spectrogram=librosa.feature.melspectrogram(audioData.astype('float64') , sr=samplingFreq)
    #mel_spectrogram2=Image.fromarray(mel_spectrogram)
    #mel_spectrogramHash= imagehash.phash(mel_spectrogram2)
    #mel_spectrogramHash=str(mel_spectrogramHash)
    return mel_spectrogram

def generateHash(feature):
    image= Image.fromarray(feature)
    featureHash= imagehash.phash(image,hash_size=16)
    featureHash= str(featureHash)
    return featureHash
    

def saveHashed(filename,mfccHash,melSpecgram):
    songHash={"name": filename,"mfcc": mfccHash,"melspec": melSpecgram}
    hash_array.append(songHash)
    return hash_array

for filename in os.listdir(directory):
    path= directory + '\\' +filename
    #print(path)
    mp3Audio = AudioSegment.from_file(path, format="mp3")
    wname = mktemp('.wav')
    mp3Audio.export(wname,format="wav")
    audioData,samplingFreq = librosa.load(wname,sr=22050 ,mono=True ,offset=0.0 ,duration=60)
    print(audioData)
    spectrogram(audioData,samplingFreq,filename)
    mfcc= mffcc_feature(audioData,samplingFreq ,filename)
    print(mfcc)
    melSpecgram= mel_specgram_Feature(audioData , samplingFreq)
    mfccHash=generateHash(mfcc)
    melSpecgramHash = generateHash(melSpecgram)
    arr=saveHashed(filename,mfccHash,melSpecgramHash)
    with open('DataBase.json', 'w') as outfile:
        json.dump(arr,outfile , indent=2)
print('finish')
