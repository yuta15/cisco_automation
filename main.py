import os

import json
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

    # テスト用パラメータ
    tesf_if_params = [
        {'if_type': 'GigabitEthernet', 'if_num': 2.100, 'if_addr_and_mask': '10.1.101.1/24','vlan_id': 100},
        {'if_type': 'GigabitEthernet', 'if_num': 2.101, 'if_addr_and_mask': '10.1.101.1/24','vlan_id': 101},
        {'if_type': 'GigabitEthernet', 'if_num': 2.102, 'if_addr_and_mask': '10.1.102.1/24','vlan_id': 102},
        {'if_type': 'GigabitEthernet', 'if_num': 2.103, 'if_addr_and_mask': '10.1.103.1/24','vlan_id': 103},
        {'if_type': 'GigabitEthernet', 'if_num': 2.104, 'if_addr_and_mask': '10.1.104.1/24','vlan_id': 104},
        {'if_type': 'GigabitEthernet', 'if_num': 3.200, 'if_addr_and_mask': '10.1.200.1/24','vlan_id': 200},
        {'if_type': 'GigabitEthernet', 'if_num': 3.201, 'if_addr_and_mask': '10.1.201.1/24','vlan_id': 201},
        {'if_type': 'GigabitEthernet', 'if_num': 3.202, 'if_addr_and_mask': '10.1.202.1/24','vlan_id': 202},
        {'if_type': 'GigabitEthernet', 'if_num': 3.203, 'if_addr_and_mask': '10.1.203.1/24','vlan_id': 203},
        {'if_type': 'GigabitEthernet', 'if_num': 3.204, 'if_addr_and_mask': '10.1.204.1/24','vlan_id': 204},
    ]
    tesf_del_if_params = [
        {'if_type': 'GigabitEthernet', 'if_num': 2.100},
        {'if_type': 'GigabitEthernet', 'if_num': 2.101},
        {'if_type': 'GigabitEthernet', 'if_num': 2.102},
        {'if_type': 'GigabitEthernet', 'if_num': 2.103},
        {'if_type': 'GigabitEthernet', 'if_num': 2.104},
        {'if_type': 'GigabitEthernet', 'if_num': 3.200},
        {'if_type': 'GigabitEthernet', 'if_num': 3.201},
        {'if_type': 'GigabitEthernet', 'if_num': 3.202},
        {'if_type': 'GigabitEthernet', 'if_num': 3.203},
        {'if_type': 'GigabitEthernet', 'if_num': 3.204},
    ]
    # 削除
    # for test_del_pal in tesf_del_if_params:
    #     response = client.delete_interface(**test_del_pal)
    #     print(response)

    # 実行結果及び結果の書き出し
    with open('result.txt', mode='w') as f:
        print(client.fetch_all_interface_data().json(), file=f)
        for if_param in tesf_if_params:
            print(client.create_interface(**if_param).status_code, file=f)
        print(client.fetch_all_interface_data().json(), file=f)
    

if __name__ == "__main__":
    main()