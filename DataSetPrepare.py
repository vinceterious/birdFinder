import sys
import skimage.io
import numpy as np
import librosa
from sklearn.preprocessing import minmax_scale
from pathlib import Path
import XenoCantoRestApi
from tqdm import tqdm

class DataSetPrepare:
    def __init__(self, retrieveXenoCantoAPISampleList):
        self.r = retrieveXenoCantoAPISampleList
        self.y = {}
    def cropImg(self, img, hSize, wSize):
        return img[0:hSize, 0:wSize]

    def repeatImgUntilWSizeDesired(self, img, wSizeDesired):
        hSize = img.shape[0]
        w = img.shape[1]
        numberOfRepetition = (wSizeDesired // w) + 1
        blank_image2 = 255 * np.ones(shape=(hSize, (numberOfRepetition)*w), dtype=np.uint8)
        for idx in range(0, numberOfRepetition):
            blank_image2[0:hSize, w*idx:w*idx+w] = img
        return self.cropImg(blank_image2, hSize, wSizeDesired)

    def shapeImg(self, img):
        hImg =128
        wImg = 1024
        w = img.shape[1]
        if w < wImg:
            return self.repeatImgUntilWSizeDesired(img, wImg)
        else:
            return self.cropImg(img,hImg,wImg)

    def generateLabelFromPath(self, filePath):
        x = str(filePath).split('/')
        l = x[1] + "," + x[2]
        if l not in self.y:
            self.y[l] = len(self.y)
        return int(self.y[l])

    def preprocessImg(self, inFile):
        img = skimage.io.imread(inFile)
        sizeImg = self.shapeImg(img)
        sizeNorma = np.ndarray(shape=sizeImg.shape, dtype=float)
        sizeNorma = sizeImg / 255.0
        #print(str(file) + " Shape: " + str(sizeImg.shape[:2]))
        return sizeNorma

    def generateDataSet(self):
        label = []
        imgDataSet = []
        files = list(Path(self.r.dirSound).rglob("*.png"))
        for file in tqdm(files):
            with open(file, "r") as f:
                label.append(self.generateLabelFromPath(file))
                imgDataSet.append(self.preprocessImg(file))
        print(self.y)
        return label, imgDataSet

    def createSpectrograme(self, inSoundFile):
        y, sr = librosa.load(inSoundFile)
        mels = librosa.feature.melspectrogram(y=y, sr=sr)
        mels = np.log(mels + 1e-9)
        img = minmax_scale(mels, feature_range=(0, 255)).astype(np.uint8)
        img = np.flip(img, axis=0) # put low frequencies at the bottom in image
        img = 255-img # invert. make black==more energy
        return img

    def createAllSpectrogramesInDirDataSet(self):
        files = list(Path(self.r.dirSound).rglob("*.mp3"))
        #sampleMin = 48000
        for file in tqdm(files):
            with open(file, "r") as f:
                img = self.createSpectrograme(file)
                out = str(file).replace('mp3','png')
                skimage.io.imsave(out, img)
        #print(str(sampleMin)) Is resampling is needed ? check y_8k = librosa.resample(y, orig_sr=sr, target_sr=8000)

def main():
    api = XenoCantoRestApi.XenoCantoRestApi()
    r = DataSetPrepare(api)
    #r.createAllSpectrogramesInDirDataSet()
    r.generateDataSet()
    return 0

if __name__ == '__main__':
    sys.exit(main())