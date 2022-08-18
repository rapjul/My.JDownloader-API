from my_jd_api.commands.device import Jddevice


class Linkgrabber:
    """
    Class that represents the linkgrabber of a Device
    """

    def __init__(self, device: Jddevice):
        self.device = device
        self.url = "/linkgrabberv2"

    def clear_list(self):
        """
        Clears Linkgrabbers list
        """
        resp = self.device.action(self.url + "/clearList", http_action="POST")
        return resp

    def move_to_downloadlist(self, link_ids, package_ids):
        """
        Moves packages and/or links to download list.

        :param package_ids: Package UUID's.
        :type: list of strings.
        :param link_ids: Link UUID's.
        """
        params = [link_ids, package_ids]
        resp = self.device.action(self.url + "/moveToDownloadlist", params)
        return resp

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
                "hosts": True,
                "url": True,
                "availability": True,
                "variantIcon": True,
                "variantName": True,
                "variantID": True,
                "variants": True,
                "priority": True,
            }
        ],
    ):
        """

        Get the links in the linkcollector/linkgrabber

        :param params: A dictionary with options. The default dictionary is
        configured so it returns you all the downloads with all details, but you
        can put your own with your options. All the options available are this
        ones:
        {
            "bytesTotal"    : false,
            "comment"       : false,
            "status"        : false,
            "enabled"       : false,
            "maxResults"    : -1,
            "startAt"       : 0,
            "packageUUIDs"  : null,
            "hosts"         : false,
            "url"           : false,
            "availability"  : false,
            "variantIcon"   : false,
            "variantName"   : false,
            "variantID"     : false,
            "variants"      : false,
            "priority"      : false
        }
        :type: Dictionary
        :rtype: List of dictionaries of this style, with more or less detail based on your options.

        [   {   'availability': 'ONLINE',
            'bytesTotal': 68548274,
            'enabled': True,
            'name': 'The Rick And Morty Theory - The Original        Morty_ - '
                    'Cartoon Conspiracy (Ep. 74) @ChannelFred (192kbit).m4a',
            'packageUUID': 1450430888524,
            'url': 'youtubev2://DEMUX_M4A_192_720P_V4/d1NZf1w2BxQ/',
            'uuid': 1450430889576,
            'variant': {   'id': 'DEMUX_M4A_192_720P_V4',
                        'name': '192kbit/s M4A-Audio'},
            'variants': True
            }, ... ]
        """
        resp = self.device.action(self.url + "/queryLinks", params)
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

    def add_container(self, type_, content):
        """
        Adds a container to Linkgrabber.

        :param type_: Type of container.
        :type: string.
        :param content: The container.
        :type: string.

        """
        params = [type_, content]
        resp = self.device.action(self.url + "/addContainer", params)
        return resp

    def get_download_urls(self, link_ids, package_ids, url_display_type):
        """
        Gets download urls from Linkgrabber.

        :param package_ids: Package UUID's.
        :type: List of strings.
        :param link_ids: link UUID's.
        :type: List of strings
        :param url_display_type: No clue. Not documented
        :type: Dictionary
        """
        params = [package_ids, link_ids, url_display_type]
        resp = self.device.action(self.url + "/getDownloadUrls", params)
        return resp

    def set_priority(self, priority, link_ids, package_ids):
        """
        Sets the priority of links or packages.

        :param package_ids: Package UUID's.
        :type: list of strings.
        :param link_ids: link UUID's.
        :type: list of strings
        :param priority: Priority to set. Priorities: HIGHEST, HIGHER, HIGH, DEFAULT, LOWER;
        :type: str:
        """
        params = [priority, link_ids, package_ids]
        resp = self.device.action(self.url + "/setPriority", params)
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

    def get_variants(self, params):
        """
        Gets the variants of a url/download (not package), for example a youtube
        link gives you a package with three downloads, the audio, the video and
        a picture, and each of those downloads have different variants (audio
        quality, video quality, and picture quality).

        :param params: List with the UUID of the download you want the variants. Ex: [232434]
        :type: List
        :rtype: Variants in a list with dictionaries like this one: [{'id':
        'M4A_256', 'name': '256kbit/s M4A-Audio'}, {'id': 'AAC_256', 'name':
        '256kbit/s AAC-Audio'},.......]
        """
        resp = self.device.action(self.url + "/getVariants", params)
        return resp

    def add_links(
        self,
        params=[
            {
                "autostart": False,
                "links": None,
                "packageName": None,
                "extractPassword": None,
                "priority": "DEFAULT",
                "downloadPassword": None,
                "destinationFolder": None,
                "overwritePackagizerRules": False,
            }
        ],
    ):
        """
        Add links to the linkcollector

        {
        "autostart" : false,
        "links" : null,
        "packageName" : null,
        "extractPassword" : null,
        "priority" : "DEFAULT",
        "downloadPassword" : null,
        "destinationFolder" : null
        }
        """
        resp = self.device.action("/linkgrabberv2/addLinks", params)
        return resp

    def is_collecting(self):
        """
        Boolean status query about the collecting process
        """
        resp = self.device.action(self.url + "/isCollecting")
        return resp

    def get_childrenchanged(self):
        """
        no idea what parameters i have to pass and/or i don't know what it does.
        if i find out i will implement it :p
        """
        pass

    def remove_links(self, link_ids=[], package_ids=[]):
        """
        Remove packages and/or links of the linkgrabber list.
        Requires at least a link_ids or package_ids list, or both.

        :param link_ids: link UUID's.
        :type: list of strings
        :param package_ids: Package UUID's.
        :type: list of strings.
        """
        params = [link_ids, package_ids]
        resp = self.device.action(self.url + "/removeLinks", params)
        return resp

    def get_downfolderhistoryselectbase(self):
        """
        No idea what parameters i have to pass and/or i don't know what it does.
        If i find out i will implement it :P
        """
        pass

    def help(self):
        """
        It returns the API help.
        """
        resp = self.device.action("/linkgrabberv2/help", http_action="GET")
        return resp

    def rename_link(self, link_id, new_name):
        """
        Renames files related with link_id
        """
        params = [link_id, new_name]
        resp = self.device.action(self.url + "/renameLink", params)
        return resp

    def move_links(self):
        """
        No idea what parameters i have to pass and/or i don't know what it does.
        If i find out i will implement it :P
        """
        pass

    def move_to_new_package(self, link_ids, package_ids, new_pkg_name, download_path):
        params = link_ids, package_ids, new_pkg_name, download_path
        resp = self.device.action(self.url + "/movetoNewPackage", params)
        return resp

    def set_variant(self):
        """
        No idea what parameters i have to pass and/or i don't know what it does.
        If i find out i will implement it :P
        """
        pass

    def get_package_count(self):
        resp = self.device.action("/linkgrabberv2/getPackageCount")
        return resp

    def rename_package(self, package_id, new_name):
        """
        Rename package name with package_id
        """
        params = [package_id, new_name]
        resp = self.device.action(self.url + "/renamePackage", params)
        return resp

    def query_packages(
        self,
        params=[
            {
                "availableOfflineCount": True,
                "availableOnlineCount": True,
                "availableTempUnknownCount": True,
                "availableUnknownCount": True,
                "bytesTotal": True,
                "childCount": True,
                "comment": True,
                "enabled": True,
                "hosts": True,
                "maxResults": -1,
                "packageUUIDs": [],
                "priority": True,
                "saveTo": True,
                "startAt": 0,
                "status": True,
            }
        ],
    ):
        resp = self.device.action(self.url + "/queryPackages", params)
        return resp

    def move_packages(self):
        """
        No idea what parameters i have to pass and/or i don't know what it does.
        If i find out i will implement it :P
        """
        pass

    def add_variant_copy(self):
        """
        No idea what parameters i have to pass and/or i don't know what it does.
        If i find out i will implement it :P
        """
        pass
