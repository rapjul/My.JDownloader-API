from my_jd_api.commands.device import Jddevice


class Update:
    """
    Class that represents the update-functionality of a Device
    """

    def __init__(self, device: Jddevice):
        self.device = device
        self.url = "/update"

    def restart_and_update(self):
        """

        :return:
        """
        resp = self.device.action(self.url + "/restartAndUpdate")
        return resp

    def run_update_check(self):
        """

        :return:
        """
        resp = self.device.action(self.url + "/runUpdateCheck")
        return resp

    def is_update_available(self):
        """

        :return:
        """
        resp = self.device.action(self.url + "/isUpdateAvailable")
        return resp

    def update_available(self):
        self.run_update_check()
        resp = self.is_update_available()
        return resp
