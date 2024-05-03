import cv2
import os
import shutil
import requests
import tempfile
from imageio.v2 import imwrite
from io import BytesIO
from sample.fitnessAI.api.s3.s3 import s3_client, create_presigned_url, S3_BUCKET

FRAME_PREFIX = "_frame"
CURR_DIR = os.path.dirname(__file__)

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

    def __init__(self, presigned_get_url, key: str) -> None:
        self.file_content = self._download_s3_file(presigned_get_url=presigned_get_url)
        if self.file_content.status == 200:
            self.file_content = self.file_content.content
            
        
        # Download to temp
        self.file_path = file_path
        self.file_name = os.path.basename(file_path).split('.mp4')[0] #split subject to change
        self.target_folder = target_folder
        
        self.output_folder = self._create_temp_storage()
        self.frame_list = []

        self._update_naming()
        self._extract_frames()

    def _upload_frame_to_s3(self, frame, key):
        # Encode frame to JPEG format
        success, buffer = cv2.imencode('.jpg', frame)
        if not success:
            raise ValueError("Could not encode frame to JPEG")

        # Create a byte stream from the buffer
        io_buf = BytesIO(buffer)

        # Upload the byte stream to S3
        s3_client.upload_fileobj(io_buf, S3_BUCKET, key)
        
        print(f"Uploaded frame to s3://{S3_BUCKET}/{key}")
        presigned_get_url = create_presigned_url(key)
        if presigned_get_url.status == 200:
            return presigned_get_url
        else:
            return presigned_get_url.status_code

    def _download_s3_file(self, presigned_get_url):
        response = requests.get(presigned_get_url)
        return response

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
        with tempfile.NamedTemporaryFile(delete=True, suffix='.mp4') as temp_video:
            temp_video.write(self.file_content)
            temp_video.flush()

            vidcap = cv2.VideoCapture(temp_video.name)
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
                    time_string_output = f"{min:02d}:{sec:02d}"
                    image_name = f"{self.file_name}{FRAME_PREFIX}{time_string}.png"
                    output_filename = os.path.join(self.output_folder, image_name)
                    
                    # Required for colour correction because normally CV2 is BGR
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                    presigned_get_url = self._upload_frame_to_s3(
                        frame=frame,
                        key=f'{image_name}/{time_string}'
                    )

                    output = [f'{time_string_output}', presigned_get_url.text]
                    

                
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
    
    