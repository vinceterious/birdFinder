import sys
import skimage.io
import numpy as np
import librosa
from sklearn.preprocessing import minmax_scale
import XenoCantoRestApi

class DataSetPrepare:
    def __init__(self, retrieveXenoCantoAPISampleList):
        self.r = retrieveXenoCantoAPISampleList

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
        wImg = 1000
        w = img.shape[1]
        if w < wImg:
            return self.repeatImgUntilWSizeDesired(img, wImg)
        else:
            return self.cropImg(img,hImg,wImg)

    def openSpectrograme(self):
        from pathlib import Path
        files = list(Path(self.r.dirSound).rglob("*.png"))
        idx=0
        for file in files:
            with open(file, "r") as f:
                img = skimage.io.imread(file)
                sizeImg = self.shapeImg(img)
                #print(str(file) + " Shape: " + str(sizeImg.shape[:2]))

    def createSpectrograme(self):
        from pathlib import Path
        files = list(Path(self.r.dirSound).rglob("*.mp3"))
        sampleMin = 48000
        for file in files:
            with open(file, "r") as f:
                y, sr = librosa.load(file)
                mels = librosa.feature.melspectrogram(y=y, sr=sr)
                sampleMin = min(sr,sampleMin)
                mels = np.log(mels + 1e-9)
                img = minmax_scale(mels, feature_range=(0, 255)).astype(np.uint8)
                img = np.flip(img, axis=0) # put low frequencies at the bottom in image
                img = 255-img # invert. make black==more energy
                out = str(file).replace('mp3','png')
                skimage.io.imsave(out, img)
        #print(str(sampleMin)) Is resampling is needed ? check y_8k = librosa.resample(y, orig_sr=sr, target_sr=8000)
def main():
    api = XenoCantoRestApi.XenoCantoRestApi()
    r = DataSetPrepare(api)
    r.createSpectrograme()
    r.openSpectrograme()
    return 0

if __name__ == '__main__':
    sys.exit(main())