from moviepy.editor import VideoFileClip,AudioFileClip
from pydub import AudioSegment
import numpy as np
import os
import playsound

def audiosegment_to_videofileclip(audio,videoclip,outname):
    # Duration of the audio segment
    audio_segment=AudioFileClip(audio)
    
    
    # Create a black screen video with the same duration as the audio
    videoclip = VideoFileClip(videoclip)
    
    # Replace the audio of the video clip with the audio segment
    videoclip = videoclip.set_audio(audio_segment)
    
    videoclip.write_videofile(outname, codec='libx264')


def edit(mainfile,insertfile,startime,endtime):
    # Load the main audio file
    main_audio = AudioSegment.from_file(mainfile)

    # Load the audio clip you want to insert
    insert_audio = AudioSegment.from_file(insertfile)

    len_file=len(insert_audio)
    #endtime=[i+len_file for i in startime]
    
    

    # Replace the part of the main audio with the insert audio
    for i,j in enumerate(startime):
        if i==0:
            #
            output_audio = main_audio[: startime[i]] + insert_audio+ main_audio[endtime[i]:]
        else:
            output_audio = output_audio[: startime[i]] + insert_audio + main_audio[endtime[i]:]

    name=insertfile.split(".")[0]+"output_audio.wav"

    # Export the result to a file
    output_audio.export(name, format="wav")
    return name



def stretch_or_compress_audio(input_file, output_file, target_duration_seconds):
    # Load the audio file
    audio = AudioSegment.from_file(input_file)

    # Get the current duration of the audio
    current_duration_seconds = len(audio) / 1000  # Length of audio in seconds

    # Calculate the speed ratio required to stretch or compress the audio
    speed_ratio = target_duration_seconds / current_duration_seconds

    # Apply time stretching or compressing
    stretched_audio =  audio.set_frame_rate(int(audio.frame_rate / speed_ratio))

    # Export the modified audio to a file
    stretched_audio.export(output_file, format="wav")  # Change format if needed



def get_wave_files(path):
    # Initialize an empty list to store wave files
    wave_files = []

    # Navigate through the directory
    for root, dirs, files in os.walk(path):
        # Search for files with .wav extension
        for file in files:
            if file.endswith(".wav"):
                # If file ends with .wav, append its absolute path to the list
                wave_files.append(os.path.join(root, file))
    
    return wave_files




if __name__ == "__main__":
    x=get_wave_files("Downloads/audio_in")
    lis=[i.replace("\\", "/") for i in x]
    for i in lis:
        x=edit("Downloads/aap_audio.wav",i,[900,121000],[2900,122500])
        #playsound.playsound(x)
        audio=AudioFileClip(x)
        #audio.preview()
        video=VideoFileClip("Downloads/aap.mp4")
        video=video.set_audio(audio)
        video.write_videofile("{}.mp4".format(i.split(".")[0]), codec='libx264')
        audio.close()
        video.close()


