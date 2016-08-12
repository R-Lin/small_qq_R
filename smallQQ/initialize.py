# coding:utf8
import requests
import logging
import os


def get_req():
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82 Safari/537.36'
    }
    req = requests.session()
    req.headers.update(header)
    return req


def log():
    log_dir = 'log'
    log_file = 'default.log'
    logfile = os.path.join(log_dir, log_file)
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)

    logger = logging.Logger("mylog")
    file_stream = logging.FileHandler(logfile)
    terminal_stream = logging.StreamHandler()

    log_format = logging.Formatter('%(asctime)s [%(levelname)s] Line:%(lineno)d  %(message)s')
    file_stream.setFormatter(log_format)
    terminal_stream.setFormatter(log_format)

    logger.setLevel(logging.DEBUG)
    file_stream.setLevel(logging.WARNING)
    terminal_stream.setLevel(logging.DEBUG)

    logger.addHandler(file_stream)
    logger.addHandler(terminal_stream)
    return logger



