import os
from dataclasses import dataclass, astuple


@dataclass
class Cfg:
    site: str = os.environ.get('gsite')
    login: str = os.environ.get('glogin')
    psw: str = os.environ.get('gpsw')
    root_path: str = 'E:/Parse'


if None in astuple(Cfg()):
    raise 'domain, login, psw not found'



