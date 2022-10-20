from . import tables, enums 
from .config import config, yaml

def nop(*_):
    """NOP (unused request can use this)"""
    ...

nop(tables, enums, config, yaml)