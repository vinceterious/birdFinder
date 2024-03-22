import sys
import json
import os
import retrieveXenoCantoAPISampleList

class ReadXenoCantoData:
    r = retrieveXenoCantoAPISampleList.RetrieveXenoCantoAPISampleList()
    downloadFile = {}
    def readFileByFile(self):
        dir = self.r.directoryJson
        filename = self.r.filename
        files = os.listdir( dir )
        for file in files:
            with open(dir + "/" + file, "r") as f:
                recordData = json.load(f)["recordings"]
                for entry in recordData:
                    espece = entry["gen"]
                    sousEspece = entry["sp"]
                    if espece not in self.downloadFile.keys():
                        self.downloadFile[espece] = { }
                    if sousEspece not in self.downloadFile[espece].keys():
                        self.downloadFile[espece][sousEspece] = []
                    self.downloadFile[espece][sousEspece].append(entry["file"])
        for espece, sousEspeces in self.downloadFile.items():
            for sousEspece, files in sousEspeces.items():
                print(espece + "," + sousEspece + "," + str(len(files)))
    
    def downloadExtractSoundForCorvusAndColumbus(self):
        #temporary hard code
        espece = "Passer"
        sousEspece = "domesticus"
        for idx in range(1,21):
            path = espece + "/" + sousEspece
            url = self.downloadFile[espece][sousEspece][idx]
            fName = str(idx) + ".mp3"
            self.r.downloadOneFile(url, path, fName)

def main():
    r = ReadXenoCantoData()
    r.readFileByFile()
    r.downloadExtractSoundForCorvusAndColumbus()
    return 0

if __name__ == '__main__':
    sys.exit(main())