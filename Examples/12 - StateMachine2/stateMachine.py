#! /usr/bin/env python3
import argparse
import logging
import math
import traceback
from functools import wraps
from os import environ
from pathlib import Path

import yaml
from rich import print
from rich.pretty import pprint
from rich.prompt import Prompt
from rich.table import Table
from rich.panel import Panel

from classes import ME, Clock
from commons import FMODE, STATE
from console import console
from exceptions import *
from loginit import logInit


def fPath(fName: str) -> Path:
    return Path(__file__).parent.joinpath(fName)


def readCmdDb(fName: Path) -> dict:
    with open(fPath(fName), FMODE.READ) as f:
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


def writeTimeLine(f):
    @wraps(f)
    def inner(*args, **kwargs):
        with open(fPath(environ['TIMELINE_FILE']), FMODE.APPEND) as fl:
            fl.write(f"{timer.getSeconds()},{args[1]}\n")
        return f(*args, **kwargs)
    return inner

@writeTimeLine
def exec(machine, cmd, id=None):
    console.log(f"running command {cmd}")
    machine.run(cmd, id)

def interact(machine, timer: Clock, cfg: dict,
             log: logging = logging.getLogger('StateMachine'), debug: bool = False,
             verbose: bool = False):
    environ.setdefault('TIMELINE_FILE', cfg['cmdHistory'])
    console.rule(style='green')
    console.print("Welcome to State Machine",
                  style='bold red on yellow', justify='center')
    console.rule(style='green')
    while True:
        cmd = Prompt.ask('command')
        cmd = cmd.strip().upper()
        if cmd.startswith('N'):
            try:
                exec(machine, cmd)
            except Command_Error as e:
                # definire un 1,2
                console.print('TM(1,2)')
                console.print(e.__str__())
            except Command_Device_Error as e:
                # definire un 1,2
                console.print('TM(1,2)')
                console.print(e.__str__())
                traceback.print_exc()
            except State_Error as e:
                machine.show()
                console.print('TM(1,2)')
                console.print(e.__str__())
        else:
            sect = cmd.split(' ')
            if sect[0] in ['EXIT','X','Q','E']:
                console.rule(style='green')
                console.print("Goodbye!!!",
                  style='bold red on yellow', justify='center')
                console.rule(style='green')
                break
            elif sect[0] in ['HELP','H','?']:
                if len(sect) == 1:
                    machine.list_cmd()
                    tb2 = Table.grid()
                    tb2.add_column(style='yellow')
                    tb2.add_column()
                    tb2.add_column()
                    tb2.add_row('EXIT/X/Q/E', '    ',
                                'To exit from the interactive mode')
                    tb2.add_row('HELP/H/?', ' ', 'Display this help')
                    tb2.add_row('STATUS', ' ',
                                'Display the status of the StateMachine')
                    tb2.add_row('SHOW','','Show Command information')
                    console.print(Panel(tb2, title='Internal Commands'))
                else:
                    machine.cmd_description(sect[1])
            elif sect[0] == "SHOW":
                if len(sect) == 1:
                    console.print(f"{MSG.ERROR}command name is missing")
                else:
                    for elem in sect[1:]:
                        machine.show_cmd(elem)
            elif sect[0] == "STATUS":
                machine.show()


def batch(machine, timer: Clock, fName: str = 'timeline.txt',
        log: logging = logging.getLogger('StateMachine'), debug: bool = False,
        verbose: bool = False):

    log.debug(f"Reading the command file {fName}")
    if debug and verbose:
        console.print(f"{MSG.DEBUG}Reading the command file {fName}")
    with open(fPath(fName), 'r') as f:
        lines = f.readlines()

    i = 0  # corresponding to the timeline line
    tollerance = 1e-5
    for line in lines:
        if line.strip().startswith('#') or line.strip()=="":
            # The line in the command file is commented
            continue
        else:
            parts = line.strip().split(',')
            while True:

                now = timer.getSeconds()
                if math.isclose(now, float(parts[0]), rel_tol=tollerance):
                    i += 1
                    try:
                        machine.run(','.join(parts[1:]), id=i)
                    except Command_Error as e:
                        # definire un 1,2
                        console.print('TM(1,2)')
                        console.print(e.__str__())
                    except Command_Device_Error as e:
                        # definire un 1,2
                        console.print('TM(1,2)')
                        console.print(e.__str__())
                    except State_Error as e:
                        console.print('TM(1,2)')
                        console.print(e.__str__())
                    break
                elif now > float(parts[0]):
                    i += 1
                    log.warning(
                        f"Executing {parts[1]}: {machine.cmd_description(parts[1])}"
                        f" - with delay ({now})")
                    console.print(
                        f"{MSG.WARNING}Executing {parts[1]}: {machine.cmd_description(parts[1])}"
                        f" - with delay ({now})")
                    try:
                        machine.run(','.join(parts[1:]), id=i)
                    except Command_Error as e:
                        # definire un 1,2
                        console.print('TM(1,2)')
                        console.print(e)
                    break
                else:
                    pass
    log.info(f"The execution of the timeline is finished")
    if verbose:
        console.print(f"{MSG.INFO}The execution of the timeline is finished")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Finite State Machine')
    parser.add_argument('-f', '--command-file', metavar='FILE',
                        help='Command File', default='timeline.txt')
    parser.add_argument('-i', '--interactive', action='store_true',
                        help='enable the intercative mode', default=False)
    parser.add_argument('-C', '--configure', metavar="FILE",
                        type=str, help="Configuration file", default="configure.yml")
    parser.add_argument(
        '-d', '--debug', action='store_true', help='Debug Mode')
    parser.add_argument('-v', '--verbose',
                        action='count', help='Verbose Mode')
    args = parser.parse_args()
    cfg = yaml.safe_load(open(fPath(args.configure)))
    if args.debug:
        logLevel = logging.DEBUG
    else:
        logLevel = logging.INFO
    log = logInit(fPath(cfg['logFile']), 'StateMachine',
                  logLevel, fileMode=FMODE.WRITE)

    # if args.verbose >1:
    #     pprint(readCmdDb(fPath(cfg['commandTable'])))

    timer = Clock()

    machine = ME('ME', STATE.OFF, fPath(cfg['commandTable']), args.verbose,log)
    log.debug(f"Starting the Machine {machine.name}")
    if args.interactive:
        with open(fPath(cfg['cmdHistory']), FMODE.WRITE) as f:
            f.write('# Time (seconds), TC\n')
        interact(machine, timer, cfg, log, args.debug, args.verbose)
    else:
        
        batch(machine, timer, args.command_file, log, args.debug, args.verbose)
