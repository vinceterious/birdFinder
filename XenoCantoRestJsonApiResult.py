import sys
import json
import os
import XenoCantoRestApi

class XenoCantoRestJsonApiResult:
    def __init__(self, retrieveXenoCantoAPISampleList):
        self.r = retrieveXenoCantoAPISampleList

    def constructMetadataDico(self, mapOfDowloadUrls, entry):
        espece = entry["gen"]
        sousEspece = entry["sp"]
        if espece not in mapOfDowloadUrls.keys():
            mapOfDowloadUrls[espece] = { }
        if sousEspece not in mapOfDowloadUrls[espece].keys():
            mapOfDowloadUrls[espece][sousEspece] = []
        mapOfDowloadUrls[espece][sousEspece].append(entry["file"])

    def getMapOfUrlFromJsonApi(self):
        dir = self.r.directoryJson
        mapOfDowloadUrls = {}
        files = os.listdir( dir )
        for file in files:
            with open(dir + "/" + file, "r") as f:
                recordData = json.load(f)["recordings"]
                for entry in recordData:
                    self.constructMetadataDico(mapOfDowloadUrls, entry)
        #for espece, sousEspeces in mapOfDowloadUrls.items():
            #for sousEspece, files in sousEspeces.items():
                #print(espece + "," + sousEspece + "," + str(len(files)))
        return mapOfDowloadUrls

def main():
    api = XenoCantoRestApi.XenoCantoRestApi()
    r = XenoCantoRestJsonApiResult(api)
    map = r.getMapOfUrlFromJsonApi()
    api.downloadAllFilesFound(map)
    return 0

if __name__ == '__main__':
    sys.exit(main())