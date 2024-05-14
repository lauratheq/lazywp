#!/usr/bin/python3

# TODO comments
import logging
import src.config as config

class Logging:
    logger = None
    log_level = config.LOG_LEVEL
    log_levels = {
        "NOTSET": 0,
        "DEBUG": 10,
        "INFO": 20,
        "WARN": 30,
        "ERROR": 40,
        "CRITICAL": 50
    }

    def __init__(self, *args):
        if 'log_level' in args:
            self.log_level = args.log_level
    
         # initialize logger
        self.init_logger()
        
    def init_logger(self):
        '''
        initializes the logger and sets the log level

        Parameters:
            self (obj): the class object

        Returns:
            void
        '''

        self.logger = logging.getLogger('lazywp')
        self.logger.setLevel(self.log_levels[self.log_level])
        format = '%(asctime)s - %(levelname)s - %(filename)s - %(message)s'
        formatter = logging.Formatter(format)
        
        # file logging
        fh = logging.FileHandler('/var/log/lazywp.log')
        fh.setFormatter(formatter)
        fh.setLevel(self.log_levels[self.log_level])
        self.logger.addHandler(fh)
