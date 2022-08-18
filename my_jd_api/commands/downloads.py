from my_jd_api.commands.device import Jddevice


class Downloads:
    """
    Class that represents the downloads list of a Device
    """

    def __init__(self, device: Jddevice):
        self.device = device
        self.url = "/downloadsV2"

    def query_links(
        self,
        params=[
            {
                "bytesTotal": True,
                "comment": True,
                "status": True,
                "enabled": True,
                "maxResults": -1,
                "startAt": 0,
                "packageUUIDs": [],
                "host": True,
                "url": True,
                "bytesloaded": True,
                "speed": True,
                "eta": True,
                "finished": True,
                "priority": True,
                "running": True,
                "skipped": True,
                "extractionStatus": True,
            }
        ],
    ):
        """
        Get the links in the download list
        """
        resp = self.device.action(self.url + "/queryLinks", params)
        return resp

    def query_packages(
        self,
        params=[
            {
                "bytesLoaded": True,
                "bytesTotal": True,
                "comment": True,
                "enabled": True,
                "eta": True,
                "priority": True,
                "finished": True,
                "running": True,
                "speed": True,
                "status": True,
                "childCount": True,
                "hosts": True,
                "saveTo": True,
                "maxResults": -1,
                "startAt": 0,
            }
        ],
    ):
        """
        Get the packages in the download list
        """
        resp = self.device.action(self.url + "/queryPackages", params)
        return resp

    def cleanup(self, action, mode, selection_type, link_ids=[], package_ids=[]):
        """
        Clean packages and/or links of the linkgrabber list.
        Requires at least a package_ids or link_ids list, or both.

        :param package_ids: Package UUID's.
        :type: list of strings.
        :param link_ids: link UUID's.
        :type: list of strings
        :param action: Action to be done. Actions: DELETE_ALL, DELETE_DISABLED, DELETE_FAILED, DELETE_FINISHED, DELETE_OFFLINE, DELETE_DUPE, DELETE_MODE
        :type: str:
        :param mode: Mode to use. Modes: REMOVE_LINKS_AND_DELETE_FILES, REMOVE_LINKS_AND_RECYCLE_FILES, REMOVE_LINKS_ONLY
        :type: str:
        :param selection_type: Type of selection to use. Types: SELECTED, UNSELECTED, ALL, NONE
        :type: str:
        """
        params = [link_ids, package_ids]
        params += [action, mode, selection_type]
        resp = self.device.action(self.url + "/cleanup", params)
        return resp

    def set_enabled(self, enable, link_ids, package_ids):
        """
        Enable or disable packages.

        :param enable: Enable or disable package.
        :type: boolean
        :param link_ids: Links UUID.
        :type: list of strings
        :param package_ids: Packages UUID.
        :type: list of strings.
        """
        params = [enable, link_ids, package_ids]
        resp = self.device.action(self.url + "/setEnabled", params)
        return resp

    def force_download(self, link_ids=[], package_ids=[]):
        params = [link_ids, package_ids]
        resp = self.device.action(self.url + "/forceDownload", params)
        return resp

    def set_dl_location(self, directory, package_ids=[]):
        params = [directory, package_ids]
        resp = self.device.action(self.url + "/setDownloadDirectory", params)
        return resp

    def remove_links(self, link_ids=[], package_ids=[]):
        """
        Remove packages and/or links of the downloads list.
        NOTE: For more specific removal, like deleting the files etc, use the /cleanup api.
        Requires at least a link_ids or package_ids list, or both.

        :param link_ids: link UUID's.
        :type: list of strings
        :param package_ids: Package UUID's.
        :type: list of strings.
        """
        params = [link_ids, package_ids]
        resp = self.device.action(self.url + "/removeLinks", params)
        return resp

    def reset_links(self, link_ids, package_ids):
        params = [link_ids, package_ids]
        resp = self.device.action(self.url + "/resetLinks", params)
        return resp

    def move_to_new_package(self, link_ids, package_ids, new_pkg_name, download_path):
        params = link_ids, package_ids, new_pkg_name, download_path
        resp = self.device.action(self.url + "/movetoNewPackage", params)
        return resp
