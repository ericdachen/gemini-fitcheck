import cv2
import mediapipe as mp
import os
import requests
import json
from sample.fitnessAI.api.s3.s3 import create_presigned_url

part_groups = {
    'nose': [0],
    'eyes': [1, 2, 3, 4, 5, 6],
    'ears': [7, 8],
    'shoulders': [11, 12],
    'elbows': [13, 14],
    'wrists': [15, 16],
    'hips': [23, 24],
    'knees': [25, 26],
    'ankles': [27, 28],
    'feet': [29, 30, 31, 32]
}

class VideoDrawer:
        
    def __init__(self, video_full_path, output_folder_path, file_name) -> None:
        
        self.output_count = 0
        self.base = output_folder_path
        self.file_name = file_name
        self.video_path = video_full_path
        self.output_path = os.path.join(self.base, f'{file_name}_annotated_video_{self.output_count}.mp4')
        self.output_filename = f'{self.file_name}/annotated_video_{self.output_count}.mp4'

        # Setup MediaPipe Pose
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(static_image_mode=False, model_complexity=2, enable_segmentation=True)
        self.mp_drawing = mp.solutions.drawing_utils

        # Load video

        self.video = ... # to be set
        self.frame_width = ... # to be set
        self.frame_height = ... # to be set
        self.fps = ... # to be set

        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.out = ... # to be set
        
    
    def _set_video(self):
        self.video = cv2.VideoCapture(self.video_path)
        if not self.video.isOpened():
            print("Error: Could not open video.")
        
        self.frame_width = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = self.video.get(cv2.CAP_PROP_FPS)
        self.out = cv2.VideoWriter(self.output_path, self.fourcc, self.fps, (self.frame_width, self.frame_height))


    def draw_landmarks_and_connections_with_colour(self, frame, landmarks, original_to_filtered_index):
        part_colors = {
            'nose': (255, 0, 0),       # Red in RGB for nose
            'eyes': (0, 255, 0),       # Green in RGB for eyes
            'ears': (0, 0, 255),       # Blue in RGB for ears
            'shoulders': (255, 255, 0),# Yellow in RGB for shoulders
            'elbows': (255, 0, 255),   # Purple in RGB for elbows
            'wrists': (255, 165, 0),   # Orange in RGB for wrists
            'hips': (255, 20, 147),    # Pink in RGB for hips
            'knees': (0, 255, 255),    # Cyan in RGB for knees
            'ankles': (255, 0, 255)    # Magenta in RGB for ankles
        }

        # Define connections based on typical human body skeleton
        connections = [
            # Connections within each part
            (0, 1), (1, 2), (2, 3), (3, 4), (0, 4), # Head to eyes
            (0, 5), (0, 6), # Nose to ears
            (5, 11), (6, 12), # Ears to shoulders
            (11, 12), (11, 13), (13, 15), (12, 14), (14, 16), # Upper body
            (11, 23), (12, 24), (23, 24), # Torso
            (23, 25), (25, 27), (24, 26), (26, 28), # Legs
            (28, 32), (32, 30), (30, 28), (27, 29), (29, 31), (31, 27), # Foot
        ]

        # Loop through connections to draw lines
        if landmarks:
            for id, landmark in enumerate(landmarks):
                part_group = next((key for key, indices in part_groups.items() if id in indices), 'default')
                color = part_colors.get(part_group, (245, 117, 66))  # Get color based on the part group
                cv2.circle(frame, (int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0])), 4, color, -1)  # Draw the landmark
            for start_index, end_index in connections:
                # Translate original indices to filtered indices
                filtered_start_index = original_to_filtered_index.get(start_index)
                filtered_end_index = original_to_filtered_index.get(end_index)

                if filtered_start_index is not None and filtered_end_index is not None:
                    start_landmark = landmarks[filtered_start_index]
                    end_landmark = landmarks[filtered_end_index]

                    # Determine color based on the part group of the starting landmark
                    start_part_group = next((key for key, indices in part_groups.items() if start_index in indices), 'default')
                    line_color = part_colors.get(start_part_group, (245, 117, 66))  # Default color

                    # Draw line
                    cv2.line(frame,
                            (int(start_landmark.x * frame.shape[1]), int(start_landmark.y * frame.shape[0])),
                            (int(end_landmark.x * frame.shape[1]), int(end_landmark.y * frame.shape[0])),
                            line_color, 2)  # Use specific color for the line
        
        # Loop through all landmarks to draw circles


    def draw_landmarks_and_connections(self, frame, landmarks, original_to_filtered_index, severity_index):

        # Define connections based on typical human body skeleton
        connections = [
            # Connections within each part
            (0, 1), (1, 2), (2, 3), (3, 4), (0, 4), # Head to eyes
            (0, 5), (0, 6), # Nose to ears
            (5, 11), (6, 12), # Ears to shoulders
            (11, 12), (11, 13), (13, 15), (12, 14), (14, 16), # Upper body
            (11, 23), (12, 24), (23, 24), # Torso
            (23, 25), (25, 27), (24, 26), (26, 28), # Legs
            (28, 32), (32, 30), (30, 28), (27, 29), (29, 31), (31, 27), # Foot
        ]

        colour_index = {
            0:  (0, 255, 0),
            1: (0, 230, 255),
            2: (0, 110, 255),
            3: (0, 0, 255),
        }
        main_colour = colour_index[severity_index]

        # Loop through connections to draw lines
        if landmarks:
            for id, landmark in enumerate(landmarks):
                color = main_colour
                cv2.circle(frame, (int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0])), 6, color, -1)  # Draw the landmark
            for start_index, end_index in connections:
                # Translate original indices to filtered indices
                filtered_start_index = original_to_filtered_index.get(start_index)
                filtered_end_index = original_to_filtered_index.get(end_index)

                if filtered_start_index is not None and filtered_end_index is not None:
                    start_landmark = landmarks[filtered_start_index]
                    end_landmark = landmarks[filtered_end_index]
                    line_color = main_colour 

                    # Draw line
                    cv2.line(frame,
                            (int(start_landmark.x * frame.shape[1]), int(start_landmark.y * frame.shape[0])),
                            (int(end_landmark.x * frame.shape[1]), int(end_landmark.y * frame.shape[0])),
                            line_color, 4)  # Use specific color for the line
        
        # Loop through all landmarks to draw circles

    def _severity_test(self, value: int):
        """Returns 0 (not severe), 1 (somewhat severe), 2 (severe), 4(very sever)
        """
        lst = [[0, 1, 2, 5], [4, 5, 6], [7, 8], [9, 10]]
        for i in range(len(lst)):
            if value in lst[i]:
                return i
        return 0

    def draw_loop(self, start_time_tuple, end_time_tuple, part_list, severity):
        self._set_video()
        start_frame = int((60*start_time_tuple[0]+start_time_tuple[1]) * self.fps)
        end_frame = int((60*end_time_tuple[0]+end_time_tuple[1]) * self.fps)
        frame_count = 0
        part_indices = sum([part_groups[part] for part in part_list],[])
        severity_index = self._severity_test(severity)
        # print(part_indices)
        while self.video.isOpened():
            
            print(frame_count)
            ret, frame = self.video.read()
            if not ret:
                print("No more frames to read or error reading a frame.")
                
                break
            
            if frame_count >= start_frame and frame_count <= end_frame:
                # Process frame
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = self.pose.process(frame_rgb)
                
                
                if results.pose_landmarks:
                    # Filter the landmark
                    original_to_filtered_index = {i: idx for idx, i in enumerate(part_indices) if i < len(results.pose_landmarks.landmark)}
                    filtered_landmarks = [results.pose_landmarks.landmark[i] for i in part_indices if i < len(results.pose_landmarks.landmark)]

                    # self.draw_landmarks(frame, filtered_landmarks)
                    self.draw_landmarks_and_connections(frame, filtered_landmarks, original_to_filtered_index, severity_index=severity_index)

                # Write the frame into the file 'output_video.mp4'
                self.out.write(frame)
            
            frame_count+=1
            if frame_count > end_frame:
                break

        # Release everything if job is finished
        self.video.release()
        self.out.release()

        presigned_response = self.get_presigned_s3(self.output_filename)
        upload_response = self.upload_file_to_s3(presigned_response, self.video_path)
        get_presigned_url = create_presigned_url(json.loads(presigned_response.text)['fields']['key'])


        self.output_count += 1
        self.output_path = os.path.join(self.base, f'annotated_video_{self.output_count}.mp4')
        self.output_filename = f'{self.file_name}/annotated_video_{self.output_count}.mp4'

        

        print("Video processing complete. Video saved to:", self.output_path)
        return get_presigned_url
    
    def get_presigned_s3(self, file_name):
        url = f'http://127.0.0.1:8000/upload-url'
        response = requests.post(url=url, data={'file_name': file_name})
        return response
    
    def upload_file_to_s3(aelf, response, file_path):
        dct = json.loads(response.text)
        with open(file_path, 'rb') as f: # rb data open allows easier transfer
            files = {'file': (os.path.basename(file_path), f)}
            response = requests.post(dct['url'], data=dct['fields'], files=files)
            return response.status_code, response.content

if __name__ == "__main__":
    file_dir = os.path.dirname(__file__) # Base would be gemini-fitcheck
    output_path = os.path.join(file_dir, '..', '..', 'content', 'parsed_outputs', 'draw_test')
    video_path = os.path.join(file_dir, '..', '..', 'content', 'videos', '2024.04.11_GYM_ERIC.mp4')
    video_drawer = VideoDrawer(
        video_full_path=video_path,
        output_folder_path=output_path
    )
    video_drawer.draw_loop(
        start_time_tuple=(0,30),
        end_time_tuple=(0,45)
    )

