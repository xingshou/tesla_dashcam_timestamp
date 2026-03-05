from pathlib import Path
from PySide6.QtCore import Signal, QObject, QTimer
from ffmpeg_progress_yield import FfmpegProgress
from datetime import datetime
from multiprocessing import Process, Queue
import logging

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def process_video(
    input_file: Path,
    output_file: Path,
    timestamp_epoch: int,
    camera: str,
    queue: Queue,
) -> None:
    """Run ffmpeg conversion in a separate process and send progress to
    queue."""
    try:
        # Ensure output directory exists
        output_file.parent.mkdir(parents=True, exist_ok=True)
        cmd = [
            "ffmpeg",
            "-i",
            str(input_file),
            "-vf",
            f"drawtext=fontsize=24:fontcolor=white:x=10:y=10:text='%{{pts\\:localtime\\:{timestamp_epoch}}}'",
            "-y",
            str(output_file),
        ]
        ff = FfmpegProgress(cmd)
        for progress in ff.run_command_with_progress():
            queue.put((camera, int(progress)))
    except Exception as e:
        logger.error("Error converting %s: %s", input_file, e)
        queue.put((camera, 100))  # Signal completion even on error


class VideoProcessor(QObject):
    progress_updated = Signal(str, int)
    conversion_finished = Signal(str)
    missing_file_detected = Signal(str)

    def __init__(self):
        super().__init__()
        self.processes: list[tuple[Process, str]] = []
        self.queue: Queue = Queue()
        self.timer: QTimer = QTimer()
        self.timer.timeout.connect(self.check_queue)
        self.active_processes: int = 0
        self.completed_cameras: set[str] = set()

    def process_videos(
        self, input_dir: Path, output_dir: Path, timestamp: str
    ) -> None:
        """Start parallel video processing for all camera files."""
        cameras = ["back", "front", "left_repeater", "right_repeater"]
        timestamp_epoch = self._timestamp_to_epoch(timestamp)
        self.active_processes = 0
        self.processes = []
        self.completed_cameras.clear()

        for camera in cameras:
            input_file = input_dir / f"{timestamp}-{camera}.mp4"
            output_file = output_dir / f"{timestamp}-{camera}.mp4"
            if input_file.exists():
                process = Process(
                    target=process_video,
                    args=(
                        input_file,
                        output_file,
                        timestamp_epoch,
                        camera,
                        self.queue,
                    ),
                )
                self.processes.append((process, camera))
                self.active_processes += 1
            else:
                logger.warning("File %s does not exist", input_file)
                self.missing_file_detected.emit(camera)
                self.completed_cameras.add(camera)

        # Start all processes
        for process, _ in self.processes:
            process.start()

        # Start polling queue for progress updates
        if self.active_processes > 0:
            self.timer.start(100)  # Check queue every 100ms

    def check_queue(self) -> None:
        """Poll the queue for progress updates."""
        while not self.queue.empty():
            camera, progress = self.queue.get()
            self.progress_updated.emit(camera, progress)
            if progress == 100 and camera not in self.completed_cameras:
                self.conversion_finished.emit(camera)
                self.completed_cameras.add(camera)
                self.active_processes -= 1

        if self.active_processes <= 0:
            self.timer.stop()
            for process, _ in self.processes:
                process.join()  # Ensure all processes are cleaned up
            self.processes = []
            logger.info("All processes completed")

    def _timestamp_to_epoch(self, timestamp: str) -> int:
        """Convert timestamp string to epoch time."""
        try:
            dt = datetime.strptime(timestamp, "%Y-%m-%d_%H-%M-%S")
            return int(dt.timestamp())
        except ValueError as e:
            logger.error("Invalid timestamp format %s: %s", timestamp, e)
            return 0
