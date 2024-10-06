
import time
from datetime import datetime
from os import environ
from pathlib import Path
from threading import Thread

import yaml
from rich import print
from rich.table import Table
from rich.text import Text
from rich.pretty import pprint

from commands import MECommands, PECommands
from commons import FMODE, MSG, STATE
from console import console
from exceptions import (Command_Error,  State_Error, Command_Device_Error, Command_Error_Parameters,
                        Command_Error_Parameter)
import logging
import numpy as np


class Parameter:
    def __init__(self, item: dict):
        self.name = item['name']
        self.description = item['description']
        self.unit = item['unit']
        self.default = item['default']
        self.Value = None
        

class Command:
    def __init__(self, cName, confFile: Path):
        cfg = yaml.safe_load(open(confFile, FMODE.READ))
        flag = False
        for elem in cfg['commands']:
            # for item in elem:
            #     setattr(self,item, elem[item])
            if elem['name'] == cName:
                self.name = elem["name"]
                self.destination = elem["destination"]
                self.description = elem['description']
                self.initial = elem['initial']
                self.transient = elem['transient']
                self.final = elem['final']
                self.paramenters = []
                if elem['parameters']:
                    for item in elem['parameters']:
                        self.paramenters.append(Parameter(item))
                flag = True

        if not flag:
            console.log(f"{MSG.ERROR}Command {cName} not found")
            raise Command_Error(cName)

    def show(self, params=None):
        console.print(Text(self.name, style="bold yellow", justify="center"))
        console.print(Text(self.description, justify="center"))
        console.print(f"Destination: [blue]{self.destination}[/blue]")
        tab = Table()
        tab.add_column('Initial')
        tab.add_column('Transient')
        tab.add_column('Final')
        tab.add_row(self.initial, self.transient, self.final)
        console.print(tab)
        if len(self.paramenters) == 0:
            console.print(Text("No parameters", style="bold red"))
        else:
            tb = Table()
            tb.add_column('Parameter Name')
            tb.add_column('Description')
            if params:
                tb.add_column("Value", justify='right')
                for item in self.paramenters:
                    tb.add_row(item.name, item.description,
                               str(params[item.name]))
            else:
                for item in self.paramenters:
                    tb.add_row(item.name, item.description)
            console.print(tb)

    def validate(self, cmd: str):
        params = {}
        parts = cmd.strip().split(' ', 1)
        if not self.name == parts[0]:
            raise Command_Error(parts[0])
        if len(self.paramenters) == 0:
            if len(parts) > 1:
                console.print("TM(1,2)")
                raise Command_Error_Parameters(self.name)
        else:
            
            if len(parts) > 1:
                prm = parts[1].split(',')

                for item in prm:
                    seg = item.split(':')
                    params[seg[0].strip()] = seg[1].strip()
            for item in self.paramenters:
                if item.name in params.keys():
                    console.print(
                        f"{MSG.INFO}Parameter {item.name} Valued: {params[item.name]}")
                else:
                    if 'default' in item.__dict__.keys():
                        params[item.name] = item.default
                        console.print(
                            f"{MSG.INFO}Parameter {item.name} Default Valued: {params[item.name]}")
                    else:
                        console.print("TM(1,2)")
                        raise Command_Error_Parameter(self.name, item.name)

        return params


class Commands:
    def __init__(self, fName: Path, verbose: bool = False):
        self.verbose = verbose
        self.configuration = fName
        self.commands = []
        if verbose > 1:
            console.print(f"{MSG.INFO}Loading the configuration file {fName}")

    def getCommand(self, cName: str):
        for element in self.commands:
            if element.name == cName:
                return element
        else:
            console.log("Adding the command")
            temp = Command(cName, self.configuration)
            self.commands.append(temp)
            return temp

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
                    console.print("TM(1,8)")
                case 'Command_Device_Error':
                    # Definire un 1,8
                    console.print("TM(1,8)")
            self.exc = e

            console.print(e.__str__())

    def join(self, timeout=None):
        super(PropagatingThread, self).join(timeout)
        if self.exc:
            raise self.exc
        return self.ret


def background(f):
    '''
    a threading decorator
    use @background above the function you want to run in the background
    '''

    def backgrnd_func(*a, **kw):
        if 'TIMELINE_FILE' in environ:
            k = f(*a, **kw)
            return k
        else:

            # threading.Thread(target=f, args=a, kwargs=kw).start()
            k=PropagatingThread(target=f, args=a, kwargs=kw)
            k.start()
            a=k.join()
            return a
    return backgrnd_func


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


class StaticMachine:
    def __init__(self, name, initialState, tranTable):
        self.name = name
        self.state = initialState
        self.commandsList = Commands(tranTable)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        console.print(f"{MSG.INFO}Initializing the StateMachine {value}")
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
        console.print(
            f"{MSG.INFO}[magenta]TM(5,1)[/magenta] Changing the {self.name} state: {cs} -> {value}")
        self._state = value

    def __str__(self): return f"Machine {self.name}\nState: {self.state}"
    
    def show(self):
        if self.state==STATE.IDLE:
            color="green"
        elif self.state==STATE.BUSY:
            color="yellow"
        elif self.state==STATE.OFF:
            color="red"
        console.print(f"[bold green]{self.name}:[/bold green]\t[{color}]{self.state}[/{color}]")


class DynamicMachine(StaticMachine):

    def do(self, cmd: Command, id: int, params: dict):
        if cmd.name in [x for x in dir(self.Commands) if not x.startswith('_')]:
            if self.state == cmd.initial:
                self.state = cmd.transient
                action = getattr(self.Commands, cmd.name)
                # console.print('TM(1,7)')
                # ACK.write(sub=7, sqCMD=id)
                try:
                    retVal = action(params=params, caller=self)
                except State_Error as e:
                    self.show()
                    console.print('TM(1,8)')
                    console.print(e.__str__())
                    retVal = None
                # console.print("TM(1,7)")
                self.state = cmd.final
                
                return retVal
            else:
                raise State_Error(cmd, self.state, id)

        else:
            # console.print(dir(self.Commands))
            # console.print(cmd)
            raise Command_Device_Error(cmd, self.name, id)

class FP(StaticMachine):
    
    def acquire(self, params: dict):
        self.state=STATE.BUSY
        row=256
        col=256
        img=np.ones((row,col))
        time.sleep(params['PSS00001'])
        self.state=STATE.IDLE
        return img

class PE(DynamicMachine):
    def __init__(self, name, initialState, tranTable, verbose):
        super().__init__(name, initialState, tranTable)
        self.FP=FP("FP", STATE.OFF, tranTable)
        self.Commands = PECommands(verbose)

    @background
    def do(self, cmd: Command, id: int, params: dict):
        ret=super().do(cmd, id, params)
        return ret
        
        
    def run(self, cmd: Command, id: int, params: dict):
        retVal = self.do(cmd, id, params)
        return retVal
    
    def show(self):
        super().show()
        self.FP.show()

class CMP(StaticMachine):

    pass

class ME(DynamicMachine):
    def __init__(self, name, initialState, tranTable, verbose: int = 0,log:logging=None):
        super().__init__(name, initialState, tranTable)
        self.log=log
        self.PE = PE('PE', STATE.OFF, tranTable, verbose)
        self.CMP=CMP("CMP", STATE.OFF, tranTable)
        self.verbose=verbose
        self.Commands = MECommands(verbose)

    @background
    def do(self, cmd: Command, id: int, params: dict):
        ret=super().do(cmd, id, params)
        # pprint(ret)
        # if 'img' in ret.keys():
        #     console.log("Checking the image compressor")
        #     if self.CMP.status == STATE.IDLE:
        #         console.print("compressione")
        #     else:
        #         raise State_Error(
        #             cmd.name, "CMP", self.CMP.state, id)
        return ret
        
    
    def run(self, cmd: Command, id: int):  # , cmdInfo: dict):
        parts = cmd.strip().split(' ')
        cmd_to_run = self.commandsList.getCommand(parts[0])
        # cmd_to_run.show()
        params = cmd_to_run.validate(cmd)
        # cmd_to_run.show(params)
        # console.print('TM(1,1)')
        # ACK.write(sub=1, sqCMD=id)
        if self.state == STATE.OFF and cmd_to_run.name != 'NSS00001':
            raise State_Error(cmd_to_run.name, "ME", self.state, id)
        if cmd_to_run.destination == 'ME':
            if self.state == cmd_to_run.initial:
                console.log("executing ME command")
                self.log.info("TM(1,1)")
                self.log.info(
                    f"Executing {cmd}: { cmd_to_run.description}")
                if self.verbose:
                    console.print(f"{MSG.INFO}TM(1,1)")
                    console.print(
                        f"{MSG.INFO}Executing {cmd}: {cmd_to_run.description} ")
                retVal = self.do(cmd_to_run, id, params)

                

            else:
                raise State_Error(cmd_to_run.name, "ME",self.state, id)
        if cmd_to_run.destination == 'PE':
            if self.PE.state == cmd_to_run.initial:
                retVal = self.PE.run(cmd_to_run, id, params)
                if 'img' in retVal.keys():
                    console.log("Checking the image compressor")
                    if self.CMP.state == STATE.IDLE:
                        console.print("compressione")
                    else:
                        raise State_Error(
                            cmd_to_run.name, "CMP", self.CMP.state, id)
            else:
                raise State_Error(cmd_to_run.name,"PE", self.PE.state, id)
        return retVal

    def cmd_description(self, cmd: str) -> str:
        # a = self.commandsList.getCommand(cmd)
        tab = Table.grid()
        tab.add_column(style="green")
        tab.add_column()
        tab.add_column()
        lista = yaml.safe_load(open(self.commandsList.configuration))
        for elem in lista['commands']:
            if elem['name'] == cmd:
                tab.add_row(elem['name'], '  ', elem['description'])
            else:
                continue
        console.print(tab)

    def show_cmd(self, cName):
        a = self.commandsList.getCommand(cName)
        a.show()

    def list_cmd(self):
        tab = Table.grid()
        tab.add_column(style="green")
        tab.add_column()
        tab.add_column()
        lista = yaml.safe_load(open(self.commandsList.configuration))
        for elem in lista['commands']:
            tab.add_row(elem['name'], '  ', elem['description'])
        console.print(tab)
    
    def show(self):
        super().show()
        self.PE.show()
        self.CMP.show()









