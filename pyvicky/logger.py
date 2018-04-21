# -*- coding: utf-8 -*-

import logging
import os


class Logger:
    def __init__(self, file_path, silent):
        self.logger = logging.getLogger()

        if not os.path.exists(file_path):
            dir_path = os.path.split(file_path)[0]
            if dir_path:
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)
            f = open(file_path, 'w')
            f.close()

        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s %(levelname)s in \'%(module)s\' at line %(lineno)d: %(message)s',
                                      '%Y-%m-%d %H:%M:%S')
        file_handler = logging.FileHandler(file_path)
        file_handler.setLevel(logging.DEBUG)

        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

        if silent:
            self.logger.setLevel(logging.ERROR)  # shows only error
            # self.logger.setLevel(logging.DEBUG)  # shows info and debug and error

        logging.info('Logger initialised')
