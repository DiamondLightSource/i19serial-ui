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

    def _wait_for_task(self, plan_name: str):
        while True:
            current_state = self._client.get_worker_state()
            self.logger.debug(f"Current blueapi state: {current_state}")
            if current_state == WorkerState.IDLE:
                self.logger.info(f"Plan {plan_name} finished, can start next task")
                break
            if current_state == WorkerState.ABORTING:
                # May actually be overkill
                self.logger.warning("Abort button pressed, will stop task")
                break
            # TODO replace with progress bar maybe?
            self.logger.info(f"Running {plan_name}")
            sleep(POLL_TIME_S)

    @pyqtSlot()
    def start(self):
        self._running = True
        try:
            while self._running and len(self.queue) > 0:
                task = self.queue.popleft()
                self.logger.info(f"Start task {task.element_label}")
                self.logger.info(f"With parameters: {task.plan_params}")
                self._client.run_plan(task.plan_name, {"parameters": task.plan_params})
                # TODO DEV
                # self.logger.info(
                #   f"RUN TASK with {task.plan_params['exposure_time_s']}"
                # )
                # self._client.run_plan(
                #     "sleep", {"time": task.plan_params["exposure_time_s"]}
                # )
                self._wait_for_task(task.plan_name)
                print("TASK NOW DONE - MOVING TO NEXT ONE")
                self.task_done.emit(0)
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
