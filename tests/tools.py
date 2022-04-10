
class Mock:
    def __init__(self, obj, attr_name, new_attr):
        self._obj = obj
        self._attr_name = attr_name
        self._new_attr = new_attr
        self._old_attr = None

    def __enter__(self):
        self.old_attr = getattr(self._obj, self._attr_name)
        setattr(self._obj, self._attr_name, self._new_attr)

    def __exit__(self, exc_type, exc_val, exc_tb):
        setattr(self._obj, self._attr_name, self.old_attr)
