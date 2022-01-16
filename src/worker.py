from multiprocessing import Lock, Process, Queue


class Worker:
    """ Put callables in the queue, get results from the queue. """
    def __init__(self, queue: Queue = None):
        self.queue = queue or Queue()
        self.process = Process(target=self.worker_loop,
                               args=[self.queue])
        self.process.start()

    def __del__(self):
        self.stop()

    def stop(self):
        self.queue.put(None)
        self.process.join()

    @staticmethod
    def worker_loop(queue):
        while True:
            task = queue.get()
            if task is None:
                return
            self.queue.put(task())
