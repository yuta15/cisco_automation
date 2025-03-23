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
        

    # def interface_no_shutdown(self, if_type, if_num):
    #     """
    #     Args:
    #         if_type: str, 
    #             Interfaceの種類や名前
    #             ex) GigabitEthernet
    #                 Fastethernet等
    #         if_num: int | str, 
    #             interface番号
    #             ex) 1を指定した場合、Gigabitethernet1,
    #                 1/24を指定した場合、Gigabitethernet1/24のような形になる。
    #     """
    #     url = f'{self.base_url}/Cisco-IOS-XE-native:native/interface/{if_type}={if_num}
    #     body= {

    #         "name": "2",
    #         "shutdown": False,
    #     },

        
    def create_interface(
        self, 
        if_type: str, 
        if_num: int | str, 
        if_addr_and_mask: str, 
        vlan_id: int = None
        ):
        """
        Args:
            if_type: str, 
                Interfaceの種類や名前
                ex) GigabitEthernet
                    Fastethernet等
            if_num: int | str, 
                interface番号
                ex) 1を指定した場合、Gigabitethernet1,
                    1/24を指定した場合、Gigabitethernet1/24のような形になる。
                    subintafaceを指定する場合は、
                    1.101のように指定
            if_addr_and_mask: str
                interfaceアドレスおよびマスク情報
                ex)192.168.1.1/24, 10.10.1.1/16等
            vlan_id: int = None
                vlan IDを指定
                ex)100を指定するとGigabitEthernet1.100のようになります。
        """
        put_if_data = InterfaceModel(
            if_type=if_type,
            if_num=if_num,
            if_addr_and_mask=if_addr_and_mask,
            vlan_id=vlan_id
        ).generate_if_dict()

        if isinstance(if_num, str) and "/" in if_num:
            if_num="%".join(if_num.split("/"))
        url = f'{self.base_url}/Cisco-IOS-XE-native:native/interface/{if_type}="{if_num}"'
        try:
            response = requests.put(
                url=url,
                auth=(self.username, self.password),
                headers=self.header,
                json=put_if_data,
                verify=False
            )
        except:
            raise 
        else:
            return response


    def fetch_all_interface_data(self):
        """
        全インターフェース情報を取得するための関数
        """
        url = f'{self.base_url}/Cisco-IOS-XE-native:native/interface'
        try:
            response = requests.get(
                url=url,
                auth=(self.username, self.password),
                headers=self.header,
                verify=False
                )
        except:
            raise
        else:
            return response
    

    def delete_interface(self, if_type, if_num):
        """
        指定したインターフェースを初期化する。
        """
        if "/" in if_num:
            if_num="%".join(if_num.split("/"))
        url = f'{self.base_url}/Cisco-IOS-XE-native:native/interface/{if_type}="{if_num}"'
        try:
            response = requests.delete(
                url=url,
                auth=(self.username, self.password),
                headers=self.header,
                verify=False
                )
        except:
            raise
        else:
            return response