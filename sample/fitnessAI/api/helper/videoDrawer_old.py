import cv2
import mediapipe as mp
import os

part_groups = {
    'nose': [0],
    'eyes': [1, 2, 3, 4, 5, 6],
    'ears': [7, 8],
    'shoulders': [11, 12],
    'elbows': [13, 14],
    'wrists': [15, 16],
    'hips': [23, 24],
    'knees': [25, 26],
    'ankles': [27, 28]
}

class VideoDrawer:
        
    def __init__(self, video_full_path, output_folder_path) -> None:
        
        self.output_count = 0
        self.output_path = os.path.join(output_folder_path, f'annotated_video_{self.output_count}.mp4')

        # Setup MediaPipe Pose
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(static_image_mode=False, model_complexity=2, enable_segmentation=True)
        self.mp_drawing = mp.solutions.drawing_utils

        # Load video

        self.video = cv2.VideoCapture(video_full_path)
        frame_width = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = self.video.get(cv2.CAP_PROP_FPS)

        if not self.video.isOpened():
            print("Error: Could not open video.")

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.out = cv2.VideoWriter(self.output_path, fourcc, self.fps, (frame_width, frame_height))
    

    def draw_landmarks_and_connections(self, frame, landmarks):
        part_colors = {
            'nose': (0, 0, 255),       # Red in BGR for nose
            'eyes': (0, 255, 0),       # Green in BGR for eyes
            'ears': (255, 0, 0),       # Blue in BGR for ears
            'shoulders': (0, 255, 255),# Yellow in BGR for shoulders
            'elbows': (255, 0, 255),   # Purple in BGR for elbows
            'wrists': (0, 165, 255),   # Orange in BGR for wrists
            'hips': (147, 20, 255),    # Pink in BGR for hips
            'knees': (255, 255, 0),    # Cyan in BGR for knees
            'ankles': (255, 0, 255)    # Magenta in BGR for ankles
        }

        # Define connections based on typical human body skeleton
        connections = [
            # Connections within each part
            (0, 1), (1, 2), (2, 3), (3, 4), (0, 4), # Head to eyes
            (0, 5), (0, 6), # Nose to ears
            (5, 11), (6, 12), # Ears to shoulders
            (11, 12), (11, 13), (13, 15), (12, 14), (14, 16), # Upper body
            (11, 23), (12, 24), (23, 24), # Torso
            (23, 25), (25, 27), (24, 26), (26, 28) # Legs
        ]

        # Loop through connections to draw lines
        if landmarks:
            for start_index, end_index in connections:
                if start_index < len(landmarks) and end_index < len(landmarks):
                    start_landmark = landmarks[start_index]
                    end_landmark = landmarks[end_index]

                    # Determine color based on the part group of the starting landmark
                    start_part_group = next((key for key, indices in part_groups.items() if start_index in indices), 'default')
                    line_color = part_colors.get(start_part_group, (245, 117, 66))  # Default color

                    # Draw line
                    cv2.line(frame,
                            (int(start_landmark.x * frame.shape[1]), int(start_landmark.y * frame.shape[0])),
                            (int(end_landmark.x * frame.shape[1]), int(end_landmark.y * frame.shape[0])),
                            line_color, 2)  # Use specific color for the line

        # Loop through all landmarks to draw circles
        for id, landmark in enumerate(landmarks):
            part_group = next((key for key, indices in part_groups.items() if id in indices), 'default')
            color = part_colors.get(part_group, (245, 117, 66))  # Get color based on the part group
            cv2.circle(frame, (int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0])), 4, color, -1)  # Draw the landmark



    # def draw_landmarks(self, frame, landmarks):
    #     # Define colors for different body parts
    #     # part_colors = {
    #     #     'nose': (255, 0, 0),       # Red
    #     #     'eyes': (0, 255, 0),       # Green
    #     #     'ears': (0, 0, 255),       # Blue
    #     #     'shoulders': (255, 255, 0),# Yellow
    #     #     'elbows': (128, 0, 128),   # Purple
    #     #     'wrists': (255, 165, 0),   # Orange
    #     #     'hips': (255, 20, 147),    # Pink
    #     #     'knees': (0, 255, 255),    # Cyan
    #     #     'ankles': (255, 0, 255)    # Magenta
    #     # }

    #     part_colors = {
    #         'nose': (0, 0, 255),       # Red in BGR
    #         'eyes': (0, 255, 0),       # Green in BGR
    #         'ears': (255, 0, 0),       # Blue in BGR
    #         'shoulders': (0, 255, 255),# Yellow in BGR (red and green)
    #         'elbows': (255, 0, 255),   # Purple in BGR (blue and red)
    #         'wrists': (0, 165, 255),   # Orange in BGR (some green and full red)
    #         'hips': (147, 20, 255),    # Pink in BGR
    #         'knees': (255, 255, 0),    # Cyan in BGR (blue and green)
    #         'ankles': (255, 0, 255)    # Magenta in BGR (blue and red)
    #     }

    #     # Define groups of landmarks

    #     # if landmarks and len(landmarks.landmark) > 1:
    #     #     # Example: Draw a line between the first and second landmark with an explicit color
    #     #     pt1 = (int(landmarks.landmark[0].x * frame.shape[1]), int(landmarks.landmark[0].y * frame.shape[0]))
    #     #     pt2 = (int(landmarks.landmark[1].x * frame.shape[1]), int(landmarks.landmark[1].y * frame.shape[0]))
    #     #     cv2.line(frame, pt1, pt2, (0, 0, 255), 3)  # Explicitly setting to blue in BGR

    #     # Loop through all landmarks and draw them
    #     if landmarks:
    #         for id, landmark in enumerate(landmarks.landmark):
    #             # Identify which group this landmark belongs to
    #             part_group = 'default'
    #             name_part_group = None
    #             for key, indices in part_groups.items():
    #                 if id in indices:
    #                     # print('HERE:', key)
    #                     part_group = key
    #                     break
    #             # print(part_group)
    #             # Determine the color and size for the landmark
    #             color = part_colors.get(part_group, (245, 117, 66))
    #             print(color)
    #             connection_color = color
    #             circle_radius = 4 if part_group in ['nose', 'eyes', 'ears'] else 2
    #             self.mp_drawing.draw_landmarks(
    #                 frame, landmarks, self.mp_pose.POSE_CONNECTIONS,
    #                 self.mp_drawing.DrawingSpec(color=color, thickness=2, circle_radius=circle_radius),
    #                 self.mp_drawing.DrawingSpec(color=connection_color, thickness=2, circle_radius=2)
    #             )

    # Example of how to call this method
    # Assuming 'frame' is your current video frame and 'results.pose_landmarks' is the output from MediaPipe
    # self.draw_landmarks(frame, results.pose_landmarks)

    # [OLD] Draw connections
    # self.mp_drawing.draw_landmarks(
    #     frame, landmarks, self.mp_pose.POSE_CONNECTIONS,
    #     self.mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2),
    #     self.mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
    # )

    def draw_loop(self, start_time_tuple, end_time_tuple, part):
        start_frame = int((60*start_time_tuple[0]+start_time_tuple[1]) * self.fps)
        end_frame = int((60*end_time_tuple[0]+end_time_tuple[1]) * self.fps)
        frame_count = 0
        part_indices = part_groups[part]
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
                    filtered_landmarks = [
                        results.pose_landmarks.landmark[i] for i in part_indices 
                        if i < len(results.pose_landmarks.landmark)
                    ]

                    # self.draw_landmarks(frame, filtered_landmarks)
                    self.draw_landmarks_and_connections(frame, filtered_landmarks)

                # Write the frame into the file 'output_video.mp4'
                self.out.write(frame)
            
            frame_count+=1
            if frame_count > end_frame:
                break

        # Release everything if job is finished
        self.video.release()
        self.out.release()
        self.output_count += 1
        print("Video processing complete. Video saved to:", self.output_path)

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

