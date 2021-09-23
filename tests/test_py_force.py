import unittest
import os
from py_force.session import SFSession
from py_force.models import Account


class TestPyForce(unittest.TestCase):

    def setUp(self):
        self.test_domain = os.getenv("TEST_DOMAIN")
        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")
        self.username = os.getenv("USERNAME")
        self.password = os.getenv("PASSWORD")
        self.security_token = os.getenv("SECURITY_TOKEN")

    def tearDown(self):
        pass

    def test_auth(self):
        sf = SFSession(self.test_domain)
        status, token = sf.authenticate(self.client_id,
                                        self.client_secret,
                                        self.username,
                                        self.password,
                                        self.security_token)
        self.assertEqual(status, 200)

        status, data = sf.get_resources()
        self.assertEqual(status, 200)

        status, data = sf.get_objects()
        self.assertEqual(status, 200)

        a = Account(Name='Fostech',
                    NumberOfEmployees=1)
        status, data = sf.create_account(a.json(exclude_unset=True))
        self.assertEqual(status, 201)

        id = data['id']
        status, data = sf.query_account(id)
        self.assertEqual(status, 200)

        a = Account(NumberOfEmployees=3)
        status, data = sf.update_account(id, a.json(exclude_unset=True))
        self.assertEqual(status, 204)

        status, data = sf.query_account(id)
        self.assertEqual(status, 200)
        self.assertEqual(data['Name'], 'Fostech')
        self.assertEqual(data['NumberOfEmployees'], 3)

        status, data = sf.delete_account(id)
        self.assertEqual(status, 204)