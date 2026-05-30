from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from ..base import Base


class NetworkNode(Base):
    __tablename__ = "network_nodes"

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False, comment="Имя узла")
    node_type = Column(
        String(50),
        nullable=False,
        comment="Тип: switch, router, server, patch_panel, access_point, other",
    )
    ip_address = Column(String(45), comment="IP-адрес")
    mac_address = Column(String(32), comment="MAC-адрес")
    vendor = Column(String(100), comment="Производитель")
    model = Column(String(150), comment="Модель")
    serial_number = Column(String(100), comment="Серийный номер")

    status = Column(
        String(50),
        default="active",
        comment="Статус: active, inactive, faulty",
    )
    notes = Column(Text)

    location_id = Column(Integer, ForeignKey("locations.id"))

    location = relationship("Location", back_populates="network_nodes")
    outgoing_links = relationship(
        "NetworkLink",
        back_populates="from_node",
        foreign_keys="NetworkLink.from_node_id",
    )
    incoming_links = relationship(
        "NetworkLink",
        back_populates="to_node",
        foreign_keys="NetworkLink.to_node_id",
    )


class NetworkLink(Base):
    __tablename__ = "network_links"

    id = Column(Integer, primary_key=True)
    port_from = Column(String(50), comment="Порт на исходном узле")
    port_to = Column(String(50), comment="Порт на целевом узле")
    link_type = Column(
        String(50),
        default="ethernet",
        comment="Тип: ethernet, fiber, wireless, other",
    )
    status = Column(
        String(50),
        default="active",
        comment="Статус: active, inactive, faulty",
    )
    notes = Column(Text)

    from_node_id = Column(
        Integer, ForeignKey("network_nodes.id"), nullable=False
    )
    to_node_id = Column(
        Integer, ForeignKey("network_nodes.id"), nullable=False
    )

    from_node = relationship(
        "NetworkNode",
        back_populates="outgoing_links",
        foreign_keys=[from_node_id],
    )
    to_node = relationship(
        "NetworkNode",
        back_populates="incoming_links",
        foreign_keys=[to_node_id],
    )
