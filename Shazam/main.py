from typing import DefaultDict
from PyQt5 import QtWidgets, QtCore, uic, QtGui, QtPrintSupport
from pyqtgraph import PlotWidget, plot
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import *   
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from os import path
import pandas as pd
import numpy as np
import sys
import os
import matplotlib.pyplot as plot
import librosa 
from pydub import AudioSegment
from tempfile import mktemp
import librosa.display
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import imagehash
from PyQt5.QtWidgets import QTableWidget   
import pylab
from comparee import compare

MAIN_WINDOW,_=loadUiType(path.join(path.dirname(__file__),"main.ui"))

class MainApp(QMainWindow,MAIN_WINDOW):
  
    def __init__(self,parent=None):
        super(MainApp,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.similarties={}
        self.Buttons= [self.Browse1 , self.Browse2 , self.Identify]
        self.Buttons[2].setDisabled(True) 
        self.Table= [self.song_1,self.song_2,self.song_3,self.song_4,self.song_5,self.song_6,self.song_7,self.song_8,self.song_9,self.song_10]
        self.songs= [None,None]
        self.outMix= None
        self.Buttons[0].clicked.connect(lambda : self.readSong(1) )
        self.Buttons[1].clicked.connect(lambda : self.readSong(2) )
        self.Buttons[2].clicked.connect(self.songMixer)


    def readSong(self,songNumber):
      fileName= QFileDialog.getOpenFileName( self, 'choose the signal', os.getenv('HOME') ,"mp3(*.mp3)" ) 
      self.path = fileName[0] 
      
      if self.path =="" :
          return
      modifiedAudio = AudioSegment.from_file( self.path , format="mp3") # read mp3
      wname = mktemp('.wav')  # use temporary file
      modifiedAudio.export(wname, format="wav")  # convert to wav

      if songNumber == 1:
        self.firstSongName.setText(os.path.splitext(os.path.basename(self.path))[0])
        self.song1Data,self.samplingFrequency1 = librosa.load(wname,sr=22050 ,mono=True ,offset=0.0 ,duration=60)
        
        self.songs[0]= self.song1Data
        self.Buttons[2].setDisabled(False) 
        print("Song1 read ")
        #print(self.song1Data)

      elif songNumber == 2 :
        self.secondSongName.setText(os.path.splitext(os.path.basename(self.path))[0])
        self.song2Data,self.samplingFrequency2 =audioData,samplingFreq = librosa.load(wname,sr=22050 ,mono=True ,offset=0.0 ,duration=60)
        self.songs[1]= self.song2Data
        self.Buttons[2].setDisabled(False) 
        print("song2 read")

        for i in range (10):
            self.Table[i].clear()
        
    def songMixer(self) :
        sliderRatio = self.mixerSlider.value()/100

        if (self.songs[0] is not None) and (self.songs[1] is not None):
            self.outMix = self.songs[0] * sliderRatio + self.songs[1] * (1-sliderRatio)
        
        else:
            if self.songs[0] is not None : self.outMix = self.songs[0]
            if self.songs[1] is not None: self.outMix = self.songs[1]
           
        self.spectrogram()

    def spectrogram (self):
        
        
        Spectro_Path = 'mixSpectrogram.png'
        pylab.axis('off')  # no axis
        pylab.axes([0., 0., 1., 1.], frameon=False, xticks=[], yticks=[])  # Remove the white edge
        D = librosa.amplitude_to_db(np.abs(librosa.stft(self.outMix)), ref=np.max)
        librosa.display.specshow(D, y_axis='linear')
        pylab.savefig(Spectro_Path, bbox_inches=None, pad_inches=0)
        pylab.close()
        self.features()

    def features (self): 
      
      #mfcc 
      pylab.axis('off')  
      pylab.axes([0., 0., 1., 1.], frameon=False, xticks=[], yticks=[])
      SavePath = 'mfcc.png'
      feature1= librosa.feature.mfcc(y=self.outMix, sr=self.samplingFrequency1)
      #print(feature1)
      Image1=Image.fromarray(feature1)
      Hash1=imagehash.phash(Image1,hash_size=16)
      Hash1=str(Hash1)
      #print(Hash1)
      librosa.display.specshow(feature1.T,sr=self.samplingFrequency1 )
      pylab.savefig(SavePath, bbox_inches=None, pad_inches=0)
      pylab.close()

      #melspectrogram
      pylab.axis('off') 
      pylab.axes([0., 0., 1., 1.], frameon=False, xticks=[], yticks=[]) 
      SavePath ='melspectrogram.png'
      feature2= librosa.feature.melspectrogram(y=self.outMix, sr=self.samplingFrequency1)
      #print (feature2)
      Image2=Image.fromarray(feature2)
      Hash2=imagehash.phash(Image2,hash_size=16)
      Hash2=str(Hash2)
      #print(Hash2)
      librosa.display.specshow(feature2.T,sr=self.samplingFrequency1 )
      pylab.savefig(SavePath, bbox_inches=None, pad_inches=0)
      pylab.close()
      self.generateFingerprintUser(Hash1,Hash2)
    def generateFingerprintUser(self,featureHash1,featureHash2):

        SongHashesUser = {"mfccHash":'',"melSpectrogramHash" : ""}
        SongHashesUser["mfccHash"] = str(featureHash1)
        SongHashesUser["melSpectrogramHash"] = str(featureHash2)
        print(SongHashesUser["mfccHash"])
        print(SongHashesUser["melSpectrogramHash"])
        self.similarties=compare(SongHashesUser)
        print(self.similarties)
        self.Tableconstruct()

    def Tableconstruct(self):
        for i in range(len(self.Table)):
                self.Table[i].setText(str(self.similarties[i][0])+'--->Similarty index='+str(self.similarties[i][1])+'%')
                #print(self.similarties[i][i])
          
        
def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())


if __name__=='__main__':
    main()