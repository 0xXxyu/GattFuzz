import logging
from colorama import Fore,Style
import sys

class Logger():
    def __init__(self, loglevel=logging.INFO, loggername=None):
        self.logger = logging.getLogger(loggername)
        self.logger.setLevel(loglevel)

        formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')

        if not self.logger.handlers:
            # 日志输出到控制台
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(loglevel)
            stream_handler.setFormatter(formatter)

            self.logger.addHandler(stream_handler)
    
    def get_logger(self):
        return self.logger


# TODO 带颜色的输出
# def get_logger():
#     logger = logging.getLogger()
#     logger.setLevel(logging.DEBUG)
 
#     if not logger.handlers:
#         ch = logging.StreamHandler(sys.stdout)
#         ch.setLevel(logging.DEBUG)
#         formatter = logging.Formatter(
#             " %(message)s")
#         ch.setFormatter(formatter)
#         logger.addHandler(ch)

#     return logger

# class Logger():
 
#     logger = get_logger()
#     @staticmethod
#     def debug(msg):
#         Logger.logger.debug(Fore.WHITE + "[DEBUG]: " + str(msg) + Style.RESET_ALL)
 
#     @staticmethod
#     def info(msg):
#         Logger.logger.info(Fore.GREEN + "[INFO]: " + str(msg) + Style.RESET_ALL)
 
#     @staticmethod
#     def warning(msg):
#         Logger.logger.warning("\033[38;5;214m" + "[WARNING]: " + str(msg) + "\033[m")
 
#     @staticmethod
#     def error(msg):
#         Logger.logger.error(Fore.RED + "[ERROR]: " + str(msg) + Style.RESET_ALL)
 
#     @staticmethod
#     def critical(msg):
#         Logger.logger.critical(Fore.RED + "[CRITICAL]: " + str(msg) + Style.RESET_ALL)

# # Logger.error("error")