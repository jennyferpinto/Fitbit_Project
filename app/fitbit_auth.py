import os, httplib
from oauth import oauth

CONSUMER_KEY    = 'c91f84cd10f04cebad9beb7d4812eb90'
CONSUMER_SECRET = 'e2b38ed6dad443e8bad8efbe3e0e3da5'
SERVER = 'api.fitbit.com'
REQUEST_TOKEN_URL = 'http://%s/oauth/request_token' % SERVER
ACCESS_TOKEN_URL = 'http://%s/oauth/access_token' % SERVER
AUTHORIZATION_URL = 'http://%s/oauth/authorize' % SERVER
DEBUG = False

def fetch_response(oauth_request, connection, debug=DEBUG):
    url = oauth_request.to_url()
    connection.request(oauth_request.http_method,url)
    response = connection.getresponse()
    s=response.read()
    if debug:
        print 'requested URL: %s' % url
        print 'server response: %s' % s
    return s

def get_request_token():
    connection = httplib.HTTPSConnection(SERVER)
    consumer = oauth.OAuthConsumer(CONSUMER_KEY, CONSUMER_SECRET)
    signature_method = oauth.OAuthSignatureMethod_PLAINTEXT()
    oauth_request = oauth.OAuthRequest.from_consumer_and_token(consumer, http_url=REQUEST_TOKEN_URL)
    oauth_request.sign_request(signature_method, consumer, None)

    resp = fetch_response(oauth_request, connection)
    auth_token = oauth.OAuthToken.from_string(resp)

    #build the URL
    authkey = str(auth_token.key)
    authsecret = str(auth_token.secret)
    auth_url = "%s?oauth_token=%s" % (AUTHORIZATION_URL, auth_token.key)
    return auth_url, auth_token

def get_access_token(access_code, user_key, user_secret):
    oauth_verifier = access_code
    auth_token = oauth.OAuthToken(user_key, user_secret)
    connection = httplib.HTTPSConnection(SERVER)
    consumer = oauth.OAuthConsumer(CONSUMER_KEY, CONSUMER_SECRET)
    signature_method = oauth.OAuthSignatureMethod_PLAINTEXT()
    oauth_request = oauth.OAuthRequest.from_consumer_and_token(consumer, token=auth_token, http_url=ACCESS_TOKEN_URL, parameters={'oauth_verifier': oauth_verifier})
    oauth_request.sign_request(signature_method, consumer, auth_token)
    # now the token we get back is an access token
    # parse the response into an OAuthToken object
    access_token = oauth.OAuthToken.from_string(fetch_response(oauth_request,connection))
    return access_token
