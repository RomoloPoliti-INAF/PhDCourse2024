types = {
    'd': 'dev',
    'a': 'alpha',
    'b': 'beta',
    'rc': 'candidate',
    'f': 'final',
}


class Version:
    """Version Class
        respecting the semantic versioning 2.0.0
    """

    def __init__(self, version: tuple):
        self.version = version

    @property
    def version(self):
        if self._type is None:
            adv = ""
        else:
            adv = f"-{self._type}"
            if self._build is not None :
                adv += f".{self._build}"
        return f"{self._major}.{self._minor}.{self._patch}{adv}"

    @version.setter
    def version(self, version):
        tags = ('_major', '_minor', '_patch', '_type', '_build')
        for tag in tags:
            setattr(self, tag, 0)
        # version=version.split(".")
        for i in range(len(version[0:3])):
            if type(version[i]) is str:
                if version[i].isdigit():
                    setattr(self, tags[i], int(version[i]))
                else:
                    raise ValueError(
                        f"{tags[i][1:].title()} version must be a number")
            elif type(version[i]) is float:
                setattr(self, tags[i], int(version[i]))
            elif type(version[i]) is int:
                setattr(self, tags[i], version[i])
        if len(version) > 3:
            if len(version[3]) == 1:
                if not version[3] in types.keys():
                    raise ValueError(f"Unknown type {version[3]}")
                else:
                    self._type = types[version[3]]
            else:
                if not version[3] in types.values():
                    raise ValueError(f"Unknown type {version[3]}")
                self._type = version[3]
        else:
            self._type = None
        if len(version) == 5:
            self._build = version[4]
        else:
            self._build = None

    def __str__(self) -> str:
        if self._type == "final":
            return f"Version {self._major}.{self._minor}.{self._patch}"
        else:
            return f"Version {self.version}"

    def full(self) -> str:
        return self.version



