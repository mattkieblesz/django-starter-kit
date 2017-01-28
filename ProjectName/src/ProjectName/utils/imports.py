import pkgutil


class ModuleProxyCache(dict):
    def __missing__(self, key):
        if '.' not in key:
            return __import__(key)

        module_name, class_name = key.rsplit('.', 1)

        module = __import__(module_name, {}, {}, [class_name])
        handler = getattr(module, class_name)

        # We cache a NoneType for missing imports to avoid repeated lookups
        self[key] = handler

        return handler


_cache = ModuleProxyCache()


def import_string(path):
    result = _cache[path]
    return result


def import_submodules(context, root_module, path):
    for loader, module_name, is_pkg in pkgutil.walk_packages(path, root_module + '.'):
        # this causes a Runtime error with model conflicts
        # module = loader.find_module(module_name).load_module(module_name)
        module = __import__(module_name, globals(), locals(), ['__name__'])
        for k, v in iter(vars(module).items()):
            if not k.startswith('_'):
                context[k] = v
        context[module_name] = module
