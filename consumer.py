from __future__ import (absolute_import, division, print_function)
import multiprocessing
import time
from metrics import time_method, record_time
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
                output_csv = self.process_image_comparision(next_task)
                self.save_result(output_file, output_csv)
                self.task_queue.task_done()
        return

    @time_method
    def process_image_comparision(self, callable_task):
        output_csv = callable_task()
        return output_csv

    @time_method
    def save_result(self, output_file, output_csv):
        with self.write_output_lock:
            output_file.write(output_csv + "\n")
            output_file.flush()


