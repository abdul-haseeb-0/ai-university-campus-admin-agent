"""Validation utilities for input data."""

def validate_student_id(sid):
    """Return True if student id format looks valid."""
    return isinstance(sid, str) and len(sid) > 0
