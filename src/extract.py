from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import requests
import socket
import ssl  
import OpenSSL
import time
import datetime
import whois 
import os
import sys

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
    """
    [Active] Sets the port feature based on port status.

    1) -1 if any port except 80(http) and 443(https) are open.
    2) 1 if no port except 80(http) and 443(https) are open.
    """
   
    for port in ports:

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)  
        IP = socket.gethostbyname(elements.netloc)
        result = sock.connect_ex((IP,ports[port]))

        if (ports[port] != 80 and ports[port] != 443) and (result == 0):
            features['port'] = -1
            break

        else:
            features['port'] = 1

def extractUrlLength():
    """
    [Passive] Sets the URL_Length feature with the threshold value of 54.

    1) -1 if the length is greater than or equal to 54.
    2) 1 if the length is less than 54.
    """

    if (len(URL) >= 54 ):
        features['URL_Length'] = -1
    else:
        features['URL_Length'] = 1

def extractAtSymbol():
    """
    [Passive] Sets the having_At_Symbol feature based on the presence of @ in the URL

    1) -1 if the URL contains @
    2) 1 if the URL does not contain @
    """

    if "@" in URL:
        features["having_At_Symbol"] = -1
    else:
        features["having_At_Symbol"] = 1

def extractDoubleSlashRedirecting():
    """
    [Passive] Sets the double_slash_redirecting feature based on the position of the last //.

    1) -1 if the last occuring // is after the 6th index.
    2) 1 if the last occuring // is before the 6th index.
    """
    
    if URL.rfind("//") > 6:
        features["double_slash_redirecting"] = -1
    else:
        features["double_slash_redirecting"] = 1

def extractPrefixSuffix():
    """
    [Passive] Sets the Prefix_Suffix feature after checking if the domain(netloc) comtains a -.

    1) -1 if the domain(netloc) contains a -.
    2) 1 if the domain(netloc) does not contain a -.
    """

    if '-' in elements.netloc:
        features["Prefix_Suffix"] = -1
    else:
        features["Prefix_Suffix"] = 1

def extractRedirects():
    """
    [Active] Sets the Redirect feature after checking if the URL redirects to a different URL.

    1) -1 if more than one redirects take place.
    2) 1 if less than or equal to 1 redirects take place.
    """
    try:
        responses = requests.get(URL, allow_redirects=True)
        if len(responses.history) > 1:
            features["Redirect"] = -1
        else:
            features["Redirect"] = 1
    except requests.exceptions.SSLError:
        print("Critical Error: Could not find ssl certificate")

def extractHttpsToken():
    """
    [Passive] Sets the HTTPS_token feature after checking if the domain starts with https or http.

    1) -1 if the domain begins with https or http.
    2) 1 if the domain does not begin with https or http.
    """
    if "https" in elements.netloc or elements.netloc.startswith("http"):
        features["HTTPS_token"] = -1
    else:
        features["HTTPS_token"] = 1

def extractShortiningService():
    """
    [Passive] Sets the Shortining_Service feature after checking if the domain starts with one of the popular link shortening websites.

    1) -1 if the domain begins with a link shortening domain.
    2) 1 if the domain does not begin with a link shortening domain.
    """

    if elements.netloc.startswith(("bit.ly", "t.co", "tinyurl")):
        features["Shortining_Service"] = -1
    else:
        features["Shortining_Service"] = 1

def extractHavingSubDomain():
    """
    [Passive] Sets the having_Sub_Domain feature after checking how many sub-domains the hostname has.
    This number include the "www." prefix and the top level domain like ".com" or ".uk"

    1) -1 if the hostname has more than 3 parts after splitting along '.' ie "www." + some name + ".com". 
    2) 1 if the hostname has 3 or fewer parts after splitting along '.'
    """

    list = elements.hostname.split(".")
    if len(list) > 3:
        features["having_Sub_Domain"] = -1
    else:
        features["having_Sub_Domain"] = 1

def extractHavingIpAdress():
    """
    [Passive] Sets the having_IP_Address feature after checking if the domain resembles an IP adress.

    1) -1 if the domain resembles an IP Address in integer or hexadecimal form.
    2) 1 if the domain does not resemble an IP Address in integer or hexadecimal form.
    """

    parts = elements.netloc.split('.')

    # Number of times a number appears in the domain
    countNum = 0
    # Numver of times a hexadecimal appears in the domain
    countHex = 0
    # Number of times a 'Normal' string appears in the domain
    countNormal = 0

    for part in parts:
        if part.isdigit():
            countNum = countNum + 1
        else:
            try:
                int(part, 16)
                countHex = countHex + 1
            except ValueError:
                countNormal = countNormal + 1
    
    if countNum + countHex > 0:
        features["having_IP_Address"] = -1
    else:
        features["having_IP_Address"] = 1

def extractSSLFinalState():
    """
    [Active] Sets the SSLfinal_State feature after checking the SSL certificate.

    1) -1 if the SSL certificate is less than 12 months old or expires in less than 12 months.
    2) 1 if the SSL certificate is more than 12 months old and expires in more than 12 months.
    """

    # trustedIssuers = ["GeoTrust", "GoDaddy", "Network Solutions", "Thawte", "Comodo", "Doster", "VeriSign"]
    if elements.scheme == "https":
        certString = ssl.get_server_certificate((socket.gethostbyname(elements.netloc),443))
        certificate = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, certString.encode('utf-8'))
        # Issuer = certificate.get_issuer()

        pattern = '%Y%m%d%H%M%Sz' # Pattern Matching for certificate dates
        currentTime = datetime.datetime.now() # Getting current calendar date

        # Checking if the Certificate is more than a year old
        startDate = str(certificate.get_notBefore(),'utf-8') # Getting the notBefore date on the Certificate
        startDateEpoch = int(time.mktime(time.strptime(startDate, pattern))) # Converting to Epoch Seconds
        startDateCal = datetime.datetime.fromtimestamp(startDateEpoch) # Converting to calendar date

        AgeInMonths = (currentTime.year - startDateCal.year) * 12 + (currentTime.month - startDateCal.month) # Finding age of license in months
        
        # Checking if the Certificate is valid for over a year
        endDate = str(certificate.get_notAfter(),'utf-8') # Getting the notAfter date on the Certificate
        endDateEpoch = int(time.mktime(time.strptime(endDate, pattern))) # Converting to Epoch Seconds
        endDateCal = datetime.datetime.fromtimestamp(endDateEpoch) # Converting to calendar date

        ExpiryInMonths = (endDateCal.year - currentTime.year) * 12 + (endDateCal.year - currentTime.year) # Finding expiry time in months

        if AgeInMonths > 12 and ExpiryInMonths > 12:
            features["SSLfinal_State"] = 1    
        else:
            features["SSLfinal_State"] = -1    
    else:
        features["SSLfinal_State"] = -1

def extractWhoisData():
    """
    [Active] Sets the age_of_domain and Domain_registeration_length feature after checking the whois database for the given domain.

    age_of_domain
    1) -1 if the domain was registered less than 6 months ago.
    2) 1 if the domain has been registered for more than 6 months.

    Domain_registeration_length
    1) -1 if the domain registration expires withing 12 months from the current date.
    2) 1 if the domain registration expires after 12 months from the current date.
    """
    try:

        data = whois.whois(URL)
        currentTime = datetime.datetime.now()

        if data == None:
            features["age_of_domain"] = -1
            features["Domain_registration_length"] = -1
        else:
            # Getting registration and expiry dates from whois records.

            # Flagging as suspicious if the creation or expiration dates are null

            if data["expiration_date"] is None:
                features["Domain_registration_length"] = -1
            if data["creation_date"] is None:
                features["age_of_domain"] = -1
            
            #Extracting expiration date

            if type(data["expiration_date"]) == list:
                expiryDate = data["expiration_date"][0]
            else:
                expiryDate = data["expiration_date"]

            # Extracting creation date
            if type(data["creation_date"]) == list:
                creationDate = data["creation_date"][0]
            else:
                creationDate = data["creation_date"]

            # Checking to make sure the age_of_domain feature is not flagged as suspicious beacuse it contains a null date of creation
            if features["age_of_domain"] != -1:
                # Checking if the domain registration date is more than 6 months ago
                monthsFromCreation = (currentTime.year - creationDate.year) * 12 + (currentTime.month - creationDate.month)

                if monthsFromCreation < 6:
                    features["age_of_domain"] = -1
                else:
                    features["age_of_domain"] = 1

            # Checking to make sure the Domain_registration_length is not flagged as suspicious beacuse it contains a null date of expiry
            if features["Domain_registration_length"] != -1:
                # Checking if the domain is registered for atleast 12 months into the future
                monthsTillExpiration = (expiryDate.year - currentTime.year) * 12 + (expiryDate.month - currentTime.month)

                if monthsTillExpiration <= 12:
                    features["Domain_registration_length"] = -1
                else:
                    features["Domain_registration_length"] = 1

    except whois.parser.PywhoisError:
        print("Critical error: Can't complete WHOIS lookup")

def extractHtmlAndJsFeatures():
    """
    [Active] Sets the Favicon and Submitting_to_email features after scrapping and assessing the script for the given website.

    Favicon
    1) -1 if the Favicon does not follow the industry standard for including favicon icon or hosting the icon file at a different domain.
    2) 1 if the Favicon follows the industry standard for including favicon icon and the icon file is hosted on the same domain.

    Submitting_to_email
    1) -1 if the pageSource contains mail() or mailto:
    2) 1 if the pageSource does not contain mail() and mailto:

    """
    PATH = "../src/WebDrivers/chromedriver"
    print(PATH)

    option = Options()
    option.headless = True

    # Making the selenium actions headless
    driver = webdriver.Chrome(PATH, options=option)
    driver.get(URL)

    # Getting page source
    pageSource = driver.page_source

    # 1. CHECKING THE FAVICON FEATURE

    if ("<link rel=\"shortcut icon\"" not in pageSource) and ("<link rel=\"icon\"" not in pageSource):
        features["Favicon"] = -1
    elif ("<link rel=\"shortcut icon\"" in pageSource):
        start = pageSource.find("<link rel=\"shortcut icon\"") # Getting the index where the shortcut icon link was found.
        endTag = pageSource.find(">", start) # Getting the index where the link tag closes
        hrefIndex = pageSource.find("href",start)  # Getting the index where the first href after the "short icon" appears

        # Flagged as suspicious of the tag is closed without an href.
        if endTag < hrefIndex:
            features["Favicon"] = -1
        else:
            urlStart = pageSource.find("\"", hrefIndex) # Getting the start index of the link
            urlEnd = pageSource.find("\"", urlStart + 1) # Getting the end index of the link
            imageHref = pageSource[urlStart + 1 : urlEnd] # Getting the href url

            # Checking if the domain of the favicon url and orignal url are the same.
            if urlparse(imageHref).netloc != elements.netloc:
                features["Favicon"] = -1
            else:
                features["Favicon"] = 1
    elif ("<link rel=\"icon\"" in pageSource):
        start = pageSource.find("<link rel=\"icon\"") # Getting the index where the icon link was found.
        endTag = pageSource.find(">", start) # Getting the index where the link tag closes
        hrefIndex = pageSource.find("href",start)  # Getting the index where the first href after the "short icon" appears

        # Flagged as suspicious of the tag is closed without an href.
        if endTag < hrefIndex:
            features["Favicon"] = -1
        else:
            urlStart = pageSource.find("\"", hrefIndex) # Getting the start index of the link
            urlEnd = pageSource.find("\"", urlStart + 1) # Getting the end index of the link
            imageHref = pageSource[urlStart + 1 : urlEnd] # Getting the href url

            # Checking if the domain of the favicon url and orignal url are the same.
            if urlparse(imageHref).netloc != elements.netloc:
                features["Favicon"] = -1
            else:
                features["Favicon"] = 1
    else:
        features["Favicon"] = -1

    # 2. CHECKING THE EMAIL SUBMISSION FEATURE

    if "mail()" in pageSource or "mailto:" in pageSource:
        features["Submitting_to_email"] = -1
    else:
        features["Submitting_to_email"] = 1

    driver.quit()

def extractAllFeatures(url):
    """
    Takes a URL and extracts all the features required for classification.

    Args:
        url (String): A string storing the URL.

    Returns:
        [dictionary]: A dictionary containing all the features for the given URL.
    """
    global features
    features = {
        "having_IP_Address": 0,
        "port": 0,
        "URL_Length": 0,
        "having_At_Symbol": 0,
        "double_slash_redirecting": 0,
        "Prefix_Suffix": 0,
        "Redirect": 0,
        "HTTPS_token": 0,
        "Shortining_Service": 0,
        "having_Sub_Domain": 0,
        "having_IP_Address": 0,
        "SSLfinal_State": 0,
        "age_of_domain": 0,
        "Domain_registration_length": 0,
        "Favicon": 0,
        "Submitting_to_email": 0}

    global URL 
    URL = url

    global elements
    elements = urlparse(URL)

    print(elements.netloc)
    extractPort()
    extractAtSymbol()
    extractUrlLength()
    extractDoubleSlashRedirecting()
    extractPrefixSuffix()
    extractRedirects()
    extractHttpsToken()
    extractShortiningService()
    extractHavingSubDomain()
    extractHavingIpAdress()
    extractHavingIpAdress()
    extractSSLFinalState()
    extractWhoisData()
    extractHtmlAndJsFeatures()
    print(features)
    return features
