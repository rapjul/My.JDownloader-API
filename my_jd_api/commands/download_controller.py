from my_jd_api.commands.device import Jddevice


class DownloadController:
    """
    Class that represents the download-controller of a Device
    """

    def __init__(self, device: Jddevice):
        self.device = device
        self.url = "/downloadcontroller"

    def start_downloads(self):
        """

        :return:
        """
        resp = self.device.action(self.url + "/start")
        return resp

    def stop_downloads(self):
        """

        :return:
        """
        resp = self.device.action(self.url + "/stop")
        return resp

    def pause_downloads(self, value: bool):
        """

        :param value:
        :return:
        """
        value = bool(value)

        params = [value]
        resp = self.device.action(self.url + "/pause", params)
        return resp

    def get_speed_in_bytes(self):
        """

        :return:
        """
        resp = self.device.action(self.url + "/getSpeedInBps")
        return resp

        # btyes = int(resp)
        # return btyes

    def force_download(self, link_ids: list[int], package_ids: list[int]):
        """
        :param link_ids:
        :param package_ids:
        :return:
        """
        params = [link_ids, package_ids]
        resp = self.device.action(self.url + "/forceDownload", params)
        return resp

    def get_current_state(self):
        """

        :return:
        """
        resp = self.device.action(self.url + "/getCurrentState")
        return resp
