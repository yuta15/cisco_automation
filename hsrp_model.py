from pydantic import BaseModel, Field, field_validator, conint
from typing import Optional
from ipaddress import IPv4Address


class HsrpModel(BaseModel):
    """
    standby_group_id: Optional[int] = None
        ex) standby_group_id=1
    standby_ip: Optional[IPv4Address] = None
        ex)standby_ip="192.168.1.254
    standby_priority: Optional[int] = None
        ex)standby_priority=105
        **range 1 - 255
    standby_preempt: Optional[dict] = None
        ex)standby_preempt={
            delay: {
                sync: 0~3600 
                minimum: 0~3600
                reload: 0~3600
            }
        }
    """
    standby_group_id: Optional[int] = Field(default=None)
    standby_ip: Optional[IPv4Address] = Field(default=None)
    standby_priority: Optional[int] = Field(default=None, ge=1, le=100)
    standby_preempt: Optional[dict] = Field(default=None)


    

    @property
    def hsrp_config(self) -> dict:
        """
        hsrp用のDictを返すプロパティ
        """

        hsrp_config = {
            "standby":{
                "version":2,
                "group":[
                    {
                        "number": self.standby_group_id,
                        "priority": self.standby_priority,
                        "ip": self.standby_ip
                    }
                ]
            }
        }
        return hsrp_config