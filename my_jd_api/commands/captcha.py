from my_jd_api.commands.device import Jddevice


class Captcha:
    """
    Class that represents the captcha interface of a Device
    """

    def __init__(self, device: Jddevice):
        self.device = device
        self.url = "/captcha"

    """
    Get the waiting captchas
    """

    def list(self):
        resp = self.device.action(self.url + "/list", [])
        return resp

    """
    Get the base64 captcha image
    """

    def get(self, captcha_id):
        resp = self.device.action(self.url + "/get", (captcha_id,))
        return resp

    """
    Solve a captcha
    """

    def solve(self, captcha_id, solution):
        resp = self.device.action(self.url + "/solve", (captcha_id, solution))
        return resp
