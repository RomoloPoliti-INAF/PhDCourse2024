#! /usr/bin/env python3
import argparse
import logging
from loginit import logInit
from rich import print
from commons import FMODE, MSG, STATE



def run(command:str,log:logging,debug:bool=False,verbose:bool=False)->None:
    log.debug("Reading the command file")
    if debug and verbose:
        print(f"{MSG.DEBUG}Reading the command file")
    with open(command,FMODE.READ) as f:
        lines=f.readlines()
        
    for line in lines:
        if line.strip().startswith('#'):
            continue
        else:
            print(line.strip())
    
if __name__ == '__main__':
    parser=argparse.ArgumentParser(description='Finite State Machine')
    parser.add_argument('-c', '--command',metavar='COMMAND', help='Command File',default='timeline.txt')
    parser.add_argument('-d', '--debug',action='store_true', help='Debug Mode')
    parser.add_argument('-v','--verbose',action='store_true', help='Verbose Mode')
    args=parser.parse_args()
    if args.debug:
        logLevel=logging.DEBUG
    else:
        logLevel=logging.INFO
    log=logInit('StateMachine.log','StateMachine',logLevel,fileMode=FMODE.WRITE)
    run(args.command,log,args.debug,args.verbose)





