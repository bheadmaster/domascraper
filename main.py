#!/usr/bin/env python3

import logging
import multiprocessing

from src.gui import GUI
from src.worker import Worker



def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(name)s:%(lineno)d %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )

    workers = [ Worker() for i in range(multiprocessing.cpu_count()) ]
    try:
        GUI(workers).run()
    finally:
        [ worker.stop() for worker in workers ]


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
