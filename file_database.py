import pickle
from Database import Database


class FileDatabase(Database):
    def __init__(self, filename='Database.pkl'):
        """Initialize database with filename for persistence and load existing data."""
        super().__init__()  # Initialize the base class
        self.filename = filename
        self.data_dict = self.pickle_load()  # Load data from file

    def pickle_ser(self):
        """Serialize data_dict to the file for persistence."""
        with open(self.filename, 'wb') as f:
            pickle.dump(self.data_dict, f)

    def pickle_load(self):
        """Load data from file into data_dict, or initialize if file is missing."""
        try:
            with open(self.filename, 'rb') as f:
                return pickle.load(f)
        except (FileNotFoundError, EOFError):
            return {}

    def value_set(self, key, val):
        """Insert key-value pair into database and save to file."""
        result = super().value_set(key, val)
        if result:
            self.pickle_ser()
        return result

    def value_delete(self, key):
        """Delete key from database, save to file, and return the deleted value."""
        value = super().value_delete(key)
        if value is not None:
            self.pickle_ser()
        return value
