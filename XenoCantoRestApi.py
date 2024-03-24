import requests
import sys
import json
import time
import os
from http.client import responses

class XenoCantoRestApi:
    directoryJson = "xenocantoApiResult"
    dirSound = "xenocantoSound"
    filename = "sample"

    def requestXenoCanto(self, url, verbose=False):
        r = requests.get(url)
        if verbose:
            print("Request: " + url + " Status:" + str(r.status_code))
        if r.status_code == 200:
            return r
        else:
            print("Issue with the request check url on return code.")
            print("url: " + url)
            print("status code: " + str(r.status_code) + " (" + responses[r.status_code] + ")")
            return None

    def requestOnePageFromXenoCanto(self, index, verbose=False):
        site = "https://xeno-canto.org/api/2/recordings?query=cnt:france"
        url = ""
        if index == 1:
            url = site
        else:
            url = site + "&page="+str(index)
        return self.requestXenoCanto(url, verbose)

    def writeOnePageFromXenoCanto(self, index, r):
        fileTowrite = self.directoryJson + "/" + self.filename + "_" + str(index) + ".json"
        with open(fileTowrite, "w") as f:
            f.write(r.text)

    def retrieveXenoCantoAPISampleList(self):
        rootR = self.requestOnePageFromXenoCanto(1)
        if rootR != None:
            if not os.path.exists(self.directoryJson):
                os.makedirs(self.directoryJson)
            self.writeOnePageFromXenoCanto(1, rootR)
            samples = json.loads(rootR.text)
            numOfRequest = samples["numPages"]
            for idx in range(2, numOfRequest + 1):
                time.sleep(1) #Xeno canto API take  max 1 request by sec
                r = self.requestOnePageFromXenoCanto(idx, True)
                if r != None:
                    self.writeOnePageFromXenoCanto(idx, r)
        return 0

    def downloadExtractSoundForCorvus(self):
        #temporary hard code
        espece = "Corvus"
        sousEspece = "corone"
        for idx in range(1,21):
            path = espece + "/" + sousEspece
            url = self.downloadFile[espece][sousEspece][idx]
            fName = str(idx) + ".mp3"
            self.r.downloadOneFile(url, path, fName)

    def downloadOneFile(self, url, path, filename ):
        time.sleep(1) #Xeno canto API take  max 1 request by sec
        absPath = self.dirSound + "/" + path
        if not os.path.exists( absPath ):
            os.makedirs(absPath )
        r = self.requestXenoCanto(url, True)
        if r != None:
            fileToWrite = absPath + "/" + filename
            with open(fileToWrite, "wb") as f:
                f.write(r.content)
                f.close()

def main():
    r = XenoCantoRestApi()
    return r.retrieveXenoCantoAPISampleList()

if __name__ == '__main__':
    sys.exit(main())