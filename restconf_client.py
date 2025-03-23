import requests
from interface_model import InterfaceModel


class RestconfClient():
    def __init__(self, host: str, username: str, password: str, port: int=443, **kwargs):
        self.host: str = host
        self.username: str = username
        self.password:str = password
        self.port:int = port
        self.base_url = f'https://{self.host}:{self.port}/restconf/data/'
        self.header = {'Content-Type': 'application/yang-data+json', 'Accept': 'application/yang-data+json'}
        
        
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
                ex) Gigabitethernet
                    Fastethernet等
            if_num: int | str, 
                interface番号
                ex) 1を指定した場合、Gigabitethernet1,
                    1/24を指定した場合、Gigabitethernet1/24のような形になる。
            if_addr_and_mask: str
                interfaceアドレスおよびマスク情報
                ex)192.168.1.1/24, 10.10.1.1/16等
            vlan_id: int = None
                vlan IDを指定
                ex)100を指定するとGigabitethernet1.100のようになります。
        """
        put_if_data = InterfaceModel(
            if_type=if_type,
            if_num=if_num,
            if_addr_and_mask=if_addr_and_mask,
            vlan_id=vlan_id
        ).generate_if_json()
        url = f'{self.base_url}/Cisco-IOS-XE-native:native/interface/{if_type}={if_num}.{vlan_id if not vlan_id==None else ""}'
        response = requests.put(
            url=url,
            auth=(self.username, self.password),
            headers=self.header,
            json=put_if_data,
            verify=False
        )
        return response


    def fetch_all_interface_data(self):
        """
        全インターフェース情報を取得するための関数
        """
        url = f'{self.base_url}/Cisco-IOS-XE-native:native/interface/'
        response = requests.get(
            url=url,
            auth=(self.username, self.password),
            headers=self.header
            )
        return response
    