from commons import MSG


class Command_Error(Exception):
    def __init__(self, cmd, id=None, message='Unknown Command'):
        self.cmd = cmd
        self.message = message
        self.id = id
        super().__init__(self.message)

    def __str__(self):
        if self.id is None:
            return f"{MSG.ERROR}Command Error: {self.cmd} - {self.message}"
        else:
            return f'{MSG.ERROR} id: {self.id} {self.cmd} -> {self.message}'

class Command_Error_Parameters(Exception):
    def __init__(self, cmd, message='not require parameters'):
        self.cmd = cmd
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{MSG.ERROR}{self.cmd} {self.message}'

class Command_Error_Parameter(Exception):
    def __init__(self,cmd,parameter,message='Missing Parameter'):
        self.cmd = cmd
        self.parameter = parameter
        self.message = message
        super().__init__(self.message)
        
    def __str__(self):
        return f'{MSG.ERROR}{self.cmd} {self.message} {self.parameter}'
    
class State_Error(Exception):
    def __init__(self, cmd,name, state, id=None, message='The machine is not in the correct state to run the command'):
        self.cmd = cmd
        self.state = state
        self.name=name
        self.message = message
        self.id = id
        super().__init__(self.message)

    def __str__(self):
        if self.id:
            return f"{MSG.ERROR} id: {self.id} {self.cmd} - {self.name} [bold red]{self.state}[/bold red] -> {self.message}"
        else:
            return f"{MSG.ERROR} {self.cmd} - {self.name} [bold red]{self.state}[/bold red] -> {self.message}"


class Command_Device_Error(Exception):
    def __init__(self, cmd, name, id=None, message="The command was sent ot the wrong Device"):
        self.cmd = cmd
        self.name = name
        self.message = message
        self.id = id
        super().__init__(self.message)

    def __str__(self):
        if self.id:
            return f"{MSG.ERROR} id: {self.id} {self.cmd.name} - {self.name} -> {self.message}"
        else:
            return f"{MSG.ERROR} {self.cmd.name} - {self.name} -> {self.message}"
