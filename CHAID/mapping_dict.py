class MappingDict(dict):
    """ a dict with a default value when no key present """
    def __missing__(self, key):
        value = self[key] = [key]
        return value
