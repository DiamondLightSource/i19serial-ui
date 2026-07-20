"""Small tool to create separate thread for polling the blueapi worker while avoiding freezing the UI."""

from time import sleep

from blueapi.worker import WorkerState
from PyQt6.QtCore import QMutex, QObject, pyqtSignal, pyqtSlot

from i19serial_ui.blueapi_tools.blueapi_client import SerialBlueapiClient
from i19serial_ui.log import LOGGER
from i19serial_ui.parameters.queue import QueueElement

POLL_TIME_S = 1.0


class BlueapiStatePoller(QObject):
    finished = pyqtSignal()

    def __init__(self, client: SerialBlueapiClient):
        self.logger = LOGGER
        self._client = client
        self._running = True
        self._mutex = QMutex()
        super().__init__()

    def set_new_task(self, task: QueueElement):
        self.task = task

    def running(self):
        try:
            self._mutex.lock()
            return self._running
        finally:
            self._mutex.unlock()

    @pyqtSlot()
    def start(self):
        self._running = True
        self.logger.info(f"RUN TASK with {self.task.plan_params['exposure_time_s']}")
        self._client.run_plan(
            "sleep", {"time": self.task.plan_params["exposure_time_s"]}
        )
        while self._running:
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
        self.logger.info("TASK DONE")
        self.finished.emit()

    @pyqtSlot()
    def stop(self):
        self._mutex.lock()
        self._running = False
        self.finished.emit()
        self._mutex.unlock()
