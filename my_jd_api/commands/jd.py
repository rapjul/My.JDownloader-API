from my_jd_api.commands.device import Jddevice


class Jd:
    """
    Class that represents the jd-functionality of a Device
    """

    def __init__(self, device: Jddevice):
        self.device = device
        self.url = "/jd"

    def get_core_revision(self):
        """

        :return:
        """
        resp = self.device.action(self.url + "/getCoreRevision")
        return resp
