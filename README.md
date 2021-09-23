# PY_FORCE

A Python powered Salesforce library.

## Quickstart

### Create a Session

To begin, import the SFSession class, and initialize it with your Salesforce domain.

```
from py_force import SFSession
sf = SFSession('example.my.salesforce.com')
```

### Authentication

Most of the Salesforce functionality is behind an authentication wall. API authentication must be allowed for your domain and user. Follow the [Salesforce documentation](https://help.salesforce.com/s/articleView?id=sf.remoteaccess_oauth_username_password_flow.htm&type=5) for instructions on how to allow authentication.

Once authentication with the Salesforce domain as been allowed, call authenticate with the credentials given from your Salesforce domain.

```
status, token = sf.authenticate(client_id, client_secret, username, password, security_token)
```

### Working with Accounts

Accounts are a Salesforce object. Read more about them [here](https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_account.htm).

Accounts can be manipulated using the `create_account`, `update_account`, `query_account`, and `delete_account` methods.

```
a = Account(Name='Fostech',
            NumberOfEmployees=1)
status, data = sf.create_account(a.json(exclude_unset=True))

id = data['id']
status, data = sf.query_account(id)

a = Account(NumberOfEmployees=3)
status, data = sf.update_account(id, a.json(exclude_unset=True))

status, data = sf.query_account(id)

status, data = sf.delete_account(id)
```

### Running Tests

Tests can be run by storing authentication in environment variables and running `tests/test_py_force.py`.

```
TEST_DOMAIN='domian' CLIENT_ID='id' CLIENT_SECRET='secret' USERNAME='username' PASSWORD='password' SECURITY_TOKEN='security_token' python -m unittest tests/test_py_force.py
```
