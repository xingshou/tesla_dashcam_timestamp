# tesla_dashcam_timestamp

**Version: v0.1.2**

tesla_dash_cam is a Python application designed to process Tesla dashcam video files by overlaying timestamps using FFmpeg. It provides a user-friendly GUI built with PySide6, allowing users to select input and output directories, view grouped video files, and convert them in parallel with real-time progress updates.

## Features

- **Directory Selection**: Select input and output directories for Tesla dashcam videos.
- **File Grouping**: Groups video files by timestamp (e.g., `yyyy-mm-dd_hh-mm-ss`), ignoring non-matching files.
- **Parallel Conversion**: Converts videos from four cameras (`back`, `front`, `left_repeater`, `right_repeater`) in parallel using `multiprocessing`.
- **Progress Monitoring**: Displays full file names, progress bars, and percentage labels for each camera.
- **Missing File Handling**: Marks non-existent files as `Missing` without updating their progress.
- **User-Friendly GUI**: Disables file and directory selection during conversion and resets status on new selections.
- **Output Directory Validation**: Prevents selecting the same directory for both input and output.

## Installation

### Prerequisites

- Python 3.10 or higher
- FFmpeg installed on your system
  - macOS: `brew install ffmpeg`
  - Ubuntu: `sudo apt-get install ffmpeg`
  - Windows: Download from [FFmpeg website](https://ffmpeg.org/download.html) and add to PATH

### Python Dependencies

Install the required Python packages using pip:

```bash
pip install PySide6 ffmpeg-progress-yield
```

## Project Setup

Clone or download the repository, then navigate to the project directory:

```bash
cd tesla_dash_cam
```


## Usage

1. Run the application:

```bash
python src/main.py
```

2. Run the GUI to:

- Click "Select" to choose an "Input Directory" with Tesla dashcam videos.
- Click "Select" to choose an "Output Directory" to save output videos.
- Select a timestamp from the file list to view available videos.
- Click "Convert" to process the videos, with progress displayed in real-time.

3. Check the output files (yyyy-mm-dd_hh-mm-ss-camera.mp4) in the selected output directory.


## Directory Structure

```text
tesla_dash_cam/
├── src/
│   ├── core/
│   │   └── video_processor.py
│   ├── main.py
│   ├── ui/
│   │   └── main_window.py
│   └── utils/
│       └── file_handler.py
└── README.md
```


## Screenshots

Below are screenshots showcasing the tesla_dash_cam application in action:

- **File Selection**: Displays the list of timestamp-grouped video files available for selection in the chosen directory.
  ![File Selection](screenshots/file_selection.png)

- **Conversion Progress**: Shows the conversion process with file names, progress bars, and percentage labels for each camera.
  ![Conversion Progress](screenshots/conversion_progress.png)


## Logging

- The application logs critical events at the INFO level (e.g., conversion completion).
- Errors and warnings (e.g., missing files, invalid timestamps) are logged for debugging.


## Notes

- Ensure FFmpeg is accessible in your system's PATH.
- Missing camera files are marked as Missing and excluded from conversion.
- Conversion uses parallel processing, which may be resource-intensive on low-core systems.
- Output files are saved in the selected output directory.
- Input and output directories cannot be the same.


## License

The MIT License

Copyright (c) 2025 Sungsoo Kim

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


## Changelog

### v0.1.2 (2025-04-14)

- Add output directory selection and validation
- Disable directory selection during conversion
- Update UI to show both input and output directory paths
- Fix output file naming (remove .output suffix)
- Add warning message when selecting same directory for input and output

### v0.1.1 (2025-04-14)

- Rename project.
- Add output directory.
- Add MIT License.
- Add Changelog.


### v0.1.0 (2025-04-13)

- Initial commit.


## Contributing

Contributions are welcome! Please submit issues or pull requests to the repository.


## Contact

For questions or support, contact the project maintainer via GitHub issues.
