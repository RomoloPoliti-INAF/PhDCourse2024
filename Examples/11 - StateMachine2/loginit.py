import logging
from commons import FMODE

__version__="1.2.0"
def logInit(logName, logger, logLevel=20,fileMode=FMODE.APPEND):
    """Inizialize the logger"""    
    flag = False 
    if not logLevel in [0, 10, 20, 30, 40, 50]:
        oldLevel=logLevel
        flag=True
        logLevel = 20
    logging.basicConfig(filename=logName,
                        level=logLevel,
                        filemode=fileMode,
                        format='%(asctime)s | %(levelname)-8s | %(name)-7s | %(module)-10s | %(funcName)-20s | %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')
    a1 = logging.getLogger(logger)
    if flag:
        a1.warning(f"Log level {oldLevel} is not valid. Used the default value 20")
    return a1  # logging
