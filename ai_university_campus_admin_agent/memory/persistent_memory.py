"""Persistent memory store (placeholder)."""

class PersistentMemory:
    def save(self, key, value):
        raise NotImplementedError()

    def load(self, key):
        raise NotImplementedError()
