from enum import Enum

class Role(str, Enum):
    customer = "customer"
    agent = "agent"
    admin = "admin"
