import logging
import logging.handlers
import copy
import time
import os

# from colorama import Fore,Style
def color(text, color_code):
    """Colorize text.
    @param text: text.
    @param color_code: color.
    @return: colorized text.
    """
    return "\x1b[%dm%s\x1b[0m" % (color_code, text)

def red(text):
    return color(text, 31)

def green(text):
    return color(text, 32)

def yellow(text):
    return color(text, 33)

def blue(text):
    return color(text, 34)


class ConsoleHandler(logging.StreamHandler):
    """Logging to console handler."""

    def emit(self, record):
        colored = copy.copy(record)

        if record.levelname == "WARNING":
            colored.msg = yellow(record.msg)
        elif record.levelname == "ERROR" or record.levelname == "CRITICAL":
            colored.msg = red(record.msg)
        elif record.levelname == "INFO":
            colored.msg = green(record.msg)
        elif record.levelname == "DEBUG":
            colored.msg = blue(record.msg)
        else:
            if "analysis procedure completed" in record.msg:
                colored.msg = record.msg
            else:
                colored.msg = record.msg

        logging.StreamHandler.emit(self, colored)

class Logger():
    def __init__(self, loglevel=logging.INFO, loggername=None):
        self.logger = logging.getLogger(loggername)
        self.logger.setLevel(loglevel)

        formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')

        if not self.logger.handlers:
            # 日志输出到控制台
            console_handler = ConsoleHandler()
            console_handler.setFormatter(formatter)
            # 日志保存到文件
            log_dir_path = './logs'
            if not os.path.exists(log_dir_path):
                os.mkdir(log_dir_path)
            log_file_path = os.path.join(log_dir_path, str(int(time.time())) + '.log')    
            file_handler = logging.handlers.TimedRotatingFileHandler(log_file_path, when='D',interval=5)
            file_handler.suffix = "%Y%m%d_%H%M.log"
            file_handler.setFormatter(formatter)

            self.logger.addHandler(console_handler)
            self.logger.addHandler(file_handler)
    
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