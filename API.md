## What is the Phishy API?
In order to make access to Phishy's technology easy and platform agnostic, we developed an API. This allows us to allows us to improve our model and ensure that everyone who uses Phishy can benefit from the enhancements without having to make any changes to their projects. We plan on using this API for our Chrome Extension and possibly even our mobile apps.

## How can I use it?
Phishy's functionality can be accessed through a REST API. Consult our documentation if you'd like to get started. If you run into an issues, you can report them on our GitHub. You can also use our Advance Results API to get insights into what tests a given website passed or failed. As we continue development, we intend on adding more comprehensive API's to Phishy.

## What do you mean by features?
In order to achieve our promising results we had to build custom feature extraction tools. These features were then used for binary classification using an SVM model trained on similar data from UC Irvine's ML Repository. In addition to phishing detection, this data can be used for other application. To serve this purpose, all the feature extraction results can be accessed through the Advance Results API. We have also detailed all the features we used for Phishy here.


## Usage:

### 1. Status
This API call provides the status of the server. The JSON contains the following.

1. Status: Returns 1 if the server is operating as expected

Example :

```
https://phishy.ai/status/
```

JSON :
```
{
  Status: 1,
}
```

### 2. Regular Result
This API call provides the basic results for a given URL. The JSON contains the following.

1. Confidence Score: Returns a metric that indicates how confident we are with our models prediction.
2. Result: Returns 1 if the website is safe, 0 if the test is inconclusive and -1 if it's a phish.
3. URL: Returns the URL on which the model was run.

Example :
```
https://phishy.ai/results/?url=Enter url here
```
JSON :
```
{
  URL: 'https://phishy.ai/',
  Result: 1,
  Confidence Score: 0.96
}
```
### 3. Advance Result
This API call provides advance results for a given URL. The JSON contains the following.

1. Confidence Score: Returns a metric that indicates how confident we are with our models prediction.
2. Result: Returns 1 if the website is safe, 0 if the test is inconclusive and -1 if it's a phish.
3. URL: Returns the URL on which the model was run.
4. Features: Returns a list of features that were extracted before running the model. For every feature, 1 means safe and -1 means unsafe. null indicates an inconclusive test.
Example :
```
https://phishy.ai/adv_results/?url=Enter url here
```
JSON :
```
{
  URL: 'https://www.youtube.com/',
  Result: 1,
  Confidence Score: 1,
  Features: {…}
}
```
Features :
```
{
  Favicon: 1,
  HTTPS_token: 1,
  Prefix_Suffix: 1,
  Redirect: 1,
  SSLfinal_State: 1,
  Shortining_Service: 1,
  Submitting_to_email: 1,
  URL_Length: 1,
  age_of_domain: 1,
  double_slash_redirecting: 1,
  having_At_Symbol: 1,
  having_IP_Address: 1,
  having_Sub_Domain: 1,
  port: 1,
}
```