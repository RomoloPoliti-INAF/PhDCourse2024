from functools import wraps
from time import sleep

from rich import print
from rich.status import Status

from commons import MSG, STATE
from console import console
from exceptions import *

##########################################
# Commands
##############################


def message(text: str):
    def decorate(f):
        @wraps(f)
        def inner(*args, **kwargs):
            console.print(f"{MSG.INFO}TM(1,7)")
            with Status(text, spinner='aesthetic', console=console):
                ret = f(*args, **kwargs)
                console.log(f"{MSG.INFO} {ret['msg']}")
                if args[0].verbose:
                    console.print(f"{MSG.INFO} {f.__name__} executed")
            return ret
        return inner
    return decorate


class MECommands:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose

    @message(text='Booting...')
    def NSS00001(self, *args, **kwargs):
        """Boot Command"""
        console.print(f'{MSG.INFO}[magenta]TM(5,1)[/magenta] - Boot Report')
        sleep(1)
        return {'msg': 'Booted'}

    @message(text='Shuting down...')
    def NSS00002(self, *args, **kwargs):
        """Shuting Down Command"""
        sleep(1)
        return {'msg': 'Shutting Down'}

    @message(text='Compressor switching ON...')
    def NSS00006(self, *args, **kwargs):
        """Compressor Switching ON Command"""
        sleep(1)
        ME = kwargs['caller']
        ME.CMP.state = STATE.IDLE
        return {'msg': 'Compressor Switching ON'}


class PECommands:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose

    @message(text="PE...ON ")
    def NSS00003(self, *args, **kwargs):
        """PE ON Command"""
        sleep(1)
        return {'msg': "PE Turning On"}

    @message(text="Image acquisition...")
    def NSS00004(self, *args, **kwargs):
        "Image acquisition"
        PE = kwargs['caller']
        if PE.FP.state == STATE.IDLE:
            PE.FP.state = STATE.BUSY
            img = PE.FP.acquire(params=kwargs['params'])
            PE.FP.state = STATE.IDLE
            return {'img': img,
                    'compression': kwargs['params']['PSS00002'],
                    'msg': 'Image acquired'
                    }
        else:
            raise State_Error("NSS00004", "FP", PE.FP.state)

    @message(text="FP...ON ")
    def NSS00005(self, *args, **kwargs):
        """FP ON Command"""
        sleep(1)
        PE = kwargs['caller']
        PE.FP.state = STATE.IDLE
        return {'msg': "FP Turning On"}
