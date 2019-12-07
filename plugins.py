from importlib import import_module


def get_function(pth):
    sep_index = pth.rfind('.')
    module_name = pth[:sep_index]
    func_name = pth[sep_index + 1:]
    mod = import_module(module_name)
    return getattr(mod, func_name)


def func0(value):
    return 'func0: {0}'.format(value)


def func1(value):
    return 'func1: {0}'.format(value)


class PluginRegistry(dict):

    def __setattr__(self, key, value):
        self[key] = value

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            object.__getattribute__(self, key)

    def process(self, remainder, value):
        _fnc = getattr(self, 'func{0}'.format(remainder))
        return _fnc(value)
