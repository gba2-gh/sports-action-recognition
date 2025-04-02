import xml.etree.ElementTree as ET
import os
import cv2
import shutil


myTree = ET.parse('C:\\Users\\gzaz976\\Documents\\datasets\\rugby\\annotations.xml')
imageDataset = 'C:\\Users\\gzaz976\\Documents\\datasets\\rugby\\images\\default'
myroot = myTree.getroot()


#sets filename with correct id to save next frame in the correct sequence
def getNextFrameNumber(directory, base_name="frame", extension=".png"):
    i = 0
    while os.path.exists(os.path.join(directory, f"{base_name}_{i}{extension}")):
        i += 1
    return f"{base_name}_{i}{extension}"

#creates the correct sewquence of 6 digits 000000 to read dataset's frames
def readDatasetFrameName(current_frame):
    digits = [int(digit) for digit in str(current_frame)]
    while(len(digits) < 6):
        digits.insert(0, 0)
    number_str = ''.join(map(str, digits))
    return os.path.join(imageDataset, f'frame_{number_str}.PNG')


##Extract frames per action in the correct player and action foldor
def getBoxActions(box, player_id, base_path):
    for attribute in box.iter('attribute'):
        if(attribute.text == 'true'):
            actionName = attribute.get('name')
            if(not(actionName.startswith('State')) and actionName != 'Stationary' and   actionName != 'Has ball' and actionName != 'In Motion' ): #
                newpath = os.path.join(base_path, actionName, player_id) 
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
                current_frame= box.get('frame')
                frame = cv2.imread(readDatasetFrameName(current_frame))
                cropped_frame = frame[int(float(box.get('ytl'))):int(float(box.get('ybr'))), int(float(box.get('xtl'))):int(float(box.get('xbr')))]
                cv2.imwrite(os.path.join(newpath, getNextFrameNumber(newpath)), cropped_frame)


# Count number of directories
def countFolders(dir):
    return sum(os.path.isdir(os.path.join(dir, item)) for item in os.listdir(dir))      

def countFoldersIn(directory):
    totalFolder = 0       
    subdirectories = [os.path.join(directory, d) for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))] #get all subdir = actions
    for subdir in subdirectories:
        folder_count = countFolders(subdir)
        totalFolder += folder_count
        print(f"Number of folders in '{subdir}': {folder_count}")
    return totalFolder
    
       
# MAIN
output_path = r'C:\\Users\\gzaz976\\Documents\\datasets\\ActionDataset\\Netball'
#output_path = r'C:\\Users\\gzaz976\\Documents\\datasets\\ActionDataset\\Netball'

### frame extraction
if( os.path.exists(output_path)):
    shutil.rmtree(output_path)

for track in myroot.iter('track'): # video
    player_id = track.get('task_id') + '_' + track.get('id')
    print(player_id)
    for box in track.iter('box'): #each individual box of the video, per frame
        if (box.get('outside')=='1') or (box.get('occluded')=='1'):
            continue
        getBoxActions(box, player_id, output_path)

###count folders
print("Total Actions:", countFoldersIn(output_path))


