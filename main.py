from interface_model import InterfaceModel
from restconf_client import RestconfClient
from setting import Setting
    
    
def main():
    # 環境変数設定
    env_vars = Setting()
    
    # インスタンス化
    client = RestconfClient(
        host='192.168.1.100',
        username=env_vars.username,
        password=env_vars.password,
        port=env_vars.port
    )

    # テスト用データ
    test_if_params = [
        {'if_type': 'GigabitEthernet', 'if_name': 2.100, 'pri_addr_and_mask': '10.1.101.1/24','vlan_id': 100, "if_description": "### vlan 100 ###"},
        {'if_type': 'GigabitEthernet', 'if_name': 2.101, 'pri_addr_and_mask': '10.1.101.1/24','vlan_id': 101},
        {'if_type': 'GigabitEthernet', 'if_name': 2.102, 'pri_addr_and_mask': '10.1.102.1/24','vlan_id': 102},
        {'if_type': 'GigabitEthernet', 'if_name': 2.103, 'pri_addr_and_mask': '10.1.103.1/24','vlan_id': 103},
        {'if_type': 'GigabitEthernet', 'if_name': 2.104, 'pri_addr_and_mask': '10.1.104.1/24','vlan_id': 104},
        {'if_type': 'GigabitEthernet', 'if_name': 3.200, 'pri_addr_and_mask': '10.1.200.1/24','vlan_id': 200, "if_description": "### vlan 200 ###"},
        {'if_type': 'GigabitEthernet', 'if_name': 3.201, 'pri_addr_and_mask': '10.1.201.1/24','vlan_id': 201},
        {'if_type': 'GigabitEthernet', 'if_name': 3.202, 'pri_addr_and_mask': '10.1.202.1/24','vlan_id': 202},
        {'if_type': 'GigabitEthernet', 'if_name': 3.203, 'pri_addr_and_mask': '10.1.203.1/24','vlan_id': 203},
        {'if_type': 'GigabitEthernet', 'if_name': 3.204, 'pri_addr_and_mask': '10.1.204.1/24','vlan_id': 204},
    ]

    # 実行
    with open('result.txt', mode='w') as f:
        print(client.fetch_all_interface_data().json(), file=f)
        print('############################################', file=f)
        for test_if_param in test_if_params:
            if_model = InterfaceModel(**test_if_param)
            if_config = if_model.generate_config()
            result = client.put_config(
                url=if_model.if_url, 
                config=if_config,
                verify=False
                )
            print(result.status_code, file=f)
        print('############################################', file=f)
        print(client.fetch_all_interface_data().json(), file=f)


if __name__ == "__main__":
    main()