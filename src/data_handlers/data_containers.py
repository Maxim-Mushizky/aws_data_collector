from dataclasses import dataclass, field
from datetime import datetime
from typing import (
    List,
    Optional,
    Dict
)


@dataclass(frozen=True)
class Ids:
    image_id: Optional[str] = field(default_factory=str)
    instance_id: Optional[str] = field(default_factory=str)
    reservation_id: Optional[str] = field(default_factory=str)


@dataclass(frozen=True)
class NetworkSettings:
    ip6_address: List = field(default_factory=list)
    private_dns_name: str = field(default_factory=str)
    private_ip_address: str = field(default_factory=str)
    subnet_id: Optional[str] = field(default_factory=str)
    interface_type: Optional[str] = field(default_factory=str)
    status: Optional[str] = field(default_factory=str)


@dataclass(frozen=True)
class Tags:
    tags: Dict = field(default_factory=dict)


@dataclass(frozen=True)
class PlatformDetails:
    os: str = field(default_factory=str)


@dataclass(frozen=True)
class Specs:
    cpu: Dict = field(default_factory=dict)
    memory: int = field(default_factory=int)
    instance_type: str = field(default_factory=str)


@dataclass(frozen=True)
class Times:
    launch_time: Optional[datetime] = field(default=None)
    usage_operation_update_time: Optional[datetime] = field(default=None)


@dataclass(frozen=True)
class SecurityGroups:
    groups: List[Dict] = field(default_factory=list)


@dataclass(frozen=True)
class Placement:
    availability_zone: str = field(default_factory=str)


@dataclass(frozen=True)
class Token:
    access_key_id: str = field(default="default")
    secret_access_key: str = field(default="default")


@dataclass(frozen=True)
class EC2Data:
    token: Token = field(default_factory=Token)
    ids: Optional[Ids] = field(default=None)
    network_settings: Optional[NetworkSettings] = field(default=None)
    platform_details: Optional[PlatformDetails] = field(default=None)
    tags: Optional[Tags] = field(default=None)
    times: Optional[Times] = field(default=None)
    security_groups: Optional[SecurityGroups] = field(default=None)
    specs: Optional[Specs] = field(default=None)
    placement: Optional[Placement] = field(default=None)
