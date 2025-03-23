from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Literal, Optional
from ipaddress import IPv4Address, ip_interface, AddressValueError

from hsrp_model import HsrpModel

class InterfaceModel(BaseModel):
    if_type: Literal['GigabitEthernet', 'FastEthernet', 'Loopback']
    if_name: str
    pri_addr_and_mask: IPv4Address
    if_url: str = Field(default_factory=f'Cisco-IOS-XE-native:native/interface/{if_type}="{if_name}"')
    vlan_id: Optional[int]| None = Field(default=None)
    if_description: Optional[str] = Field(default=None, max_length=30)
    is_if_enable: bool = Field(default=True)
    
    # HSRP設定。今後拡張予定
    # sec_addr_and_mask: Optional[IPv4Address] = Field(default=None)
    # hsrp: Optional[HsrpModel] = Field(default=None)
    # standby_group_id: Optional[int] = Field(default=None)
    # standby_ip: Optional[IPv4Address] = Field(default=None)
    # standby_priority: Optional[int] = Field(default=None, ge=1, le=100)
    # standby_preempt_delay: Optional[int] = Field(default=None, ge=0, le=3600)
    # standby_preempt_minimum: Optional[int] = Field(default=None, ge=0, le=3600)
    # standby_preempt_reload: Optional[int] = Field(default=None, ge=0, le=3600)


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
                "name": self.if_num,
                "description": self.if_description,
                "shutdown": False if self.is_if_enable else None,
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
        if self.vlan_id:
            if_config[self.if_type]["encapsulation"] = {
                "dot1Q":{
                    "vlan-id": self.vlan_id
                }
            }
        return if_config
    
    
    def if_enable_config(self, enable_hardware_if: int) -> dict:
        """物理インターフェースのみをUPさせたい場合に使用"""
        enable_config = {
            self.if_type: {
                "name": enable_hardware_if,
                "shutdown": False
            }
        }