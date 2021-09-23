import requests


class SFSession(object):
    """A class for connecting to, and interacting with a Salesforce Rest API

    :param domain: The domain to connect to (e.g. mydomain.my.salesforce.com)
    """
    def __init__(self, domain):
        """Constructor method
        """
        self.auth_url = "https://{}/services/oauth2/token".format(domain)
        self.token = None

        api_url = "https://{}/services/data".format(domain)
        r = requests.get(api_url)
        versions = r.json()
        self.version = versions[-1]['version']
        self.api_url = api_url + "/v{}".format(self.version)

    def _auth_required(func):
        """A decorator function to require authorization. If
        self.authorization() has not be called, function will alert and
        return

        :param func: The function to wrap
        """
        def check_login(self, *args, **kwargs):
            if self.token is None:
                return "Authenitcation required"
            else:
                return func(self, *args, **kwargs)
        return check_login

    def authenticate(self,
                     client_id,
                     client_secret,
                     username,
                     password,
                     security_token):
        """Authenticates the Salesforce API session. All requests will be made
        using the authenticated account.

        :param client_id: The client ID with which to connect
        :param client_secret: The client secret value
        :param username: The username to log in as
        :param password: The password for the provided username
        :param security_token: The security token associated with the account
        :return: An HTTP status code and response data
        """
        payload = {
                    'grant_type': 'password',
                    'client_id': client_id,
                    'client_secret': client_secret,
                    'username': username,
                    'password': password + security_token
                  }
        r = requests.post(self.auth_url, params=payload)
        return_data = r.json()
        self.token = return_data['access_token']
        return r.status_code, self.token

    @_auth_required
    def get_resources(self):
        """Gets the resources available to the session
        :return: An HTTP status code and response data
        """
        headers = { 'Authorization': 'Bearer {}'.format(self.token) }
        uri = self.api_url
        r = requests.get(uri, headers=headers)
        return r.status_code, r.json()

    @_auth_required
    def get_objects(self, modified_since=None, unmodified_since=None):
        """Gets the objects available to the session

        :param modified_since: A value in the form 
        'EEE, dd, MMM yyyy HH:mm:ss z', that returns records that have been
        modified after the provided date and time
        :param unmodified_since: A value in the form 
        'EEE, dd, MMM yyyy HH:mm:ss z', that returns records that have not
        been modified after the provided date and time

        :return: An HTTP status code and response data
        """
        headers = { 'Authorization': 'Bearer {}'.format(self.token) }
        payload = {}
        if modified_since is not None:
            payload['If-Modified-Since'] = modified_since
        if unmodified_since is not None:
            payload['If-Unmodified-Since'] = unmodified_since
        uri = self.api_url + "/sobjects/"
        r = requests.get(uri, params=payload, headers=headers)
        return r.status_code, r.json()

    @_auth_required
    def describe_object(self, name, modified_since=None, unmodified_since=None):
        """Gets metadata on the requested object

        :param name: The name of the object to describe
        :param modified_since: A value in the form 
        'EEE, dd, MMM yyyy HH:mm:ss z', that returns records that have been
        modified after the provided date and time
        :param unmodified_since: A value in the form 
        'EEE, dd, MMM yyyy HH:mm:ss z', that returns records that have not
        been modified after the provided date and time

        :return: An HTTP status code and response data
        """
        headers = { 'Authorization': 'Bearer {}'.format(self.token), }
        payload = {}
        if modified_since is not None:
            payload['If-Modified-Since'] = modified_since
        if unmodified_since is not None:
            payload['If-Unmodified-Since'] = unmodified_since
        uri = self.api_url + "/sobjects/{}/describe".format(name)
        r = requests.get(uri, params=payload, headers=headers)
        return r.status_code, r.json()

    @_auth_required
    def create_account(self, data):
        """Creates an account object

        :param data: A JSON object holding account metadata
        :return: An HTTP status code and response data describing the account
        """
        headers = { 'Authorization': 'Bearer {}'.format(self.token), 
                    'Content-Type': 'application/json'}
        uri = self.api_url + "/sobjects/Account/"
        r = requests.post(uri, headers=headers, data=data)
        return r.status_code, r.json()

    @_auth_required
    def query_account(self, id):
        """Retrieves an account object

        :param id: The ID of the object to query
        :return: An HTTP status code and response data describing the account
        """
        headers = { 'Authorization': 'Bearer {}'.format(self.token) }
        uri = self.api_url + "/sobjects/Account/{}".format(id)
        r = requests.get(uri, headers=headers)
        return r.status_code, r.json()

    @_auth_required
    def update_account(self, id, data):
        """Updates an account object

        :param id: The ID of the object to query
        :param data: A JSON object holding account metadata
        :return: An HTTP status code and None
        """
        headers = { 'Authorization': 'Bearer {}'.format(self.token), 
                    'Content-Type': 'application/json'}
        uri = self.api_url + "/sobjects/Account/{}".format(id)
        print(uri)
        r = requests.patch(uri, headers=headers, data=data)
        return r.status_code, None

    @_auth_required
    def delete_account(self, id):
        """Deletes an account object

        :param id: The ID of the object to query
        :return: An HTTP status code and None
        """
        headers = { 'Authorization': 'Bearer {}'.format(self.token) }
        uri = self.api_url + "/sobjects/Account/{}".format(id)
        r = requests.delete(uri, headers=headers)
        return r.status_code, None