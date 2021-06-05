import json
import imagehash
import os


def readhashesfromdatabase():
    f= open('DataBase.json',)
    songsHash=json.load(f)
    return songsHash


def getHamming(hash1,hash2):
        return imagehash.hex_to_hash(hash1)-imagehash.hex_to_hash(hash2)


def compare(userSongHashes):
    similarityResults = {}
    database = readhashesfromdatabase()

    for i in database:
            melSpectrogram = 1-(getHamming(i['melspec'], userSongHashes['melSpectrogramHash']))/256.0
            mfcc = 1-(getHamming(i['mfcc'], userSongHashes['mfccHash']))/256.0
            avg = (melSpectrogram+mfcc)/2
            songname=i['name']
            similarity = avg*100
            similarityResults.update({songname: similarity})

    similarityResults = sorted(
        similarityResults.items(), key=lambda x: x[1], reverse=True)
    return similarityResults
    #print (similarityResults)
