"""Small tool to create separate thread for running the queued collections while polling
the blueapi worker while avoiding freezing the UI."""

from collections import deque
from time import sleep

from blueapi.worker import WorkerState
from PyQt6.QtCore import QMutex, QObject, pyqtSignal, pyqtSlot

from i19serial_ui.blueapi_tools.blueapi_client import SerialBlueapiClient
from i19serial_ui.log import LOGGER
from i19serial_ui.parameters.queue import QueueElement

POLL_TIME_S = 1.0


class BlueapiQueueRunner(QObject):
    finished = pyqtSignal()
    task_done = pyqtSignal(int)  # This will be to remove items from queue

    def __init__(self, client: SerialBlueapiClient, queued_tasks: deque[QueueElement]):
        self.logger = LOGGER
        self.queue = queued_tasks
        self._client = client
        self._running = True
        self._mutex = QMutex()
        super().__init__()

    def running(self):
        try:
            self._mutex.lock()
            return self._running
        finally:
            self._mutex.unlock()

    def _wait_for_task(self):
        while True:
            current_state = self._client.get_worker_state()
            print(f"CURRENT STATE: {current_state}")
            if current_state == WorkerState.IDLE:
                print("CAN START NEXT TASK")
                break
            if current_state == WorkerState.ABORTING:
                print("OOOPS PRESSED ABORT")
                break
            print("TASK STILL RUNNING")
            sleep(POLL_TIME_S)

    @pyqtSlot()
    def start(self):
        self._running = True
        try:
            while self._running and len(self.queue) > 0:
                task = self.queue.popleft()
                self.logger.info(f"RUN TASK with {task.plan_params['exposure_time_s']}")
                self._client.run_plan(
                    "sleep", {"time": task.plan_params["exposure_time_s"]}
                )
                self._wait_for_task()
                print("TASK NOW DONE - MOVING TO NEXT ONE")
        except Exception as e:
            self.logger.error("Queue failed. Please check logs for full error trace")
            self.logger.exception(e)
        self.logger.debug("Queue finished - exiting runner thread")
        self.finished.emit()

    @pyqtSlot()
    def stop(self):
        self._mutex.lock()
        self._running = False
        self.finished.emit()
        self._mutex.unlock()
