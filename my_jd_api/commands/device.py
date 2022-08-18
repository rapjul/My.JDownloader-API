import time

from my_jd_api.commands import (
    Captcha,
    Config,
    DownloadController,
    Downloads,
    Jd,
    Linkgrabber,
    System,
    Toolbar,
    Update,
)
from my_jd_api.exception import (
    MYJDApiException,
    MYJDConnectionException,
    MYJDDecodeException,
    MYJDDeviceNotFoundException,
    MYJDException,
)


class Jddevice:
    """
    Class that represents a JDownloader device and it's functions
    """

    def __init__(self, jd: Jd, device_dict: dict):
        """This functions initializates the device instance.
        It uses the provided dictionary to create the device.

        :param device_dict: Device dictionary
        """
        self.name = device_dict["name"]
        self.device_id = device_dict["id"]
        self.device_type = device_dict["type"]
        self.myjd = jd
        self.config = Config(self)
        self.linkgrabber = Linkgrabber(self)
        self.captcha = Captcha(self)
        self.downloads = Downloads(self)
        self.toolbar = Toolbar(self)
        self.downloadcontroller = DownloadController(self)
        self.update = Update(self)
        self.jd = Jd(self)
        self.system = System(self)
        self.__direct_connection_info = None
        self.__refresh_direct_connections()
        self.__direct_connection_enabled = True
        self.__direct_connection_cooldown = 0
        self.__direct_connection_consecutive_failures = 0

    def __refresh_direct_connections(self):
        response = self.myjd.request_api(
            "/device/getDirectConnectionInfos", "POST", None, self.__action_url()
        )
        if (
            response is not None
            and "data" in response
            and "infos" in response["data"]
            and len(response["data"]["infos"]) != 0
        ):
            self.__update_direct_connections(response["data"]["infos"])

    def __update_direct_connections(self, direct_info):
        """
        Updates the direct_connections info keeping the order.
        """
        tmp = []
        if self.__direct_connection_info is None:
            for conn in direct_info:
                tmp.append({"conn": conn, "cooldown": 0})
            self.__direct_connection_info = tmp
            return
        #  We remove old connections not available anymore.
        for i in self.__direct_connection_info:
            if i["conn"] not in direct_info:
                tmp.remove(i)
            else:
                direct_info.remove(i["conn"])
        # We add new connections
        for conn in direct_info:
            tmp.append({"conn": conn, "cooldown": 0})
        self.__direct_connection_info = tmp

    def enable_direct_connection(self):
        self.__direct_connection_enabled = True
        self.__refresh_direct_connections()

    def disable_direct_connection(self):
        self.__direct_connection_enabled = False
        self.__direct_connection_info = None

    def action(self, path, params=(), http_action="POST"):
        """Execute any action in the device using the postparams and params.
        All the info of which params are required and what are they default value, type,etc
        can be found in the MY.Jdownloader API Specifications ( https://goo.gl/pkJ9d1 ).

        :param params: Params in the url, in a list of tuples. Example:
        /example?param1=ex&param2=ex2 [("param1","ex"),("param2","ex2")]
        :param postparams: List of Params that are send in the post.
        """
        action_url = self.__action_url()
        if (
            not self.__direct_connection_enabled
            or self.__direct_connection_info is None
            or time.time() < self.__direct_connection_cooldown
        ):
            # No direct connection available, we use My.JDownloader api.
            response = self.myjd.request_api(path, http_action, params, action_url)
            if response is None:
                # My.JDownloader Api failed too we assume a problem with the connection or the api server
                # and throw an connection exception.
                raise (MYJDConnectionException("No connection established\n"))
            else:
                # My.JDownloader Api worked, lets refresh the direct connections and return
                # the response.
                if (
                    self.__direct_connection_enabled
                    and time.time() >= self.__direct_connection_cooldown
                ):
                    self.__refresh_direct_connections()
                return response["data"]
        else:
            # Direct connection info available, we try to use it.
            for conn in self.__direct_connection_info:
                if time.time() > conn["cooldown"]:
                    # We can use the connection
                    connection = conn["conn"]
                    api = "http://" + connection["ip"] + ":" + str(connection["port"])
                    response = self.myjd.request_api(
                        path, http_action, params, action_url, api
                    )
                    if response is not None:
                        # This connection worked so we push it to the top of the list.
                        self.__direct_connection_info.remove(conn)
                        self.__direct_connection_info.insert(0, conn)
                        self.__direct_connection_consecutive_failures = 0
                        return response["data"]
                    else:
                        # We don't try to use this connection for a minute.
                        conn["cooldown"] = time.time() + 60
            # None of the direct connections worked, we set a cooldown for direct connections
            self.__direct_connection_consecutive_failures += 1
            self.__direct_connection_cooldown = time.time() + (
                60 * self.__direct_connection_consecutive_failures
            )
            # None of the direct connections worked, we use the My.JDownloader api
            response = self.myjd.request_api(path, http_action, params, action_url)
            if response is None:
                # My.JDownloader Api failed too we assume a problem with the connection or the api server
                # and throw an connection exception.
                raise (MYJDConnectionException("No connection established\n"))
            # My.JDownloader Api worked, lets refresh the direct connections and return
            # the response.
            self.__refresh_direct_connections()
            return response["data"]

    def __action_url(self):
        return "/t_" + self.myjd.get_session_token() + "_" + self.device_id
