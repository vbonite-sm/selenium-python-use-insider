"""Utility decorators for test framework"""
import functools


def log_action(func):
    """Decorator to log function execution"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
