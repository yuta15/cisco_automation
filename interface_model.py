from pydantic import BaseModel, Field, field_validator 
from typing import Literal, Optional
from ipaddress import IPv4Address, ip_interface, AddressValueError


class InterfaceModel(BaseModel):
    if_type: Literal['Gigabitethernet', 'Fastethernet']
    if_num: str | int
    if_addr_and_mask: IPv4Address
    vlan_id: Optional[int] = Field(default=None)


    @field_validator('if_addr_and_mask' ,mode='before')
    @classmethod
    def _validate_ipv4interface(cls, in_if_addr_and_mask: str) -> IPv4Address:
        try:
            return ip_interface(in_if_addr_and_mask)
        except AddressValueError:
            raise ValueError()


    def generate_if_json(self) -> dict:
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
                        "address": self.if_addr_and_mask.ip,
                        "mask": self.if_addr_and_mask.netmask
                        }
                    }
                }
            }
        }
