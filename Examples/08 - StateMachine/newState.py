#!/usr/bin/env python3
import argparse
import functools
import logging
import math
import time
from datetime import datetime
from pathlib import Path
from textwrap import wrap
from threading import Thread

from bitstring import BitArray
from rich import print
from rich.console import Console
from rich.pretty import pprint

from commands import MECommands, PECommands
from commons import *
from exceptions import *
from loginit import logInit

console = Console()


def fPath(fName: str) -> Path:
    return Path(__file__).parent.joinpath(fName)

def checkFile(fName: str):
    if not Path(fName).exists():
        return False
    else:
        return True


def writePacket(f):
    @functools.wraps(f)
    def inner(*args, **kwargs):
        ret = f(*args, **kwargs)
        with open('packet.txt', 'a') as fl:
            fl.write(f"{ret}\n")
    return inner


class APID:
    def __init__(self, APID: int = 101):
        self.APID = APID
        self.segmentationGroup = 3
        self.SSC = 0
        self.spare1 = '0'
        self.PUSVersion = '001'
        self.spare2 = '0000'
        self.service = 1,
        self.subservice = 1,
        self.destinationID = 0  # Ground

    def writeHex(self):
        s = BitArray()
        sequence = f"0b00001"
        s.append(sequence)
        s.append(BitArray(uint=self.APID, length=11))
        s.append(BitArray(uint=self.segmentationGroup, length=2))
        s.append(BitArray(uint=self.SSC, length=14))
        k = BitArray()
        k.append('0b00010000')
        k.append(BitArray(uint=self.service, length=8))
        k.append(BitArray(uint=self.subservice, length=8))
        k.append(BitArray(uint=0, length=8))
        k.append('0b0')
        t0 = datetime(2022, 1, 1, 0, 0, 0)
        now = datetime.now()
        inter, dec = divmod((now-t0).total_seconds(), 1)
        a = 2**16
        f, g = divmod(dec*a, 1)
        k.append(BitArray(uint=int(inter), length=31))
        k.append(BitArray(uint=int(f), length=16))
        k.append(BitArray(uint=self.tcPacketID, length=16))
        k.append(BitArray(uint=self.segTC, length=2))
        k.append(BitArray(uint=self.TCSSC, length=14))
        s.append(BitArray(uint=int(k.len/8)-1, length=16))  # PacketLen
        s.append(k)
        self.SSC += 1
        return s.hex

    def seqControl(self, SSC: int = 0):
        self.tcPacketID = 0
        self.segTC = 3
        self.TCSSC = SSC


class TM_1(APID):
    def __init__(self, APID: int = 101):
        super().__init__(APID)
        self.service = 1

    @writePacket
    def write(self, sub: int = 1, sqCMD: int = 0, data=None):
        self.subservice = sub
        if sub in [1, 7]:
            self.seqControl(sqCMD)
            retVal = self.writeHex()
        return retVal


ACK = TM_1()


class PropagatingThread(Thread):
    def run(self):
        self.exc = None
        try:
            if hasattr(self, '_Thread__target'):
                # Thread uses name mangling prior to Python 3.
                self.ret = self._Thread__target(
                    *self._Thread__args, **self._Thread__kwargs)
            else:
                self.ret = self._target(*self._args, **self._kwargs)
        except BaseException as e:
            match e.__class__.__name__:
                case 'State_Error':
                    # Definire un 1,8
                    print("TM(1,8)")
                case 'Command_Device_Error':
                    # Definire un 1,8
                    print("TM(1,8)")
            self.exc = e

            print(e.__str__())

    def join(self, timeout=None):
        super(PropagatingThread, self).join(timeout)
        if self.exc:
            raise self.exc
        return self.ret


class Clock:
    def __init__(self):
        self.start = time.time()

    def getSeconds(self):
        now = time.time()-self.start
        return now

    def getTime(self):
        t0 = datetime(2022, 1, 1, 0, 0, 0)
        now = datetime.now()
        corse, dec = divmod((now-t0).total_seconds(), 1)
        a = 2**16
        fine, dec2 = divmod(dec*a, 1)
        return corse, fine


def background(f):
    '''
    a threading decorator
    use @background above the function you want to run in the background
    '''
    def backgrnd_func(*a, **kw):
        # threading.Thread(target=f, args=a, kwargs=kw).start()
        PropagatingThread(target=f, args=a, kwargs=kw).start()

    return backgrnd_func


class StateMachine:
    def __init__(self, name, initialState, tranTable):
        self.name = name
        self.state = initialState
        self.transitionTable = tranTable

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        print(f"{MSG.INFO}Initializing the StateMachine {value}")
        self._name = value

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        if not '_state' in self.__dict__:
            cs = STATE.NA
        else:
            cs = self.state
        print(
            f"{MSG.INFO}[magenta]TM(5,1)[/magenta] Changing the state: {cs} -> {value}")
        self._state = value

    def __str__(self): return f"Machine {self.name}\nState: {self.state}"

    @background
    def do(self, cmd: str, id: int):

        if cmd in [x for x in dir(self.Commands) if not x.startswith('_')]:
            if self.state == self.transitionTable[cmd]['initial']:
                self.state = self.transitionTable[cmd]['transient']
                action = getattr(self.Commands, cmd)
                # print('TM(1,7)')
                ACK.write(sub=7, sqCMD=id)
                retVal = action()
                self.state = self.transitionTable[cmd]['final']
                return retVal
            else:
                raise State_Error(cmd, self.state, id)

        else:
            raise Command_Device_Error(cmd, self.name, id)


class PE(StateMachine):
    def __init__(self, name, initialState, tranTable, verbose):
        super().__init__(name, initialState, tranTable)
        self.Commands = PECommands(verbose, console)

    def run(self, cmd: str, id: int):
        if cmd in self.transitionTable.keys():
            self.do(cmd, id)
        else:
            raise Command_Error(cmd, id)
    pass


class ME(StateMachine):
    def __init__(self, name, initialState, tranTable, verbose: bool = False):
        super().__init__(name, initialState, tranTable)
        self.PE = PE('PE', STATE.OFF, tranTable, verbose)
        self.Commands = MECommands(verbose, console)

    def run(self, cmd: str, id: int):
        if cmd in self.transitionTable.keys():
            # print('TM(1,1)')
            ACK.write(sub=1, sqCMD=id)
            if self.transitionTable[cmd]['destination'] == 'ME':
                self.do(cmd, id)
            if self.transitionTable[cmd]['destination'] == 'PE':
                self.PE.run(cmd, id)
        else:
            raise Command_Error(cmd, id)

    def cmd_description(self, cmd: str) -> str:
        if self.transitionTable[cmd]['destination'] == 'ME':
            action = getattr(self.Commands, cmd)
        if self.transitionTable[cmd]['destination'] == 'PE':
            action = getattr(self.PE.Commands, cmd)
        return action.__doc__


def run(machine, timer: Clock, fName: str = 'timeline.txt',
        log: logging = logging.getLogger('StateMachine'), debug: bool = False,
        verbose: bool = False):

    log.debug(f"Reading the command file {fName}")
    if debug and verbose:
        print(f"{MSG.DEBUG}Reading the command file {fName}")
    with open(fPath(fName), 'r') as f:
        lines = f.readlines()

    i = 0  # corresponding to the timeline line
    tollerance = 1e-5
    for line in lines:
        if line.strip().startswith('#'):
            # The line in the command file is commented
            continue
        else:
            parts = line.strip().split(',')
            while True:
                now = timer.getSeconds()
                if math.isclose(now, float(parts[0]), rel_tol=tollerance):
                    i += 1
                    log.info("TM(1,1)")
                    log.info(
                        f"Executing {parts[1]}: {machine.cmd_description(parts[1])} ({now})")
                    if verbose:
                        print(f"{MSG.INFO}TM(1,1)")
                        print(
                            f"{MSG.INFO}Executing {parts[1]}: {machine.cmd_description(parts[1])} ({now})")
                    try:
                        machine.run(parts[1], id=i)
                    except Command_Error as e:
                        # definire un 1,2
                        print('TM(1,2)')
                        print(e)
                    except Command_Device_Error as e:
                        # definire un 1,2
                        print('TM(1,2)')
                        print(e)
                    except State_Error as e:
                        print('TM(1,2)')
                        print(e)
                    break
                elif now > float(parts[0]):
                    i += 1
                    log.warning(
                        f"Executing {parts[1]}: {machine.cmd_description(parts[1])}"
                        f" - with delay ({now})")
                    print(
                        f"{MSG.WARNING}Executing {parts[1]}: {machine.cmd_description(parts[1])}"
                        f" - with delay ({now})")
                    try:
                        machine.run(parts[1], id=i)
                    except Command_Error as e:
                        # definire un 1,2
                        print('TM(1,2)')
                        print(e)
                    break
                else:
                    pass
    log.info(f"The execution of the timeline is finished")
    if verbose:
        print(f"{MSG.INFO}The execution of the timeline is finished")


def readCmdDb():
    with open(fPath('commandsTable.csv'), FMODE.READ) as f:
        lines = f.readlines()
    commandTable = {}
    for line in lines[1:]:
        seg = line.strip().split(',')
        commandTable[seg[0]] = {
            'destination': seg[1],
            'initial': seg[2],
            'transient': seg[3],
            'final': seg[4]
        }
    return commandTable


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Finite State Machine')
    parser.add_argument('-c', '--command', metavar='COMMAND',
                        help='Command File', default='timeline.txt')
    parser.add_argument(
        '-d', '--debug', action='store_true', help='Debug Mode')
    parser.add_argument('-v', '--verbose',
                        action='count', help='Verbose Mode')
    args = parser.parse_args()
    if args.debug:
        logLevel = logging.DEBUG
    else:
        logLevel = logging.INFO
    log = logInit(fPath('StateMachine.log'), 'StateMachine',
                  logLevel, fileMode=FMODE.WRITE)
    if args.verbose == 0:
        verbose = False
        hVerbose = False
    elif args.verbose == 1:
        verbose = True
        hVerbose = False
    else:
        verbose = True
        hVerbose = True

    if hVerbose:
        pprint(readCmdDb())

    timer = Clock()

    machine = ME('SIM', STATE.OFF, readCmdDb(), args.verbose)
    log.debug(f"Starting the Machine {machine.name}")
    run(machine, timer, args.command, log, args.debug, verbose)
