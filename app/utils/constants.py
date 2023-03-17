from enum import Enum

class CompanyRole(str, Enum):
    ADMIN = 'admin'
    MEMBER = 'member'
    OWNER = 'owner'