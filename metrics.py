import time
import logging
logger = logging.getLogger(__name__)


def time_method(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        record_time( method.__name__, (te - ts) * 1000)
        return result
    return timed


def record_time(metric_name, time_in_millis):
    logger.info("METRIC - %s - %d ms", metric_name, time_in_millis)


def record_error(metric_name):
    logger.error("METRIC ERRORED - %s", metric_name)
