import requests
import tempfile
import re
import cv2
# from sample.fitnessAI.api.helper.geminiAccess import geminiFitCheck
# from sample.fitnessAI.api.instructions import instruction
# from sample.fitnessAI.api.helper.videoDrawerModified import VideoDrawer
# from sample.fitnessAI.api.helper.nlp import map_body_parts

from api.helper.geminiAccess import geminiFitCheck
from api.instructions import instruction
from api.helper.videoDrawerModified import VideoDrawer
from api.helper.nlp import map_body_parts
import os
FRAME_PREFIX = "_frame"

body_parts = {
    'shoulders': ['shoulders'],
    'elbows': ['elbows'],
    'wrists': ['wrists'],
    'hips':['hips'],
    'knees': ['knees'],
    'ankles': ['ankles'], 
    'feet': ['feet'],
    'body': ['shoulders', 'hips'],
    'chest': ['shoulders', 'hips'],
    'back': ['shoulders', 'hips'],
    'legs': ['hips', 'knees', 'ankles'],
    'calves': ['knees', 'ankles'],
    'arms': ['shoulders', 'elbows', 'wrists']
}
ALL = ['shoulders', 'elbows', 'wrists', 'hips', 'knees', 'ankles', 'feet'] 


def end_time_check(min: int, sec: int, addition_sec: int) -> tuple:
    if sec + addition_sec > 60:
        return (min+1, (sec+addition_sec) - 60)
    else:
        return (min, sec+addition_sec)

def conduct_drawing(issues_list, drawer: VideoDrawer):

    output_list = []
    for issue in issues_list:

        set_1 = issue
        min, sec = list(map(int, set_1[0].split(':')))
        start_time = (min, sec)
        end_time = end_time_check(min, sec, addition_sec=5)
        print(start_time, end_time)
        severity = int(set_1[2])
        detail = set_1[1]
        body_list = set_1[3].split(', ')

        output_bodyparts = map_body_parts(input_parts=body_list, body_parts_dict=body_parts)
        if 'chest' in body_list:
            final_output = sum([body_parts[part] for part in output_bodyparts], [])
            final_output.extend(body_parts['chest'])
        else:
            final_output = sum([body_parts[part] for part in output_bodyparts], [])
        adj_final_output = final_output if final_output else ALL

        response = drawer.draw_loop(
            start_time_tuple=start_time,
            end_time_tuple=end_time,
            part_list=list(set(adj_final_output)),
            severity=severity
        )

        output_list.append((f'Severity: {severity}/10', detail, response))
    
    return output_list

def main(presigned_url_get_request, file_name):
    """file_name includes suffix ".mp4"
    """

    model = geminiFitCheck()

    download_response = requests.get(presigned_url_get_request)
    file_content = download_response.content

    final_output = []

    with tempfile.NamedTemporaryFile(delete=True, suffix='.mp4') as temp_video:
        temp_video.write(file_content)
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
                time_string = f"{min:02d}:{sec:02d}"
                save_name = f"{file_name}/{FRAME_PREFIX}{time_string}.png"
                # output_filename = os.path.join(self.output_folder, image_name)
                
                # Required for colour correction because normally CV2 is BGR
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                temp_fd, temp_path = tempfile.mkstemp(suffix='.png')
                os.close(temp_fd)
                
                cv2.imwrite(temp_path, frame)
                print(f'Uploading: {temp_path}...')
                response = model.upload_file(path=temp_path)
                output = [time_string, response]
                final_output.extend(output)
                os.unlink(temp_path)
                
                frame_count += 1
            count += 1
            
        vidcap.release() # Release the capture object
    
    print('Finished uploading files!')

    analysis = model.generate_analysis(
        prompt=instruction,
        file_timestamp_list=final_output
    ).text

    print('Model response:', analysis)

    issues = re.findall(r'\*\*([0-9]{1,2}:[0-9]{2})\*\* - (.*?)(?=\s?\(Severity: \b(10|[0-9])\b/10\)) .*?\(Body parts: ([\w\s,]+)\)',analysis)
    
    temp_fd, temp_path = tempfile.mkstemp(suffix='.mp4')
    os.close(temp_fd)
    temp_fd2, temp_path2 = tempfile.mkstemp(suffix='.mp4')
    os.close(temp_fd2)
    with open(temp_path, 'wb') as temp_file:  # Open the file in binary write mode
        temp_file.write(download_response.content) 
    video_drawer = VideoDrawer(
        video_full_path=temp_path,
        temp_output_full_path=temp_path2,
        file_name=file_name
    )
    result = conduct_drawing(
        issues_list=issues,
        drawer=video_drawer
    )
    os.unlink(temp_path)
    os.unlink(temp_path2)
    
    return result

    




    
    



