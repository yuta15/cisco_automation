from restconf_client import RestconfClient
from setting import Setting
    
def main():
    env_vars = Setting()
    
    client = RestconfClient(
        host='192.168.1.100',
        username=env_vars.username,
        password=env_vars.password,
        port=env_vars.port
    )
    if_params = [
        {'if_type': 'Gigabitethernet', 'if_num': 2, 'if_addr_and_mask': '10.1.100.1/24','vlan_id': 100},
        {'if_type': 'Gigabitethernet', 'if_num': 2, 'if_addr_and_mask': '10.1.101.1/24','vlan_id': 101},
        {'if_type': 'Gigabitethernet', 'if_num': 2, 'if_addr_and_mask': '10.1.102.1/24','vlan_id': 102},
        {'if_type': 'Gigabitethernet', 'if_num': 2, 'if_addr_and_mask': '10.1.103.1/24','vlan_id': 103},
        {'if_type': 'Gigabitethernet', 'if_num': 2, 'if_addr_and_mask': '10.1.104.1/24','vlan_id': 104},
        
        {'if_type': 'Gigabitethernet', 'if_num': 3, 'if_addr_and_mask': '10.1.200.1/24','vlan_id': 200},
        {'if_type': 'Gigabitethernet', 'if_num': 3, 'if_addr_and_mask': '10.1.201.1/24','vlan_id': 201},
        {'if_type': 'Gigabitethernet', 'if_num': 3, 'if_addr_and_mask': '10.1.202.1/24','vlan_id': 202},
        {'if_type': 'Gigabitethernet', 'if_num': 3, 'if_addr_and_mask': '10.1.203.1/24','vlan_id': 203},
        {'if_type': 'Gigabitethernet', 'if_num': 3, 'if_addr_and_mask': '10.1.204.1/24','vlan_id': 204},
        
    ]
    client.fetch_all_interface_data()
    for if_param in if_params:
        client.create_interface(**if_param)
    client.fetch_all_interface_data()
    

if __name__ == "__main__":
    main()