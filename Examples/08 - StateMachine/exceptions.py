from commons import MSG


class Command_Error(Exception):
    def __init__(self, cmd, id, message='Unknown Command'):
        self.cmd = cmd
        self.message = message
        self.id = id
        super().__init__(self.message)

    def __str__(self):
        return f'{MSG.ERROR} id: {self.id} {self.cmd} -> {self.message}'


class State_Error(Exception):
    def __init__(self, cmd, state, id, message='The machine is not in the correct state to run the command'):
        self.cmd = cmd
        self.state = state
        self.message = message
        self.id = id
        super().__init__(self.message)

    def __str__(self):
        return f"{MSG.ERROR} id: {self.id} {self.cmd} - {self.state} -> {self.message}"


class Command_Device_Error(Exception):
    def __init__(self, cmd, name, id, message="The command was sent ot the wrong Device"):
        self.cmd = cmd
        self.name = name
        self.message = message
        self.id = id
        super().__init__(self.message)

    def __str__(self):
        return f"{MSG.ERROR} id: {self.id} {self.cmd} - {self.name} -> {self.message}"
