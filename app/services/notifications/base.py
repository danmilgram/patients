import logging
from fastapi import BackgroundTasks
from abc import ABC, abstractmethod

class NotificationChannel(ABC):
    @abstractmethod
    def send_message(self, *args):
        pass

class NotificationService(object):
    def __init__(self):
        pass

    def notify(
            self,
            channel: NotificationChannel,
            *args: list,
        ):
        try:
            channel_instance = channel()
            channel_instance.send_message(*args)
        except Exception as e:
            logging.exception(e)

