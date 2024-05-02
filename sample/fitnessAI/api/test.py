# from sample.fitnessAI.api.helper import geminiAccess, videoDrawer, videoFraming

import re
import os
from sample.fitnessAI.api.helper.videoDrawer import VideoDrawer
from sample.fitnessAI.api.helper.nlp import map_body_parts


# NOSE = 'nose'
# EYES = 'eyes'
# EARS = 'ears'
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


# Skipping previous parsing

model_output_sample = """
## Cable Crossover Form Analysis

The exercise being performed is a **cable crossover**, targeting the chest muscles.

**Here's a breakdown of the form issues:**

* **0:03** - The individual is using momentum to swing the weights up, which can reduce the effectiveness of the exercise and increase the risk of injury. (Severity: 5/10) (Body parts: None)
* **0:06** - He is leaning back too far, which can put stress on the lower back. He should maintain a more upright posture with a slight bend at the hips. (Severity: 6/10) (Body parts: lower back, hips)
* **0:13** - He is not controlling the weight on the eccentric (lowering) portion of the movement, allowing the weights to pull him forward. This reduces the time under tension for the chest muscles. (Severity: 4/10) (Body parts: chest)
* **0:21** - He is bringing the handles too far down, past his torso, which can shift the focus away from the chest muscles and onto the shoulders. The handles should ideally come together around chest level. (Severity: 10/10) (Body parts: torso, chest, shoulders)

**Overall:**

The individual's form has some issues that need to be addressed to maximize the effectiveness of the exercise and minimize the risk of injury. The use of momentum, excessive leaning back, lack of control during the eccentric phase, and overextension at the bottom of the movement are the main concerns.

**Recommendations:**

* **Focus on using a slow and controlled movement:** Avoid using momentum to swing the weights. Concentrate on the mind-muscle connection and feel the chest muscles working throughout the entire movement.
* **Maintain a proper posture:** Keep the core engaged and avoid leaning back excessively. A slight bend at the hips is acceptable, but the torso should remain relatively upright.
* **Control the eccentric phase:** Resist the weight as you lower it back to the starting position. This will help to maximize muscle engagement and growth.
* **Bring the handles together at chest level:** Avoid overextending at the bottom of the movement. Focus on squeezing the chest muscles at the top of the movement and maintaining tension throughout. 
* **Consider reducing the weight:**  Focus on proper form with a lighter weight before increasing the load.

**By focusing on proper form and technique, the individual can improve the effectiveness of the cable crossover exercise and reduce the risk of injury.** 
"""

# issues = re.findall(r'\*\*([0-9]{1,2}:[0-9]{2})\*\* - .*?\(Severity: \b(10|[0-9])\b/10\) .*?\(Body parts: ([\w\s,]+)\)',model_output_sample)
"""
Index
- 0 == timestamp
- 1 == severity of issue
- 2 == 

Notes
- [0-9] says any number betwee 0 to 9
- '-' is needed as it is stylistic '**0:42** -'
- '.' = represents any characters except new line
- '*' repeated any number of times
- '?' but make it as few amount of times as possible of repeat character representations
- '.*?' should not have a space after. Used a a block to capture characters between
- '()' are what is captured in the final result
- '[\w\s,]' -- \w (matches 1 or more words) -- \s (whitespace) -- , (and commas)
"""

# Take 5 seconds out from the clip

def end_time_check(min: int, sec: int, addition_sec: int) -> tuple:
    if sec + addition_sec > 60:
        return (min+1, (sec+addition_sec) - 60)
    else:
        return (min, sec+addition_sec)

def conduct_drawing(issues_list, drawer: VideoDrawer):

    for issue in issues_list:

        set_1 = issue
        min, sec = list(map(int, set_1[0].split(':')))
        start_time = (min, sec)
        end_time = end_time_check(min, sec, addition_sec=5)
        print(start_time, end_time)
        severity = int(set_1[1])
        body_list = set_1[2].split(', ')

        output_bodyparts = map_body_parts(input_parts=body_list, body_parts_dict=body_parts)
        if 'chest' in body_list:
            final_output = sum([body_parts[part] for part in output_bodyparts], [])
            final_output.extend(body_parts['chest'])
        else:
            final_output = sum([body_parts[part] for part in output_bodyparts], [])
        adj_final_output = final_output if final_output else ALL

        drawer.draw_loop(
            start_time_tuple=start_time,
            end_time_tuple=end_time,
            part_list=list(set(adj_final_output)),
            severity=severity
        )

if __name__ == "__main__":

    video_drawer = VideoDrawer(
        video_full_path=os.path.join(
            os.path.dirname(__file__), 
            '..', 
            'content', 
            'videos', 
            '2024.04.11_GYM_ERIC.mp4'
        ),
        output_folder_path=os.path.join(
            os.path.dirname(__file__), 
            '..', 
            'content', 
            'parsed_outputs', 
            'draw_test'
        )
    )
    issues = re.findall(r'\*\*([0-9]{1,2}:[0-9]{2})\*\* - .*?\(Severity: \b(10|[0-9])\b/10\) .*?\(Body parts: ([\w\s,]+)\)',model_output_sample)
    conduct_drawing(
        issues_list=issues,
        drawer=video_drawer
    )