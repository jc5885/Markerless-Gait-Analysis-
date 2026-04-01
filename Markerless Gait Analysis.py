import mediapipe as mp
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

# Load data from CSV file
file_path = "/Users/jade/Downloads/marklerless/Lukas 01 Redo.csv"
LC_01_redo = pd.read_csv(file_path, skiprows=2)

# Print out column names to check if they match your expected names
print(LC_01_redo.columns)

# Extract the relevant columns for joint angles
joint_angles_columns = ['LC:RAnkleAngles', 'LC:RHipAngles', 'LC:RKneeAngles']
joint_angles_LC_01_redo = LC_01_redo[joint_angles_columns]

# Convert the data to numeric (assuming they are strings in the CSV)
joint_angles_LC_01_redo = joint_angles_LC_01_redo.apply(pd.to_numeric, errors='coerce')

# Check if there are NaN values after conversion
print(joint_angles_LC_01_redo.isnull().sum())
# Extract the relevant columns for joint angles
joint_angles_columns = ['LC:RAnkleAngles', 'LC:RHipAngles', 'LC:RKneeAngles']
joint_angles_LC_01_redo = LC_01_redo[joint_angles_columns]

# Convert the data to numeric (assuming they are strings in the CSV)
joint_angles_LC_01_redo = joint_angles_LC_01_redo.apply(pd.to_numeric, errors='coerce')

start_index=51
end_index=161

filtered_data = joint_angles_LC_01_redo.iloc[start_index:end_index]


mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Initialize VideoCapture with the paths to your videos
cap_side = cv2.VideoCapture('/Users/jade/Downloads/marklerless/lukas_drmoon.MOV')


# set width of output video
desired_width = 800

# create empty arrays to hold joint angle data
angles_knee = []
angles_hip = []
angles_ankle = []

# play video showing landmarks, read frames
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap_side.isOpened():
        ret, frame = cap_side.read()
        if not ret:
            break

        height, width = frame.shape[:2]
        if width > desired_width:
            aspect_ratio = height / width
            new_height = int(desired_width * aspect_ratio)
            frame = cv2.resize(frame, (desired_width, new_height))

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = pose.process(image)

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark

            # defines function to calculate joint angles based on variables a, b, c
            def calculate_angle(landmark1, landmark2, landmark3,joint_type=None):
                vector1 = np.array([landmark1[0], landmark1[1]])  # Access x and y coordinates from the list
                vector2 = np.array([landmark2[0], landmark2[1]])  # Access x and y coordinates from the list
                vector3 = np.array([landmark3[0], landmark3[1]])  # Access x and y coordinates from the list
                #vector4 = np.array([landmark4[0], landmark4[1]])  # Access x and y coordinates from the list
                if joint_type == 'ankle':
                   
                # Calculate vectors from landmarks
                    v1 = vector2 - vector1
                    v2 = vector1 - vector3
                    #dot_product = np.sum(v1*v2)
                    dot_product = np.sum(v1*v2,axis=1)
                    magnitude1 = np.linalg.norm(v1)
                    magnitude2 = np.linalg.norm(v2)
                    cosine_angle = dot_product / (magnitude1 * magnitude2)
                    angle_rad = np.arctan2(np.linalg.det([v1,v2]), np.dot(v1, v2))
                    angle_rad = np.arccos(cosine_angle)

                    angle_deg = np.degrees(angle_rad)
                    angle_deg= np.degrees(angle_rad)
                    #angle_rad_shank = np.arctan2(landmark1[1] - landmark2[1], landmark1[0] - landmark2[0])
                    #angle_deg_shank = np.degrees(angle_rad_shank)
                
                    #angle_rad_foot = np.arctan2(landmark3[1] - landmark4[1], landmark3[0] - landmark4[0])
                    #angle_deg_foot= np.degrees(angle_rad_foot)
                    #angles_ankle=  -(angle_deg_foot-angle_deg_shank)-90
                # Convert angle from radians to degrees
                    #angle_deg = np.degrees(angle_rad)
            
                    
                else:
                    v1 = vector2 - vector1
                    v2 = vector3- vector2
                # Calculate dot product
                    #dot_product = np.dot(v1, v2)

                # Calculate magnitudes
                    #magnitude1 = np.linalg.norm(v1)
                    #magnitude2 = np.linalg.norm(v2)

                # Calculate cosine of the angle
                    #cosine_angle = dot_product / (magnitude1 * magnitude2)

                # Convert cosine to angle in radians
                    #angle_rad = np.arccos(cosine_angle)
                    angle_rad = np.arctan2(np.linalg.det([v1, v2]), np.dot(v1, v2))
                    angle_deg = np.degrees(angle_rad)

                # Convert angle from radians to degrees
                #angle_deg = np.degrees(angle_rad)

                #if joint_type == 'ankle':
                    #angle_deg -= 90
               
                return angle_deg
            # Calculate dot product
                

                        # defines which marker is the hip, knee, shoulder, toe and ankle in the x and y planes
            #hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            #knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
            #ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
            #shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            #toe = [landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].y]
            #heel = [landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].y]
                                   # defines which marker is the hip, knee, shoulder, toe and ankle in the x and y planes
            hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            toe = [landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].x, landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].y]
            heel = [landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].y]
          


            # calculates knee angle in each frame as video plays
            angle_knee = calculate_angle(hip, knee, ankle)
            angles_knee.append(angle_knee)

            # calculates hip angle in each frame as video plays
            angle_hip = -calculate_angle(shoulder, hip, knee)
            angles_hip.append(angle_hip)

            # calculates ankle angle in each frame as video plays
            #angle_ankle = calculate_angle(knee, heel, toe,joint_type='ankle')
            angle_ankle = calculate_angle(ankle, knee,heel)
            angles_ankle.append(angle_ankle)

        # plays imported video, showing pose estimation
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        cv2.imshow('Mediapipe Feed', image)

        # allows user to stop video from playing by pressing q
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

# closes the video window once it finishes
cap_side.release()
cv2.destroyAllWindows()


# Placeholder start and end frames for the gait cycle
start_frame = 0  # Example start frame of the gait cycle
end_frame = 70   # Example end frame of the gait cycle


# Assuming you've identified the start and end frames correctly
# Calculate the gait cycle percentages for each frame
gait_cycle_percentages = np.linspace(0, 100, end_frame - start_frame + 1)
#normalized_x_values = np.linspace(0, 100, start_index - end_index + 1)
x_labels= np.linspace(0, 100, 20)


# PLOTTING STUFF
fig, axs = plt.subplots(3, 2, figsize=(10, 8))
plt.subplots_adjust(hspace=0.5, wspace=0.5)  # Adjust spacing between subplots
#x_values = np.linspace(0, 100, 20)





#axs[0].plot(angles_hip)
axs[0,0].plot( angles_hip[start_frame:end_frame+1],label='MediaPipe')
axs[0,0].set_xticks(range(start_frame,end_frame+1,14)) # placed at intervals of 14 
axs[0,0].set_xticklabels(range(0, 101, 20)) 
axs[0,0].set_xlabel('Gait Cycle (%)')
axs[0,0].set_ylabel('Joint Angle (degrees)')
axs[0,0].set_title('Hip Flex-Extension')
axs[0,0].text(0.98, 0.98, 'Flex', ha='right', va='top',transform=axs[0,0].transAxes)
axs[0,0].text(0.98, 0.08, 'Ext', ha='right', va='bottom',transform=axs[0,0].transAxes)

axs[0,1].plot(filtered_data['LC:RHipAngles'],label='Vicon')
axs[0,1].set_xticks(range(start_index,end_index+1,22))
axs[0,1].set_xticklabels(range(0, 101, 20)) 
axs[0,1].set_xlabel('Gait Cycle (%)')
#axs[0,1].set_ylabel('Joint Angle (degrees)')
axs[0,1].set_title('Hip Flex-Extension')
axs[0,1].text(0.98, 0.98, 'Flex', ha='right', va='top',transform=axs[0,1].transAxes)
axs[0,1].text(0.98, 0.08, 'Ext', ha='right', va='bottom',transform=axs[0,1].transAxes)

#axs[1].plot(angles_knee)
axs[1,0].plot(angles_knee[start_frame:end_frame+1],label='MediaPipe')

axs[1,0].set_xticks(range(start_frame,end_frame+1,14))
axs[1,0].set_xticklabels(range(0, 101, 20)) 
axs[1,0].set_xlabel('Gait Cycle (%)')
axs[1,0].set_ylabel('Joint Angle (degrees)')
axs[1,0].set_title('Knee Flex-Extension')
axs[1,0].text(0.98, 0.98, 'Flex', ha='right', va='top',transform=axs[1,0].transAxes)
axs[1,0].text(0.98, 0.08, 'Ext', ha='right', va='bottom',transform=axs[1,0].transAxes)

axs[1,1].plot(filtered_data['LC:RKneeAngles'],label='Vicon')
axs[1,1].set_xticks(range(start_index,end_index+1,22))
axs[1,1].set_xticklabels(range(0, 101, 20)) 
axs[1,1].set_xlabel('Gait Cycle (%)')
#axs[1,1].set_ylabel('Joint Angle (degrees)')
axs[1,1].set_title('Knee Flex-Extension')
axs[1,1].text(0.98, 0.98, 'Flex', ha='right', va='top',transform=axs[1,1].transAxes)
axs[1,1].text(0.98, 0.08, 'Ext', ha='right', va='bottom',transform=axs[1,1].transAxes)

#axs[2].plot(angles_ankle)
axs[2,0].plot(angles_ankle[start_frame:end_frame+1],label='MediaPipe')
axs[2,0].set_xticks(range(start_frame,end_frame+1,14))
axs[2,0].set_xticklabels(range(0, 101, 20)) 
axs[2,0].set_xlabel('Gait Cycle (%)')
axs[2,0].set_ylabel('Joint Angle (degrees)')
axs[2,0].set_title('Ankle Dors-Plantarflex')
axs[2,0].text(0.98, 0.98, 'Dors', ha='right', va='top',transform=axs[2,0].transAxes)
axs[2,0].text(0.98, 0.08, 'Plant', ha='right', va='bottom',transform=axs[2,0].transAxes)
#axs[2,0].set_ylim(-30, 30)

axs[2,1].plot(filtered_data['LC:RAnkleAngles'],label='Vicon')
axs[2,1].set_xticks(range(start_index,end_index+1,22))
axs[2,1].set_xticklabels(range(0, 101, 20)) 
axs[2,1].set_xlabel('Gait Cycle (%)')
#axs[2,1].set_ylabel('Joint Angle (degrees)')
axs[2,1].set_title('Ankle Dors-Plantarflex')
axs[2,1].text(0.98, 0.98, 'Dors', ha='right', va='top',transform=axs[2,1].transAxes)
axs[2,1].text(0.98, 0.08, 'Plant', ha='right', va='bottom',transform=axs[2,1].transAxes)

# Add super titles for each column


fig.text(0.2, 0.93, 'Our Approach', fontsize=16, fontweight='bold')
fig.text(0.60, 0.93, 'Conventional Approach', fontsize=16, fontweight='bold')

print(angles_ankle[start_frame:end_frame+1])


#plt.tight_layout()
#plt.legend(loc='lower left')
plt.show()
