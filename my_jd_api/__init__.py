from contextlib import contextmanager

import questionary

from my_jd_api.commands import (
    Captcha,
    Config,
    DownloadController,
    Downloads,
    Jd,
    Jddevice,
    Linkgrabber,
    Myjdapi,
    System,
    Toolbar,
    Update,
)
from my_jd_api.exception import (
    MYJDApiCommandNotFoundException,
    MYJDApiException,
    MYJDApiInterfaceNotFoundException,
    MYJDAuthFailedException,
    MYJDBadParametersException,
    MYJDBadRequestException,
    MYJDChallengeFailedException,
    MYJDConnectionException,
    MYJDDecodeException,
    MYJDDeviceNotFoundException,
    MYJDEmailForbiddenException,
    MYJDEmailInvalidException,
    MYJDErrorEmailNotConfirmedException,
    MYJDException,
    MYJDFailedException,
    MYJDFileNotFoundException,
    MYJDInternalServerErrorException,
    MYJDMaintenanceException,
    MYJDMethodForbiddenException,
    MYJDOfflineException,
    MYJDOutdatedException,
    MYJDOverloadException,
    MYJDSessionException,
    MYJDStorageAlreadyExistsException,
    MYJDStorageInvalidKeyException,
    MYJDStorageInvalidStorageIdException,
    MYJDStorageKeyNotFoundException,
    MYJDStorageLimitReachedException,
    MYJDStorageNotFoundException,
    MYJDTokenInvalidException,
    MYJDTooManyRequestsException,
    MYJDUnknownException,
)


@contextmanager
def start_session(
    username: str,
    password: str,
    app_key: str,
    *args,
    **kwargs,
):
    jd_session = Myjdapi()
    jd_session.set_app_key(app_key)

    """
    After that you can connect.
    Now you can only connect using username and password.
    This is a problem because you can't remember the session between executions
    for this reason i will add a way to "connect" which is actually not connecting,
    but adding the old tokens you saved. This way you can use this between executions
    as long as your tokens are still valid without saving the username and password.
    """
    try:
        jd_session.connect(username, password)

        if jd_session.is_connected():
            print(f"\n\nConnected to My.JDownloader account")
        else:
            raise MYJDConnectionException

        yield jd_session
    except Exception as e:
        # exit("No valid email address")
        raise e
    finally:
        jd_session.disconnect()


@contextmanager
def connect_device(jd_session: Myjdapi, device_name: str = ""):
    # When connecting it also gets the devices, so you can use them but if you want to
    # gather the devices available in My.JDownloader later you can do it like this

    jd_session.update_devices()
    # devices = jd_session.list_devices()
    # print(devices)

    try:
        if device_name is not None:
            device = jd_session.get_device(device_name=device_name)
        else:
            devices_dict = jd_session.list_devices()
            # print(devices_dict)

            selected_device = None
            if isinstance(devices_dict, list) and len(devices_dict) > 1:
                device_names = [device["name"] for device in devices_dict]

                selected_device = questionary.select(
                    "Choose a device to use for `My.JDownloader`", choices=device_names
                ).ask()

            if selected_device is None:
                selected_device = devices_dict[0]["name"]

            device = jd_session.get_device(device_name=selected_device)
            print(f"Connected to '{device.name}' on My.JDownloader")

        # print(device.name)
        # exit()

        yield device
    except Exception as e:
        raise e
    finally:
        pass
