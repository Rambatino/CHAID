class MappingDict(dict):
    """ a dict with a default value when no key present """
    def __missing__(self, key):
        """
        Returns true if the key is not found.

        Args:
            self: (todo): write your description
            key: (str): write your description
        """
        value = self[key] = [key]
        return value
