import os

config = {
    "vulnerabilities_path": os.path.abspath("./vulnerabilities"),
}


class Config():

    def get(self, key):
        if key in config:
            return config[key]
        else:
            raise KeyError('No such config key')
