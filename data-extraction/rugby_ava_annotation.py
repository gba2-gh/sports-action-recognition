import xml.etree.ElementTree as ET
import os
import csv

def getActions(box):
    actions = []
    for attribute in box.iter('attribute'):
        if(attribute.text == 'true'):
            actionName = attribute.get('name')
            if(actionName != 'Stationary' and actionName != 'State: Stationary'): #          
                actions.append(actionName)
    return actions


myTree = ET.parse('C:\\Users\\gzaz976\\Documents\\datasets\\rugby\\annotations.xml')
myRoot = myTree.getroot()

## STRUCTURE FOR AVA DATASET
# VIDEO_ID | KEYFRAME | X1 | Y1 | X2 | Y2 | ACTION_ID | PERSON_ID

##assume all cideos have the same size
task_iterator = myRoot.iter('task') 
first_task_element = next(task_iterator) 
width = first_task_element.find('original_size/width')
width = int(width.text)
height = first_task_element.find('original_size/height')
height = int(height.text)
print(width, height)

video_fps = 24
keyframe_sampling_seconds = 1 #every 1 dsecond, get action
keyframe_sampling_frames = keyframe_sampling_seconds * video_fps

with open("output_AVA.csv", 'w', newline='', encoding = 'utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)

    for track in myRoot.iter('track'):
        #print('trackid', track.get('id'))
        VIDEO_ID = track.get('task_id')
        PERSON_ID = track.get('id')
        for i, box in enumerate(track.iter('box')):
            if (box.get('outside')=='1') or (box.get('occluded')=='1'):
                continue
            if i % keyframe_sampling_frames == 0:
                KEYFRAME = i / video_fps
                X1 = float(box.get('xtl')) / width
                Y1 = float(box.get('ytl')) / height
                X2 = float(box.get('xbr')) / width
                Y2 = float(box.get('ybr')) / height

                actions = getActions(box)

                for ACTION_ID in actions:
                    row_data = [VIDEO_ID, KEYFRAME, X1, Y1, X2, Y2, ACTION_ID, PERSON_ID]
                    csvwriter.writerow(row_data)
            
            #amtFrames = box.get('frame') #TODO: separate total frames per video so videos get clipped every 3 frames, but counting from the start of their clip
