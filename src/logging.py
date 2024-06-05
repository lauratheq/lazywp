#!/usr/bin/python3

# TODO comments
import logging

class Logging:
    logger = None
    log_level = 0
    log_levels = {
        "NOTSET": 0,
        "DEBUG": 10,
        "INFO": 20,
        "WARN": 30,
        "ERROR": 40,
        "CRITICAL": 50
    }

    def __init__(self, **kwargs):
        if 'log_level' in kwargs:
            self.log_level = kwargs['log_level']
    
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
        format = '[%(asctime)s] %(filename)s - %(message)s'
        formatter = logging.Formatter(format, "%Y-%m-%d %H:%M:%S")
        
        # file logging
        fh = logging.FileHandler('/var/log/lazywp.log')
        fh.setFormatter(formatter)
        fh.setLevel(self.log_levels[self.log_level])
        self.logger.addHandler(fh)
