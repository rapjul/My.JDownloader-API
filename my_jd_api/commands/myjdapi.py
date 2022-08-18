import base64
import hashlib
import hmac
import json
import time
from urllib.parse import quote

import requests
from Crypto.Cipher import AES

from my_jd_api.commands.device import Jddevice
from my_jd_api.exception import (
    MYJDApiException,
    MYJDConnectionException,
    MYJDDecodeException,
    MYJDDeviceNotFoundException,
    MYJDException,
)

BS = 16


def PAD(s):
    try:
        return s + ((BS - len(s) % BS) * chr(BS - len(s) % BS)).encode()
    except:  # For python 2
        return s + (BS - len(s) % BS) * chr(BS - len(s) % BS)


def UNPAD(s):
    try:
        return s[0 : -s[-1]]
    except:  # For python 2
        return s[0 : -ord(s[-1])]


class Myjdapi:
    """
    Main class for connecting to JD API.

    """

    def __init__(self) -> None:
        """
        This functions initializates the myjdapi object.

        """
        self.__request_id = int(time.time() * 1000)
        self.__api_url = "https://api.jdownloader.org"
        self.__app_key = "http://git.io/vmcsk"
        self.__api_version = 1
        self.__devices = None
        self.__login_secret = None
        self.__device_secret = None
        self.__session_token = None
        self.__regain_token = None
        self.__server_encryption_token = None
        self.__device_encryption_token = None
        self.__connected = False

    def get_session_token(self):
        return self.__session_token

    def is_connected(self) -> bool:
        """
        Indicates if there is a connection established.
        """
        return self.__connected

    def set_app_key(self, app_key):
        """
        Sets the APP Key.
        """
        self.__app_key = app_key

    def __secret_create(self, email: str, password: str, domain: str):
        """
        Calculates the login_secret and device_secret

        :param email: My.Jdownloader User email
        :param password: My.Jdownloader User password
        :param domain: The domain, if is for Server (login_secret) or Device (device_secret)
        :return: secret hash

        """
        secret_hash = hashlib.sha256()
        secret_hash.update(
            email.lower().encode("utf-8")
            + password.encode("utf-8")
            + domain.lower().encode("utf-8")
        )
        return secret_hash.digest()

    def __update_encryption_tokens(self) -> None:
        """
        Updates the server_encryption_token and device_encryption_token

        """
        if self.__server_encryption_token is None:
            old_token = self.__login_secret
        else:
            old_token = self.__server_encryption_token
        new_token = hashlib.sha256()
        new_token.update(old_token + bytearray.fromhex(self.__session_token))
        self.__server_encryption_token = new_token.digest()
        new_token = hashlib.sha256()
        new_token.update(self.__device_secret + bytearray.fromhex(self.__session_token))
        self.__device_encryption_token = new_token.digest()

    def __signature_create(self, key, data):
        """
        Calculates the signature for the data given a key.

        :param key:
        :param data:
        """
        signature = hmac.new(key, data.encode("utf-8"), hashlib.sha256)
        return signature.hexdigest()

    def __decrypt(self, secret_token, data):
        """
        Decrypts the data from the server using the provided token

        :param secret_token:
        :param data:
        """
        init_vector = secret_token[: len(secret_token) // 2]
        key = secret_token[len(secret_token) // 2 :]
        decryptor = AES.new(key, AES.MODE_CBC, init_vector)
        decrypted_data = UNPAD(decryptor.decrypt(base64.b64decode(data)))
        return decrypted_data

    def __encrypt(self, secret_token, data):
        """
        Encrypts the data from the server using the provided token

        :param secret_token:
        :param data:
        """
        data = PAD(data.encode("utf-8"))
        init_vector = secret_token[: len(secret_token) // 2]
        key = secret_token[len(secret_token) // 2 :]
        encryptor = AES.new(key, AES.MODE_CBC, init_vector)
        encrypted_data = base64.b64encode(encryptor.encrypt(data))
        return encrypted_data.decode("utf-8")

    def update_request_id(self):
        """
        Updates Request_Id
        """
        self.__request_id = int(time.time())

    def connect(self, email: str, password: str) -> bool:
        """Establish connection to api

        :param email: My.Jdownloader User email
        :param password: My.Jdownloader User password
        :returns: boolean -- True if succesful, False if there was any error.

        """
        self.update_request_id()
        self.__login_secret = None
        self.__device_secret = None
        self.__session_token = None
        self.__regain_token = None
        self.__server_encryption_token = None
        self.__device_encryption_token = None
        self.__devices = None
        self.__connected = False

        self.__login_secret = self.__secret_create(email, password, "server")
        self.__device_secret = self.__secret_create(email, password, "device")
        response = self.request_api(
            "/my/connect", "GET", [("email", email), ("appkey", self.__app_key)]
        )
        self.__connected = True
        self.update_request_id()
        self.__session_token = response["sessiontoken"]
        self.__regain_token = response["regaintoken"]
        self.__update_encryption_tokens()
        self.update_devices()
        return response

    def reconnect(self) -> bool:
        """
        Reestablish connection to API.

        :returns: boolean -- True if successful, False if there was any error.

        """
        response = self.request_api(
            "/my/reconnect",
            "GET",
            [
                ("sessiontoken", self.__session_token),
                ("regaintoken", self.__regain_token),
            ],
        )
        self.update_request_id()
        self.__session_token = response["sessiontoken"]
        self.__regain_token = response["regaintoken"]
        self.__update_encryption_tokens()
        return response

    def disconnect(self) -> bool:
        """
        Disconnects from  API

        :returns: boolean -- True if successful, False if there was any error.

        """
        response = self.request_api(
            "/my/disconnect", "GET", [("sessiontoken", self.__session_token)]
        )
        self.update_request_id()
        self.__login_secret = None
        self.__device_secret = None
        self.__session_token = None
        self.__regain_token = None
        self.__server_encryption_token = None
        self.__device_encryption_token = None
        self.__devices = None
        self.__connected = False
        return response

    def update_devices(self) -> bool:
        """
        Updates available devices. Use list_devices() to get the devices list.

        :returns: boolean -- True if successful, False if there was any error.
        """
        response = self.request_api(
            "/my/listdevices", "GET", [("sessiontoken", self.__session_token)]
        )
        self.update_request_id()
        self.__devices = response["list"]

    def list_devices(self) -> list[dict]:
        """
        Returns available devices. Use getDevices() to update the devices list.
        Each device in the list is a dictionary like this example:

        {
            'name': 'Device',
            'id': 'af9d03a21ddb917492dc1af8a6427f11',
            'type': 'jd'
        }

        :returns: list -- list of devices.
        """
        return self.__devices

    def get_device(self, device_name=None, device_id=None) -> Jddevice:
        """
        Returns a jddevice instance of the device

        :param deviceid:
        """
        if not self.is_connected():
            raise MYJDConnectionException("No connection established\n")
        if device_id is not None:
            for device in self.__devices:
                if device["id"] == device_id:
                    return Jddevice(self, device)
        elif device_name is not None:
            for device in self.__devices:
                if device["name"] == device_name:
                    return Jddevice(self, device)
        raise MYJDDeviceNotFoundException("Device not found\n")

    def request_api(
        self,
        path: str,
        http_method: str = "GET",
        params: dict = None,
        action=None,
        api=None,
    ) -> dict | None:
        """
        Makes a request to the API to the 'path' using the 'http_method' with parameters,'params'.
        Ex:
        http_method=GET
        params={"test":"test"}
        post_params={"test2":"test2"}
        action=True
        This would make a request to "https://api.jdownloader.org"
        """
        if not api:
            api = self.__api_url
        data = None

        if not self.is_connected() and path != "/my/connect":
            raise MYJDConnectionException("No connection established\n")

        if http_method == "GET":
            query = [path + "?"]

            if params is not None:
                for param in params:
                    if param[0] != "encryptedLoginSecret":
                        query += ["%s=%s" % (param[0], quote(param[1]))]
                    else:
                        query += ["&%s=%s" % (param[0], param[1])]
            query += ["rid=" + str(self.__request_id)]

            if self.__server_encryption_token is None:
                query += [
                    "signature="
                    + str(
                        self.__signature_create(
                            self.__login_secret, query[0] + "&".join(query[1:])
                        )
                    )
                ]
            else:
                query += [
                    "signature="
                    + str(
                        self.__signature_create(
                            self.__server_encryption_token,
                            query[0] + "&".join(query[1:]),
                        )
                    )
                ]

            query = query[0] + "&".join(query[1:])
            encrypted_response = requests.get(api + query, timeout=3)
        else:
            params_request = []

            if params is not None:
                for param in params:
                    if not isinstance(param, list):
                        params_request += [json.dumps(param)]
                    else:
                        params_request += [param]

            params_request = {
                "apiVer": self.__api_version,
                "url": path,
                "params": params_request,
                "rid": self.__request_id,
            }
            data = json.dumps(params_request)
            # Removing quotes around null elements.
            data = data.replace('"null"', "null")
            data = data.replace("'null'", "null")
            encrypted_data = self.__encrypt(self.__device_encryption_token, data)

            if action is not None:
                request_url = api + action + path
            else:
                request_url = api + path

            try:
                encrypted_response = requests.post(
                    request_url,
                    headers={"Content-Type": "application/aesjson-jd; charset=utf-8"},
                    data=encrypted_data,
                    timeout=3,
                )
            except requests.exceptions.RequestException as e:
                return None

        if encrypted_response.status_code != 200:
            try:
                error_msg = json.loads(encrypted_response.text)
            except json.JSONDecodeError:
                try:
                    error_msg = json.loads(
                        self.__decrypt(
                            self.__device_encryption_token, encrypted_response.text
                        )
                    )
                except json.JSONDecodeError:
                    raise MYJDDecodeException(
                        "Failed to decode response: {}", encrypted_response.text
                    )

            msg = (
                "\n\tSOURCE: "
                + error_msg["src"]
                + "\n\tTYPE: "
                + error_msg["type"]
                + "\n------\nREQUEST_URL: "
                + api
                + path
            )

            if http_method == "GET":
                msg += query
            msg += "\n"
            if data is not None:
                msg += "DATA:\n" + data

            raise MYJDApiException.get_exception(
                error_msg["src"], error_msg["type"], msg
            )

        if action is None:
            if not self.__server_encryption_token:
                response = self.__decrypt(self.__login_secret, encrypted_response.text)
            else:
                response = self.__decrypt(
                    self.__server_encryption_token, encrypted_response.text
                )
        else:
            response = self.__decrypt(
                self.__device_encryption_token, encrypted_response.text
            )

        json_data = json.loads(response.decode("utf-8"))

        if json_data["rid"] != self.__request_id:
            self.update_request_id()
            return None
        self.update_request_id()

        return json_data
