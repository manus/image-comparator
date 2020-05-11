from __future__ import (absolute_import, division, print_function)
import multiprocessing
import time
from metrics import time_method, record_time, record_error
import logging
logger = logging.getLogger(__name__)


class Consumer(multiprocessing.Process):

    def __init__(self, task_queue, output_file_name, write_output_lock):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.output_file_name = output_file_name
        self.write_output_lock = write_output_lock

    def run(self):
        proc_name = self.name
        logger.info('%s: Starting' % proc_name)
        with open(self.output_file_name, mode='a') as output_file:
            while True:
                next_task = self.task_queue.get()
                if next_task is None:
                    # Poison pill means shutdown
                    logger.info('%s: Exiting' % proc_name)
                    self.task_queue.task_done()
                    break
                task_millis_in_queue = (time.time() - next_task.create_time) * 1000
                record_time("time_in_queue", task_millis_in_queue)
                logger.info('%s processing task : %s' % (proc_name, next_task))

                # No retries for now. Try once and continue
                try:
                    output_csv = self.process_image_comparision(next_task)
                    self.save_result(output_file, output_csv)
                except BaseException as e:
                    logger.error(e, exc_info=True)
                    record_error("error_processing_comparison")

                # acknowledge message after everything is done
                self.task_queue.task_done()
        return

    @time_method
    def process_image_comparision(self, callable_task):
        try:
            output_csv = callable_task()
            return output_csv
        except:
            # Preserving stacktrace
            record_error("error_calculating_similarity")
            raise

    """
    For save_result, in an ideal world, the storage would be a database
    We would just have a connection to the database, with re-connect logic if connection drops
    Locking would be provided by the database
    """
    @time_method
    def save_result(self, output_file, output_csv):

        # Use shared lock as this is a shared file opened in append mode by multiple consumers
        with self.write_output_lock:
            try:
                # Using "\n" as line separator (https://docs.python.org/3/library/os.html#os.linesep)
                output_file.write(output_csv + "\n")
                # Flush right away as any buffering can cause in-consistent or corrupted data
                # https://stackoverflow.com/questions/7842511/safe-to-have-multiple-processes-writing-to-the-same-file-at-the-same-time-cent
                output_file.flush()
            except:
                record_error("error_writing_results")
                raise

