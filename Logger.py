import logging

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