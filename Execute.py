import cv2
import numpy as np
import os
from os.path import isfile, join
import subprocess

#Function to convert_frames_to_video   
def convert_frames_to_video(pathIn,pathOut,fps):
    frame_array = []
    files = [f for f in os.listdir(pathIn) if isfile(join(pathIn, f))]
 
    #for sorting the file names properly
    files.sort(key = lambda x: int(x[5:-4]))
 
    for i in range(len(files)):
        filename=pathIn + files[i]
        #reading each files
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
        print(filename)
        #inserting the frames into an image array
        frame_array.append(img)
 
    out = cv2.VideoWriter(pathOut,cv2.VideoWriter_fourcc(*'mp4v'), fps, size)
 
    for i in range(len(frame_array)):
        # writing to a image array
        out.write(frame_array[i])
    out.release()

def main_Execute(username, validity):    
    #Check to remove the past of audio and video in video directory
    if os.path.isfile('video//audio.wav'):
        os.remove('video//audio.wav')
    if os.path.isfile('video//ColorizedVideo1.mp4'):
        os.remove('video//ColorizedVideo1.mp4')
    if os.path.isfile('video//ColorizedVide.mp4'):
        os.remove('video//ColorizedVide.mp4')
    #Check to remove the past of video in static directory
    if os.path.isfile('static//ColorizedVideo.mp4'):
        os.remove('static//ColorizedVideo.mp4')
    #Audio seperator
    command = "ffmpeg -i video//GrayscaleVideo.mp4 -ab 160k -ac 2 -ar 44100 -vn video//audio.wav"
    subprocess.call(command, shell=True)

    '''#Execute VideoColorizer.py
    cmd = 'python VideoColorizer.py --prototxt model/colorization_deploy_v2.prototxt --model model/colorization_release_v2.caffemodel --points model/pts_in_hull.npy'
    subprocess.call(cmd, shell=True)'''                              

    #Creat Colorized_video with frames     
    pathIn= 'video//images//'
    pathOut = 'video//ColorizedVide.mp4'
    fps = 24.0
    convert_frames_to_video(pathIn, pathOut, fps)

    #Combine audio to video
    command2 = 'ffmpeg -i video//ColorizedVide.mp4 -i video//audio.wav \
    -c:v copy -c:a aac -strict experimental \
    -map 0:v:0 -map 1:a:0 video//ColorizedVideo1.mp4'
    subprocess.call(command2, shell=True)
    #Remove Silent video
    os.remove('video//ColorizedVide.mp4')
    #To check if directory of user exists or not
    if not os.path.exists('static//UserColorizedVideos//' + username):
        os.makedirs('static//UserColorizedVideos//' + username)
    #play video on site
    cmd1 = 'ffmpeg -i video//ColorizedVideo1.mp4 -f mp4 -vcodec libx264 -preset superfast -profile:v high444 -acodec aac static//UserColorizedVideos//' + username + '//ColorizedVideo'+ str(100 - int(validity)) +'.mp4 -hide_banner'
    subprocess.call(cmd1, shell=True)
    #Remove unplayed video in site
    os.remove('video//ColorizedVideo1.mp4')
