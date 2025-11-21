import json
import requests

from base64 import b64encode


class BasicAUTHRequest:
    def __init__(self, login, password):
        self.login = login
        self.password = password

    @staticmethod
    def get_session():
        return requests.Session()

    def add_default_headers(self, headers=None):
        headers = headers or {}
        return {
            "Authorization": self.get_auth_token(self.login, self.password),
            "Content-Type": "application/json",
            "Accept": "*/*",
            **headers
        }

    @staticmethod
    def get_auth_token(username, password):
        token = b64encode(f"{username}:{password}".encode('utf-8')).decode("ascii")
        return f'Basic {token}'

    def get(self, url, headers=None):
        with self.get_session() as session:
            return session.get(url, headers=self.add_default_headers(headers))

    def post(self, url, data=None, headers=None):
        with self.get_session() as session:
            return session.post(url, data=json.dumps(data), headers=self.add_default_headers(headers))

    def put(self, url, data=None, headers=None):
        with self.get_session() as session:
            return session.put(url, data=json.dumps(data), headers=self.add_default_headers(headers))

    def delete(self, url, headers=None):
        with self.get_session() as session:
            return session.delete(url, headers=self.add_default_headers(headers))

    def patch(self, url, data=None, headers=None):
        with self.get_session() as session:
            return session.patch(url, data=json.dumps(data), headers=self.add_default_headers(headers))
