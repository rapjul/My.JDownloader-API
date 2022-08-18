from my_jd_api.commands.device import Jddevice


class Config:
    """
    Class that represents the Config of a Device
    """

    def __init__(self, device: Jddevice):
        self.device = device
        self.url = "/config"

    def list(self):
        """
        :return:  List<AdvancedConfigAPIEntry>
        """
        resp = self.device.action(self.url + "/list")
        return resp

    def get(self, interface_name, storage, key):
        """
        :param interfaceName: a valid interface name from List<AdvancedConfigAPIEntry>
        :type: str:
        :param storage: 'null' to use default or 'cfg/' + interfaceName
        :type: str:
        :param key: a valid key from from List<AdvancedConfigAPIEntry>
        :type: str:
        """
        params = [interface_name, storage, key]
        resp = self.device.action(self.url + "/get", params)
        return resp

    def set(self, interface_name, storage, key, value):
        """
        :param interfaceName:  a valid interface name from List<AdvancedConfigAPIEntry>
        :type: str:
        :param storage: 'null' to use default or 'cfg/' + interfaceName
        :type: str:
        :param key: a valid key from from List<AdvancedConfigAPIEntry>
        :type: str:
        :param value: a valid value for the given key (see type value from List<AdvancedConfigAPIEntry>)
        :type: Object:
        """
        params = [interface_name, storage, key, value]
        resp = self.device.action(self.url + "/set", params)
        return resp
