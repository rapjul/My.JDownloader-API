from my_jd_api.commands.device import Jddevice


class System:
    """
    Class that represents the system-functionality of a Device
    """

    def __init__(self, device: Jddevice):
        self.device = device
        self.url = "/system"

    def exit_jd(self):
        """

        :return:
        """
        resp = self.device.action(self.url + "/exitJD")
        return resp

    def restart_jd(self):
        """

        :return:
        """
        resp = self.device.action(self.url + "/restartJD")
        return resp

    def hibernate_os(self):
        """

        :return:
        """
        resp = self.device.action(self.url + "/hibernateOS")
        return resp

    def shutdown_os(self, force):
        """

        :param force:  Force Shutdown of OS
        :return:
        """
        params = force
        resp = self.device.action(self.url + "/shutdownOS", params)
        return resp

    def standby_os(self):
        """

        :return:
        """
        resp = self.device.action(self.url + "/standbyOS")
        return resp

    def get_storage_info(self):
        """

        :return:
        """
        resp = self.device.action(self.url + "/getStorageInfos?path")
        return resp
