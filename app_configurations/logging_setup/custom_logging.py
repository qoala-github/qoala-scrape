import datetime
import logging
import sys
import traceback
from os import listdir
from pathlib import Path
from loguru import logger
import json
from datetime import datetime

from app_configurations.app_settings import AppSetting

app_settings = AppSetting()


class InterceptHandler(logging.Handler):
    loglevel_mapping = {
        50: 'CRITICAL',
        40: 'ERROR',
        30: 'WARNING',
        20: 'INFO',
        10: 'DEBUG',
        0: 'NOTSET',
    }

    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except AttributeError:
            level = self.loglevel_mapping[record.levelno]

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        log = logger.bind(request_id='app')
        log.opt(
            depth=depth,
            exception=record.exc_info
        ).log(level, record.getMessage())


class CustomizeLogger:

    @classmethod
    def make_logger(cls, config_path: Path):
        print(f"config_path:{config_path}")
        config = cls.load_logging_config(config_path)
        logging_config = config['logger']
        print(f"logging_config:{logging_config}")
        logger = cls.customize_logging(
            logging_config.get('path'),
            level=logging_config.get('level'),
            retention=logging_config.get('retention'),
            rotation=logging_config.get('rotation'),
            log_format=logging_config.get('log_format')
        )
        return logger

    @classmethod
    def customize_logging(cls,
                          filepath: Path,
                          level: str,
                          rotation: str,
                          retention: str,
                          log_format: str
                          ):
        logger.remove()
        log_file_path = f"{filepath}/app_log_{datetime.today().strftime('%Y-%m-%d')}.log"

        logger.add(
            sys.stdout,
            enqueue=True,
            backtrace=True,
            level=level.upper(),
            format=log_format
        )
        logger.add(
            log_file_path,
            rotation=rotation,
            retention=retention,
            enqueue=True,
            backtrace=True,
            level=level.upper(),
            format=log_format
        )
        logging.basicConfig(handlers=[InterceptHandler()], level=0)
        logging.getLogger("uvicorn.access").handlers = [InterceptHandler()]
        for _log in ['uvicorn',
                     'uvicorn.error',
                     'fastapi'
                     ]:
            _logger = logging.getLogger(_log)
            _logger.handlers = [InterceptHandler()]

        return logger.bind(request_id=None, method=None)

    @classmethod
    def load_logging_config(cls, config_path):
        config = None
        with open(config_path) as config_file:
            config = json.load(config_file)
        print(config['logger'])
        print(config['logger'].get('path'))
        return config


class LogFileViewer:
    def list_log_file_types(self):
        try:
            """
               log File Types:
               1= Application log
               <<add more types in list>>
               """
            log_file_types = [("1", "App_Log")]
            return log_file_types
        except:
            print(f'LogFileViewer=>list_log_file_types:{sys.exc_info()[2]}/n{traceback.format_exc()} occurred')

    def get_all_files(self, log_file_type):
        try:
            file_list_with_path = []
            if int(log_file_type) == 1:
                log_file_path = app_settings.LOG_FILE_DIRECTORY
                file_list = listdir(log_file_path)
                for file_name in file_list:
                    file_path = f'{str(log_file_path)}/{file_name}'
                    #file_path_mod = file_path.replace('/', '**')
                    file_obj = (file_name, file_path)
                    file_list_with_path.append(file_obj)
            return file_list_with_path
        except:
            print(f'LogFileViewer=>get_all_files:{sys.exc_info()[2]}/n{traceback.format_exc()} occurred')

    def show_file_content(self, file_name):
        try:
            with open(file_name, "r") as f:
                content = f.read()
            return content
        except:
            print(f'LogFileViewer=>show_file_content:{sys.exc_info()[2]}/n{traceback.format_exc()} occurred')
