from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Literal, Optional
from ipaddress import IPv4Address, ip_interface, AddressValueError

from hsrp_model import HsrpModel

class InterfaceModel(BaseModel):
    if_type: Literal['GigabitEthernet', 'FastEthernet', 'Loopback']
    if_name: str
    pri_addr_and_mask: Optional[IPv4Address] = Field(default=None)
    if_url: Optional[str] = Field(default=None)
    vlan_id: Optional[int]| None = Field(default=None)
    if_description: Optional[str] = Field(default=None, max_length=30)


    # HSRP設定。今後拡張予定
    # sec_addr_and_mask: Optional[IPv4Address] = Field(default=None)
    # hsrp: Optional[HsrpModel] = Field(default=None)
    # standby_group_id: Optional[int] = Field(default=None)
    # standby_ip: Optional[IPv4Address] = Field(default=None)
    # standby_priority: Optional[int] = Field(default=None, ge=1, le=100)
    # standby_preempt_delay: Optional[int] = Field(default=None, ge=0, le=3600)
    # standby_preempt_minimum: Optional[int] = Field(default=None, ge=0, le=3600)
    # standby_preempt_reload: Optional[int] = Field(default=None, ge=0, le=3600)

    @model_validator(mode='before')
    @classmethod
    def _validate_url(cls, values):
        if_type = values.get('if_type')
        if_name = values.get('if_name')
        values['if_url'] = f'Cisco-IOS-XE-native:native/interface/{if_type}="{if_name}"'
        return values


    @field_validator('if_name' ,mode='before')
    @classmethod
    def _validate_if_num_to_string(cls, in_if_name: float | int) -> str:
        """validation用"""
        try:
            return str(in_if_name)
        except ValueError:
            raise ValueError()


    @field_validator('pri_addr_and_mask',mode='before')
    @classmethod
    def _validate_ipv4interface(cls, in_addr_and_mask: str) -> IPv4Address:
        """validation用"""
        try:
            return ip_interface(in_addr_and_mask)
        except AddressValueError:
            raise ValueError()


    def generate_config(self) -> dict:
        """interface設定用のConfigを生成する関数"""
        if_config = {
            self.if_type: {
                "name": self.if_name,
                "description": self.if_description,
                "ip": {
                    "address": {
                        "primary": {
                            "address": str(self.pri_addr_and_mask.ip),
                            "mask": str(self.pri_addr_and_mask.netmask)
                            }
                    }
                }
            }
        }
        if self.vlan_id:
            if_config[self.if_type]["encapsulation"] = {
                "dot1Q":{
                    "vlan-id": self.vlan_id
                }
            }
        return if_config
