"""Simple multiprocessing queue."""

import multiprocessing as mp
import queue
from typing import Callable, Any


def worker(work_queue: mp.Queue, output_queue: mp.Queue, create_state: Callable = None):
    """Worker function.

    Retrieves tasks from ``work_queue``, puts outputs into ``output_queue``.
    Optionally initializes state and uses said state as the first argument to functions.

    :param work_queue: mp.Queue with incoming tasks, contains tuples with (id, func, args, kwargs), where
                       id -- task identifier, func -- function to run, args/kwargs -- func arguments
    :param output_queue: mp.Queue with function outputs in (id, output) format
    :param create_state: a function that initializes worker state
    """
    state = None
    if create_state is not None:
        state = create_state()

    for identifier, func, args, kwargs in iter(work_queue.get, 'STOP'):
        if create_state is not None:
            output = func(state, *args, **kwargs)
        else:
            output = func(*args, **kwargs)

        output_queue.put((identifier, output))


class TaskQueue:
    """Multiprocessing based task queue.

    Results are deleted after query.
    """

    def __init__(self, num_workers: int = 4, queue_size: int = 10, create_state: Callable = None, context='fork'):
        """Create TaskQueue and launch workers.

        :param num_workers: number of mp.Processes launched
        :param queue_size: max size of tasks in queue
        :param create_state: function that sets up state of each worker on launch
        """
        self.num_workers = num_workers
        self.queue_size = queue_size
        self.create_state = create_state

        self.processes = []
        self.ctx = mp.get_context('fork')
        self.task_queue = self.ctx.Queue(maxsize=queue_size)
        self.output_queue = self.ctx.Queue()
        self.outputs = {}

        self.__launch_workers()

    def __del__(self):
        """Destructor for TaskQueue."""
        self.__terminate_workers()

    def __launch_workers(self):
        """Launch worker processes."""
        for i in range(self.num_workers):
            self.processes.append(
                self.ctx.Process(target=worker, args=(self.task_queue, self.output_queue, self.create_state))
            )

        for p in self.processes:
            p.start()

    def __terminate_workers(self):
        """Send stop signals to each worker and join processes."""
        for i in range(self.num_workers):
            self.task_queue.put('STOP')
        for p in self.processes:
            p.join()

    def __collect_results(self):
        """Collect all outputs from output_queue."""
        while True:
            try:
                identifier, output = self.output_queue.get_nowait()
                self.outputs[identifier] = output
            except queue.Empty:
                break

    def put_task(self, identifier: str, func: Callable, *args, **kwargs) -> bool:
        """Try putting task into TaskQueue.

        Returns whether the operation was successful.

        :param identifier: a string identifier for output retrieval
        :param func: a function to call inside the task
        :param args: positional func arguments
        :param kwargs: named func arguments

        :return: ``False`` if queue was full, ``True`` otherwise
        """
        try:
            self.task_queue.put((identifier, func, args, kwargs), block=False)
            return True
        except queue.Full:
            return False

    def get_result(self, identifier: str) -> (bool, Any):
        """Try getting result from TaskQueue.

        Return whether the operation was successful and the result (or None).

        :param identifier: a string identifier of result
        :return: ``True`` and output if the task completed, ``False`` and ``None`` if not
        """
        self.__collect_results()

        found = identifier in self.outputs
        output = self.outputs.get(identifier)

        if found:
            del self.outputs[identifier]

        return found, output

    def close(self):
        """Close TaskQueue for putting new tasks."""
        self.__terminate_workers()
