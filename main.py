import cv2
import numpy as np
from frame import Frame
import os

def convert_to_luv(frame):
    luv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2LUV)
    return luv_frame

def calculate_mean_frame_difference(prev_frame, curr_frame):
    diff_frame = cv2.absdiff(prev_frame, curr_frame)
    diff_sum = np.sum(diff_frame)
    diff_frame_mean = diff_sum / (diff_frame.shape[0] * diff_frame.shape[1])
    return diff_frame_mean

def detect_shot_boundaries(video_path):
    cap = cv2.VideoCapture(video_path)
    curr_frame = None
    prev_frame = None
    frame_diffs = []
    all_frames = []
    frame_numbers=[]
    ret, frame = cap.read()
    i = 0
    FRAME = Frame(0, 0)
    last_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    while ret:
        curr_frame = convert_to_luv(frame)

        if curr_frame is not None and prev_frame is not None:
            diff_sum_mean = calculate_mean_frame_difference(prev_frame, curr_frame)
            frame_diffs.append(diff_sum_mean)
            frame = Frame(i, diff_sum_mean)
            all_frames.append(frame)
        elif curr_frame is not None and prev_frame is None:
            diff_sum_mean = 0
            frame_diffs.append(diff_sum_mean)
            frame = Frame(i, diff_sum_mean)
            all_frames.append(frame)

        prev_frame = curr_frame
        i += 1
        ret, frame = cap.read()
    cap.release()

    frame_return = FRAME.find_possible_shot_boundaries(all_frames)

    # Optimize the possible frame
    new_frame = FRAME.optimize_shot_boundaries(frame_return, all_frames)
    for f in new_frame:
        frame_numbers.append(f.id)
    frame_numbers.append(last_frame)
    split_video(video_path, frame_numbers)

def split_video(video_path, boundaries):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    output_folder="./output"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    out = None
    shot_count = 1
    writers = {}
    for frame_number in boundaries:
        output_path = f"{output_folder}/frame_{shot_count}.mp4"
        writers[frame_number] = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        shot_count+=1
    # Read and process each frame
    frame_number = 0
    curr_frame=boundaries[0]
    cnt=0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Check if the current frame number matches any of the specified frame numbers from the boundaries list
        
        if frame_number in boundaries:
            cnt+=1
            if cnt==len(boundaries):
                break
            curr_frame=boundaries[cnt]

        ## Write all frames upto selected boundary frame into a new video clip
        writers[curr_frame].write(frame)
            
        

        frame_number += 1

    for writer in writers.values():
        writer.release()
    cap.release()
    
if __name__ == "__main__":
    video_path = "./sample.mp4"  # Update with the path to your video file
    detect_shot_boundaries(video_path)
    
