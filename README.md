How to submit the assessment -
- Fork this repository and complete the following tasks.


# Video-Processing

The goal of this project is to develop a video segmentation tool that can take a long video as input and generate smaller clips based on specified filters or criteria. The tool should leverage computer vision and audio analysis techniques to identify relevant segments within the video.

## Task Overview

You are tasked with designing and implementing a video segmentation pipeline that includes the following components:

1.  **Video Processing**:
   - Integrate a video processing library (e.g., OpenCV, FFmpeg) to handle video decoding, frame extraction, and other video manipulation tasks.
   - Implement functionality to read input video streams, extract individual frames, and prepare data for further analysis.

2. **Shot Boundary Detection**:
   - Develop algorithms or techniques to detect transitions between shots or scenes in the video, such as comparing histogram differences or edge changes between consecutive frames.
   - Implement shot boundary detection to identify potential points in the video where a new clip could begin or end.

## Requirements

- Proficiency in Python programming language and familiarity with computer vision and machine learning libraries (e.g., OpenCV, TensorFlow, PyTorch).
- Experience with video processing techniques and libraries.
- Knowledge of object detection, scene recognition, and other relevant computer vision tasks.
# Video Shot Boundary Detection

## Overview

The Video Shot Boundary Detection script is a Python program designed to analyze a video file and detect shot boundaries based on differences in frame intensity. It utilizes the OpenCV library for video processing tasks.

## Usage

To use the script, follow the steps below:

1. Run main.py (You can adjust the path to the video file by editing this script)

2. Upon execution, the script will analyze the input video, detect shot boundaries, optimize the detected boundaries, and save the clips to the output folder.

## Dependencies

- Python 3.x
- OpenCV (cv2)
- NumPy (np)

## Functionality

The Video Shot Boundary Detection script performs the following steps:

1. Opens the input video file using OpenCV's `VideoCapture` object.

2. Converts each frame of the video to the LUV color space using the `convert_to_luv()` function.

3. Calculates the mean frame difference between consecutive frames using the `calculate_mean_frame_difference()` function.

4. Stores the frame difference values along with frame IDs in a list.

5. Detects possible shot boundaries based on sudden changes in intensity using the `find_possible_frame()` method of the `Frame` class.

6. Optimizes the detected shot boundaries using the `optimize_frame()` method of the `Frame` class.

7. Uses the boundaries list with OpenCV's `VideoCapture` object to generate the shortenend clips which is saved within the ouput folder


## Resources

- OpenCV documentation: https://docs.opencv.org/
- TensorFlow Object Detection API: https://github.com/tensorflow/models/tree/master/research/object_detection
- PyTorch documentation: https://pytorch.org/docs/stable/index.html
