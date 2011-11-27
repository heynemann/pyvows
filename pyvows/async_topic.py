
class VowsAsyncTopic(object):
    def __init__(self, func, args, kw):
        self.func = func
        self.args = args
        self.kw = kw

    def __call__(self, callback):
        args = (self.args[0], callback,) + self.args[1:]
        self.func(*args, **self.kw)


class VowsAsyncTopicValue(object):
    def __init__(self, args, kw):
        self.args = args
        self.kw = kw

    def __getitem__(self, attr):
        if type(attr) is int:
            return self.args[attr]

        if attr in self.kw:
            return self.kw[attr]

        raise AttributeError

    def __getattr__(self, attr):
        if attr in self.kw:
            return self.kw[attr]

        if hasattr(self, attr):
            return self.attr

        raise AttributeError


