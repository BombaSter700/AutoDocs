from .base import _BaseSchema


class NetworkNodeCreate(_BaseSchema):
    name: str
    node_type: str
    ip_address: str | None = None
    mac_address: str | None = None
    vendor: str | None = None
    model: str | None = None
    serial_number: str | None = None
    status: str = "active"
    notes: str | None = None
    location_id: int | None = None


class NetworkNodeRead(NetworkNodeCreate):
    id: int


class NetworkLinkCreate(_BaseSchema):
    port_from: str | None = None
    port_to: str | None = None
    link_type: str = "ethernet"
    status: str = "active"
    notes: str | None = None
    from_node_id: int
    to_node_id: int


class NetworkLinkRead(NetworkLinkCreate):
    id: int
