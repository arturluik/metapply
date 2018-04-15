import json


class Logger():

    def debug(self, *args):
        self.format('debug', args)

    def info(self, *args):
        self.format('info', args)

    def format(self, level, args):
        message = ' '.join(list(map(lambda x: self.to_string(x), args)))
        print('[' + level + '] ' + message)

    def to_string(self, x):
        try:
            return json.dumps(x)
        except:
            return repr(x)
