import moviepy.editor as me
from tkinter import *
from tkinter.filedialog import askopenfilename

Tk().withdraw()

filetypes = (
    ('video files','*.WEBM,*.MP4,*.MPG,*.MP2,*.MPEG,*.MPE,*.MPW,*M4P,*.FLV','*.MOV','*.QT'),
    ('All files','*.*')
)
filename = askopenfilename(filetypes = filetypes)
# print(filename)
video = me.VideoFileClip(filename)

audio = video.audio

audio.write_audiofile("test.mp3")