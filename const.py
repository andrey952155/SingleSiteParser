import os
from dataclasses import dataclass, astuple


@dataclass
class Book:
    site: str = os.environ.get('gsite')
    login: str = os.environ.get('glogin')
    psw: str = os.environ.get('gpsw')


if None in astuple(Book()):
    raise 'domain, login, psw not found'



