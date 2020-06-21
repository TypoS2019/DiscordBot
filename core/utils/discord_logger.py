import datetime


def log(string, log_type, save=False):
    levels = {'header': '\033[95m',
              'red': '\033[91m',
              'yellow': '\033[93m',
              'blue': '\033[94m'}
    end = '\033[0m'
    print(
        levels['yellow'] + "[" + datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S:%f") + "]" + end + " " + levels[
            log_type] + string + end)
