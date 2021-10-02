import datetime
import json
import logging
import sys

from utils.encoder import Encoder


class Logger:
    __slots__ = "logger"

    def __init__(self, class_name=None) -> None:
        self.logger = LogHandler().app_logger(class_name=class_name)

    def debug(self, msg, *args, **kwargs):
        log_json = self.__prepare_log(msg, args, kwargs)
        self.logger.debug(json.dumps(log_json, cls=Encoder))

    def info(self, msg, *args, **kwargs):
        log_json = self.__prepare_log(msg, args, kwargs)
        self.logger.info(json.dumps(log_json, cls=Encoder))

    def warning(self, msg, *args, **kwargs):
        log_json = self.__prepare_log(msg, args, kwargs)
        self.logger.warning(json.dumps(log_json, cls=Encoder))

    def error(self, msg, *args, **kwargs):
        log_json = self.__prepare_log(msg, args, kwargs)
        self.logger.error(json.dumps(log_json, cls=Encoder))

    def fatal(self, msg, *args, **kwargs):
        log_json = self.__prepare_log(msg, args, kwargs)
        self.logger.fatal(json.dumps(log_json, cls=Encoder))

    @staticmethod
    def __prepare_log(msg, args, kwargs):
        record = dict()
        if type(msg) == dict:
            record.update(msg)

        for arg in args:
            if type(arg) == dict:
                record.update(arg)

        record.update(kwargs)
        log_json = dict(message_dict=record, message=msg)
        return log_json


class LogHandler(object):
    loggers = {}

    def app_logger(self, class_name=None):
        if class_name is None:
            class_name = "undefined"

        if self.loggers.get(class_name):
            logger = self.loggers.get(class_name)

            return logger

        else:
            logger = logging.getLogger(class_name)
            log_level = logging.DEBUG

            # create a sys stdout handler
            handler = logging.StreamHandler(sys.stdout)
            handler.setLevel(log_level)

            logging.basicConfig(level=log_level)

            formatter = Formatter(self)

            handler.setFormatter(formatter)

            # add the handlers to the logger
            logger.propagate = False
            logger.addHandler(handler)

            # Save new logger to existing loggers
            self.loggers.update({class_name: logger})

            return logger


class Formatter(logging.Formatter):
    def __init__(self, log_handler, *args, **kwargs):
        super(Formatter, self).__init__(*args, **kwargs)
        self.log_handler = log_handler

    def format(self, logger):

        payload = json.loads(logger.getMessage())
        log_status = dict(
            severity=logger.levelname,
            message=payload.get("message"),
            timestamp=str(
                datetime.datetime.now(
                    datetime.timezone(offset=datetime.timedelta(hours=-3))
                )
            ),
        )

        return json.dumps(log_status)
