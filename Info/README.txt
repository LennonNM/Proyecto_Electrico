#**************************************************
#
#Teleoperation System for a NAO humanoid robot 
#with data collected from a Motion Capture System
##
#Lennon Nunez Meono
#CORE, PRIS-Lab, University of Costa Rica
##
#
#**************************************************
#
#Version: 1
#--------------------------------------------------
#Read full text for a detailed explanation on the
#development of the first release of the
#Teleoperation System.
##
#Requirements:
### OS: Linux
### Commands on Teminal
### Python v2.7
### Python Module "numpy" for polinomial regression
### Nao humanoid robot (body type H25 used for the 
###     development of the syste)
### MoCap system with plenty of space for performing
###     the data collection routines
###     - 8 cameras
###     - Special suit
###     - At least 6 markers (prefered 27)
### Motive software installed on a PC
###     Hardware licences required
##
#Use:
### The system is divided in two main processes.
### The first one consists of the Calibration of 
### the system for a single operator. The second
### one is of the actual excecution of the tele-
### -operation of the humanoid robot NAO with
### the data of a recorded optical motion capture.
##
### The initial suposition is that the all of
### the requirements are met prior to the use
### of the system and that the set up of the 
### MoCap recording environment is done 
### properly. This includes the placement of the
### markers and the creation of the Rigid Bodies 
### needed for each respective NAO's chain 
### effectors (RArm, RLeg, LLeg, LArm, Head and
### Torso).
##
##
### Calibration:
##
#### If there is no NAO calibration data on the
#### directory .../Code/Ver_Release/Calibration/
#### NAO/RigidBody_Default/, or it is needed to
#### obtain new data, perform the follwing steps.
#### If there is calibration data for the NAO,
#### skip the steps to 'Person Calibration'.
#### - Run each routine via Choregraphe suit on
#### the     directory    .../Code/Ver_Release/
#### Calibration/Routines.
#### - For each routine run the script
#### GetPositions.py with the needed parameters
#### on the right order: robot IP, Reference 
#### Frame, Include Rotation, File Name.
#### -- The file is created on the directory
####    .../Code/Ver_Release/Calibration/NAO
####    GetPositions_Generated.
#### -- If File Name is not included it will
####     be automatically generated with date-time.
#### -- The new routines data are to be placed
####     on .../Code/Ver_Release/Calibration/NAO 
####     and named with its respective routine 
####     name.
#### Person Calibration:
#### - Run each routine via Choregraphe suit on
#### the     directory    .../Code/Ver_Release/
#### Calibration/Routines.
#### - Record