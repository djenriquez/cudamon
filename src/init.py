import os
import logging

def initialize_logger():
    log_level = getattr(logging, os.getenv('LOG_LEVEL', default='INFO').upper(), None)
    logging.basicConfig(level=log_level, format='%(levelname)s:%(asctime)s %(message)s')
