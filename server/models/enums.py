from enum import Enum

class Role(str, Enum):
    customer = "customer"
    agent = "agent"
    supervisor = "supervisor"
    admin = "admin"
