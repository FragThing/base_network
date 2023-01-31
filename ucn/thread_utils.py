"""Multi-thread utils"""
from gevent.event import AsyncResult
from gevent.queue import Queue


def get_wait_result():
    """Return a waitable event"""
    return AsyncResult()


def get_queue():
    """Return a queuet"""
    return Queue()
