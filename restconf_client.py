import requests
from interface_model import InterfaceModel


class RestconfClient():
    def __init__(self, host: str, username: str, password: str, port: int=443, **kwargs):
        self.host: str = host
        self.username: str = username
        self.password:str = password
        self.port:int = port
        self.base_url = f'https://{self.host}:{self.port}/restconf/data'
        self.header = {'Content-Type': 'application/yang-data+json', 'Accept': 'application/yang-data+json'}


    def put_config(self, url: str, config: dict, verify:bool=False) -> requests.Response:
        """
        設定をPUTする関数
        Args:
            url: str
                PUTするデータのURL.先頭の/はつけないこと。
                'https://{self.host}:{self.port}/restconf/data'に連結するURLを指定する。
                ex)
                    url=Cisco-IOS-XE-native:native/interface/GigabitEhternet=2
                    -> https://{self.host}:{self.port}/restconf/data/Cisco-IOS-XE-native:native/interface/GigabitEhternet=2
            config:dict
                PUTするデータ
            verify: bool = False

        return: 
            Response: requests.Response
        """
        try:
            response = requests.put(
                url=self.base_url+'/'+url,
                auth=(self.username, self.password),
                headers=self.header,
                json=config,
                verify=verify
            )
        except requests.HTTPError:
            raise requests.HTTPError()
        else:
            return response


    def get_config(self, url: str, verify:bool=False) -> requests.Response:
        """
        設定をgetする関数
        Args:
            url: str
                PUTするデータのURL.先頭の/はつけないこと。
                'https://{self.host}:{self.port}/restconf/data'に連結するURLを指定する。
                ex)
                    url=Cisco-IOS-XE-native:native/interface/GigabitEhternet=2
                    -> https://{self.host}:{self.port}/restconf/data/Cisco-IOS-XE-native:native/interface/GigabitEhternet=2
            verify: bool = False

        return: 
            Response: requests.Response
        """
        try:
            response = requests.get(
                url=self.base_url+'/'+url,
                auth=(self.username, self.password),
                headers=self.header,
                verify=verify
            )
        except requests.HTTPError:
            raise requests.HTTPError()
        else:
            return response


    def delete_config(self, url: str, verify:bool=False) -> requests.Response:
        """
        設定をdeleteする関数
        Args:
            url: str
                deleteするデータのURL.先頭の/はつけないこと。
                'https://{self.host}:{self.port}/restconf/data'に連結するURLを指定する。
                ex)
                    url=Cisco-IOS-XE-native:native/interface/GigabitEhternet=2
                    -> https://{self.host}:{self.port}/restconf/data/Cisco-IOS-XE-native:native/interface/GigabitEhternet=2
            verify: bool = False

        return: 
            Response: requests.Response
        """
        try:
            response = requests.delete(
                url=self.base_url+'/'+url,
                auth=(self.username, self.password),
                headers=self.header,
                verify=verify
            )
        except requests.HTTPError:
            raise requests.HTTPError()
        else:
            return response
 
 
    def patch_config(self, url: str, config:dict,  verify:bool=False) -> requests.Response:
        """
        設定をpatchする関数
        Args:
            url: str
                patchするデータのURL.先頭の/はつけないこと。
                'https://{self.host}:{self.port}/restconf/data'に連結するURLを指定する。
                ex)
                    url=Cisco-IOS-XE-native:native/interface/GigabitEhternet=2
                    -> https://{self.host}:{self.port}/restconf/data/Cisco-IOS-XE-native:native/interface/GigabitEhternet=2
            config:dict
                PUTするデータ
            verify: bool = False

        return: 
            Response: requests.Response
        """
        try:
            response = requests.patch(
                url=self.base_url+'/'+url,
                auth=(self.username, self.password),
                headers=self.header,
                json=config,
                verify=verify
            )
        except requests.HTTPError:
            raise requests.HTTPError()
        else:
            return response
        