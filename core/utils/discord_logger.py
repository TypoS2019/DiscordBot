import datetime


def log(string, log_type, bot=None, save=False, ):
    levels = {'header': '\033[95m',
              'red': '\033[91m',
              'yellow': '\033[93m',
              'blue': '\033[94m'}
    end = '\033[0m'
    print(
        levels['yellow'] + "[" + datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S:%f") + "]" + end + " " +
        levels[log_type] + string + end)
    if save:
        if bot is None:
            print("Unable to save log: bot is required")
        else:
            try:
                bot.data_mapper_logger.insert_doc(
                    {"TimeStamp": datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S:%f"),
                     "message": string,
                     "level": log_type})
            except:
                print("Unable to save log")
