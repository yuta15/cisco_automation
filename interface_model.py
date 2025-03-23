from pydantic import BaseModel, Field, field_validator 
from typing import Literal, Optional
from ipaddress import IPv4Address, ip_interface, AddressValueError


class InterfaceModel(BaseModel):
    if_type: Literal['GigabitEthernet', 'FastEthernet']
    if_num: str
    if_addr_and_mask: IPv4Address
    vlan_id: Optional[int] = Field(default=None)


    @field_validator('if_num' ,mode='before')
    @classmethod
    def _validate_if_num_to_string(cls, in_if_num: float | int) -> str:
        try:
            return str(in_if_num)
        except ValueError:
            raise ValueError()


    @field_validator('if_addr_and_mask' ,mode='before')
    @classmethod
    def _validate_ipv4interface(cls, in_if_addr_and_mask: str) -> IPv4Address:
        try:
            return ip_interface(in_if_addr_and_mask)
        except AddressValueError:
            raise ValueError()


    def generate_if_dict(self) -> dict:
        if self.vlan_id is None:
            return {
                self.if_type: {
                    "name": self.if_num,
                    "ip": {
                        "address": {
                        "primary": {
                            "address": str(self.if_addr_and_mask.ip),
                            "mask": str(self.if_addr_and_mask.netmask)
                            }
                        }
                    }
                }
            }
        else:
            return {
                self.if_type: {
                    "name": self.if_num,
                    "encapsulation":{
                        "dot1Q":{
                            "vlan-id": self.vlan_id
                        }
                    },
                    "ip": {
                        "address": {
                        "primary": {
                            "address": str(self.if_addr_and_mask.ip),
                            "mask": str(self.if_addr_and_mask.netmask)
                            }
                        }
                    }
                }
            }

