from urllib.parse import urlparse

URL = "http://www.youtube.com/watch?v=0Lt9w-BxKFQ"
elements = urlparse(URL)


features = {
    "having_IP_Address": 0,
    "port": 0,
    "URL_Length": 0,
    "having_At_Symbol": 0,
    "double_slash_redirecting": 0,
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
    ## Wait till we implement pure URL features

def extractUrlLength():
    """
    Sets the URL_Length feature with the threshold value of 54.

    1) -1 if the length is greater than or equal to 54.
    2) 1 if the length is less than 54.
    """

    if (len(URL) >= 54 ):
        features['URL_Length'] = -1
    else:
        features['URL_Length'] = 1

def extractAtSymbol():
    """
    Sets the having_At_Symbol feature based on the presence of @ in the URL

    1) -1 if the URL contains @
    2) 1 if the URL does not contain @
    """

    if "@" in URL:
        features["having_At_Symbol"] = -1
    else:
        features["having_At_Symbol"] = 1

def extractDoubleSlashRedirecting():
    """
    Sets the double_slash_redirecting feature based on the position of the last //.

    1) -1 if the last occuring // is after the 6th index.
    2) 1 if the last occuring // is before the 6th index.
    """
    
    if URL.rfind("//") > 6:
        features["double_slash_redirecting"] = -1
    else:
        features["double_slash_redirecting"] = 1


extractPort()
extractAtSymbol()
extractUrlLength()
extractDoubleSlashRedirecting()
print(features)
