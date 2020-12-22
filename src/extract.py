from urllib.parse import urlparse

URL = "http://www.youtube.com/watch?v=0Lt9w-BxKFQ"
elements = urlparse(URL)


features = {
    "having_IP_Address":0,
    "port":0,
    "URL_Length":0,
    "having_At_Symbol":0,
}

ports = {
    "http": 80,
    "https": 443,
    "ftp": 21,
    "ssh": 22,
    "telnet": 23,
    "smb": 445,
    "mssql": 1433,
    "oracle": 1521,
    "mysql": 3306,
    "remotedesktop": 3389
}

def extractPort():
    port = ports[elements.scheme]
    print(port)
    ## Wait till we implement pure URL feature

def extractUrlLength():
    if (len(URL) >= 54 ):
        features['URL_Length'] = -1
    else:
        features['URL_Length'] = 1

def extractAtSymbol():
    if "@" in URL:
        features["having_At_Symbol"] = -1
    else:
        features["having_At_Symbol"] = 1

extractPort()
extractAtSymbol()
extractUrlLength()
print(features)
