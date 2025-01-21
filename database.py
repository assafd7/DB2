
class Database:
    def __init__(self):
        """Initialize in-memory database."""
        self.data_dict = {}

    def value_set(self, key, val):
        """Insert key-value pair into database; return True if successful."""
        try:
            self.data_dict[key] = val
            return True
        except KeyError:
            return False

    def value_get(self, key):
        """Return the value associated with the key, or None if not found."""
        return self.data_dict.get(key)

    def value_delete(self, key):
        """Delete key from database and return its value, or None if not found."""
        return self.data_dict.pop(key, None)
