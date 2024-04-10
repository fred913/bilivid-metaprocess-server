import requests
import threading

import typing as t


class WebConnectionPool:

    def __init__(self) -> None:
        self._connections: dict[str, requests.Session] = dict()

    def _get_connection_for_current_thread(self):
        try:
            return self._connections[threading.current_thread().name]
        except KeyError:
            return self._reset_connection_for_current_thread()

    def _reset_connection_for_current_thread(self):
        return self._reset_connection(threading.current_thread().name)

    def _reset_connection(self, thread_name):
        sess = requests.Session()
        self._connections[thread_name] = sess
        return sess

    @property
    def sess(self):
        return self._get_connection_for_current_thread()
