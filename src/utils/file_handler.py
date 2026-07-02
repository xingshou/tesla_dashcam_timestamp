import re
from pathlib import Path


class FileHandler:
    def get_timestamp_groups(self, directory: Path) -> set[str]:
        timestamp_pattern = re.compile(
            r"(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})-(?:back|front|left_repeater|right_repeater)\.mp4")
        timestamps = set()
        for file in directory.glob("*.mp4"):
            match = timestamp_pattern.match(file.name)
            if match:
                timestamps.add(match.group(1))
        return timestamps
