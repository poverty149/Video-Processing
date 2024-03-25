class Frame:
    """Class to hold information about each frame"""

    def __init__(self, id, diff):
        self.id = id
        self.diff = diff

    def get_max_diff_frame(self, frames):
        """
        Find the frame with the maximum difference in a window of frames.
        """
        max_diff_frame = frames[0]
        for frame in frames[1:]:
            if frame.diff > max_diff_frame.diff:
                max_diff_frame = frame
        return max_diff_frame

    def find_possible_shot_boundaries(self, frames):
        """
        Detect possible shot boundaries based on sudden changes in intensity.
        """
        possible_boundaries = []
        window_frames = []
        window_size = 30
        sudden_change_factor = 3
        min_shot_length = 8

        index = 0
        while index < len(frames):
            window_frames.append(frames[index])

            if len(window_frames) < window_size:
                index += 1
                if index == len(frames) - 1:
                    window_frames.append(frames[index])
                continue

            # Find the frame with maximum difference in the window
            max_diff_frame = self.get_max_diff_frame(window_frames)
            max_diff_id = max_diff_frame.id

            if not possible_boundaries:
                possible_boundaries.append(max_diff_frame)
                continue

            last_boundary = possible_boundaries[-1]

            # Check if the difference of the selected frame is more than 3 times
            # the average difference of the other frames in the window
            start_id = last_boundary.id + 1
            end_id = max_diff_id - 1

            sum_diff = sum(frame.diff for frame in frames[start_id:end_id+1])
            average_diff = sum_diff / (end_id - start_id + 1)

            if max_diff_frame.diff >= sudden_change_factor * average_diff:
                possible_boundaries.append(max_diff_frame)
                window_frames = []
                index = possible_boundaries[-1].id + min_shot_length
            else:
                index = max_diff_frame.id + 1
                window_frames = []
            

        return possible_boundaries


    def optimize_shot_boundaries(self, possible_boundaries, frames):
        """
        Optimize the detected shot boundaries.
        """
        optimized_boundaries = []

        frame_count = 10
        diff_threshold = 10
        optimize_factor = 2

        for boundary in possible_boundaries:
            boundary_id = boundary.id

            # Check if the difference of the boundary is not less than 10
            if boundary.diff < diff_threshold:
                continue

            # Check if the difference is more than twice the average difference
            # of the previous and subsequent frames
            prev_frames = frames[max(0, boundary_id - frame_count):boundary_id]
            next_frames = frames[boundary_id + 1:min(len(frames), boundary_id + frame_count + 1)]

            sum_diff = sum(frame.diff for frame in prev_frames) + sum(frame.diff for frame in next_frames)
            average_diff = sum_diff / (2 * frame_count)

            if boundary.diff > optimize_factor * average_diff:
                optimized_boundaries.append(boundary)

        return optimized_boundaries
