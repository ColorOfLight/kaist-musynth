import logging
from pytz import timezone, utc
from datetime import datetime

class Logger:
  def __init__(self, logger_name):
    log_fn = '../logs/' + logger_name + '.log' 
    self.logger = self._set_logger(logger_name, log_fn)
    self.logger.debug("========== New Logger ===========")

  def write(self, content):
    self.logger.info(content)

  def log(self, content):
    self.logger.debug(content)

  def console(self, content):
    print(content)

  def _set_logger(self, name, log_path):
    # logger 인스턴스를 생성 및 로그 레벨 설정
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # fileHandler와 StreamHandler를 생성
    final_log_path = log_path + \
              '.log' if not log_path.endswith('.log') else log_path
    fileHandler = logging.FileHandler(final_log_path)
    streamHandler = logging.StreamHandler()

    fileHandler.setLevel(logging.DEBUG)
    streamHandler.setLevel(logging.INFO)

    log_format = '[%(asctime)s:%(lineno)03s] %(message)s'
    formatter = logging.Formatter(log_format)

    def customTime(*args):
      utc_dt = utc.localize(datetime.utcnow())
      my_tz = timezone("Asia/Seoul")
      converted = utc_dt.astimezone(my_tz)
      return converted.timetuple()

    logging.Formatter.converter = customTime

    fileHandler.setFormatter(formatter)
    streamHandler.setFormatter(formatter)

    # Handler를 logging에 추가
    logger.addHandler(fileHandler)
    logger.addHandler(streamHandler)

    return logger
