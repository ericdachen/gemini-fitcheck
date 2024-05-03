import cv2
import os
import shutil
from imageio.v2 import imwrite

FRAME_PREFIX = "_frame"


class videoFraming:
    """Class to store video as frames.

    Default frame chunking is at 1 frame per second of video.
    Ie. 30 sec video will create 30 frames. 
    
    ----- Variables -----

    file_path: Entire path of the file
    target_folder: Entire path of desired location of final frames
    file_name: Extracted file_name from file_path
    
    output_folder: Saved folder location of frames
    frame_list: List of frame file names    
    """

    file_path: str
    target_folder: str
    file_name: str
    
    output_folder: str
    frame_list: list

    def __init__(self, file_path, target_folder) -> None:
        self.file_path = file_path
        self.file_name = os.path.basename(file_path).split('.mp4')[0] #split subject to change
        self.target_folder = target_folder
        
        self.output_folder = self._create_temp_storage()
        self.frame_list = []

        self._update_naming()
        self._extract_frames()

    def _update_naming(self) -> None:
        if '.' in self.file_name:
            self.file_name = self.file_name.replace('.', '_')

    def _create_temp_storage(self) -> str:
        output_dir = os.path.join(self.target_folder, self.file_name)
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        else: 
            shutil.rmtree(output_dir)
            os.makedirs(output_dir)

        return output_dir

    def _extract_frames(self) -> None:

        vidcap = cv2.VideoCapture(self.file_path)
        fps = vidcap.get(cv2.CAP_PROP_FPS)

        frame_count = 0
        count = 0
        while vidcap.isOpened():
            success, frame = vidcap.read()
            if not success: # End of video
                break
            if int(count / fps) == frame_count: # Extract a frame every second
                min = frame_count // 60
                sec = frame_count % 60
                time_string = f"{min:02d}-{sec:02d}"
                image_name = f"{self.file_name}{FRAME_PREFIX}{time_string}.png"
                output_filename = os.path.join(self.output_folder, image_name)
                
                # Required for colour correction because normally CV2 is BGR
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
                imwrite(output_filename, frame)
            
                frame_count += 1
            count += 1
            
        vidcap.release() # Release the capture object
        
        # Ideally, it is logged
        print(f"Completed video frame extraction!\n\nExtracted: {frame_count} frames")

    def _get_frame_list(self) -> None:
        files = os.listdir(self.output_folder)

        for file in files:
            self.frame_list.append(
                File(
                    file_path=os.path.join(self.output_folder, file)
                )
            )


class File:
    """
    file_path: exact location including file type .png
    display_name: name of file including the suffix
    """
    def __init__(self, file_path: str, display_name: str = None):
        self.file_path = file_path
        self.timestamp = self.get_timestamp(file_path)
        if display_name:
            self.display_name = display_name

    def set_file_response(self, response):
        self.response = response

    def get_timestamp(self, filename):
        """Extracts the frame count (as an integer) from a filename with the format
            'output_frame00-00.png'.
        """
        parts = filename.split(FRAME_PREFIX)
        if len(parts) != 2:
            return None  # Indicates the filename might be incorrectly formatted
        else:
            minutes, seconds = parts[1].split('.')[0].split('-')
        return ':'.join([minutes, seconds])
    
# if __name__ == '__main__':
#     videoPath = path.join(__dirname, '..', '..', 'content', 'videos', '2024.04.11_GYM_ADAM.mp4')
#     outputPath = path.join(__dirname, '..', '..', 'content', 'parsed_outputs')
#     videoProcessor = new VideoFraming(
#         filePath=`${videoPath}`,
#         targetFolder=`${outputPath}`
#     )
#     files = videoProcessor.getFrameList()
    
    