from my_jd_api.commands.device import Jddevice


class Toolbar:
    """
    Class that represents the toolbar of a Device
    """

    def __init__(self, device: Jddevice):
        self.device = device
        self.url = "/toolbar"

    def get_status(self, params=None):
        resp = self.device.action(self.url + "/getStatus")
        return resp

    def status_downloadSpeedLimit(self):
        self.status = self.get_status()
        if self.status["limit"]:
            return 1
        else:
            return 0

    def enable_downloadSpeedLimit(self):
        self.limit_enabled = self.status_downloadSpeedLimit()
        if not self.limit_enabled:
            self.device.action(self.url + "/toggleDownloadSpeedLimit")

    def disable_downloadSpeedLimit(self):
        self.limit_enabled = self.status_downloadSpeedLimit()
        if self.limit_enabled:
            self.device.action(self.url + "/toggleDownloadSpeedLimit")
