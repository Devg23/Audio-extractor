from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import ttk
import moviepy.editor as me
import threading

filename = ''
stop_conversion = False

def convert():
    global filename, stop_conversion
    stop_conversion = False  # Reset stop flag

    try:
        video = me.VideoFileClip(filename)
        audio = video.audio
        file = asksaveasfilename(defaultextension=format.get(), filetypes=[("Audio files", "*.mp3 *.wav *.ogg")])
        
        if file:
            # Show loading text and start progress bar
            loading_label.config(text="Converting...", fg="blue")
            progress_bar.start(10)
            root.update()
            
            # Perform conversion and check for stop condition
            for chunk in audio.iter_chunks(chunk_size=1024):  # Process in chunks for stopping ability
                if stop_conversion:
                    loading_label.config(text="Conversion Stopped", fg="red")
                    progress_bar.stop()
                    audio.close()  # Close the audio resource
                    return
                audio.write_audiofile(file)
                
            loading_label.config(text="Conversion Complete!", fg="green")
            progress_bar.stop()
    except Exception as e:
        loading_label.config(text="Error during conversion", fg="red")
        progress_bar.stop()
        print(f"Error: {e}")

def select():
    global filename
    filetypes = (('Video files', '*.WEBM *.MPG *.MP4 *.AVI *.WMV *.MOV *.FLV'), ('All files', '*.*'))
    filename = askopenfilename(filetypes=filetypes)
    if filename:
        label3.config(text="File Selected", fg="green")
        label4 = Label(root, text="Select Audio Format:", font=("Arial", 16), bg="#f0f0f5")
        label4.pack()
        label4.place(x=125, y=250)

        options = [".mp3", ".ogg", ".wav"]
        format.set(".mp3")
        menu = OptionMenu(root, format, *options)
        menu.config(width=8, font=("Arial", 12), bg="#ffffff", fg="#333333")
        menu.pack()
        menu.place(x=375, y=250)

        # Export and Stop Buttons
        button3 = Button(root, text="Export", font=("Arial", 12), command=lambda: threading.Thread(target=convert).start(),
                         width=10, height=1, bg="#4CAF50", fg="white", activebackground="#45a049", relief=FLAT)
        button3.pack()
        button3.place(x=250, y=300)

        button4 = Button(root, text="Stop", font=("Arial", 12), command=stop_conversion_func, 
                         width=10, height=1, bg="#FF5733", fg="white", activebackground="#FF0000", relief=FLAT)
        button4.pack()
        button4.place(x=350, y=300)

        button3.bind("<Enter>", lambda e: button3.config(bg="#45a049"))
        button3.bind("<Leave>", lambda e: button3.config(bg="#4CAF50"))
        button4.bind("<Enter>", lambda e: button4.config(bg="#FF0000"))
        button4.bind("<Leave>", lambda e: button4.config(bg="#FF5733"))

def stop_conversion_func():
    global stop_conversion
    stop_conversion = True  # Set the stop flag

# Create the main window with gradient background
root = Tk()
root.geometry("600x400")
root.title("Video to Audio Converter")

# Create a Canvas for gradient background
canvas = Canvas(root, width=600, height=400)
canvas.pack(fill="both", expand=True)

# Define the gradient colors
canvas.create_rectangle(0, 0, 600, 400, fill="#89CFF0", outline="")
canvas.create_rectangle(0, 200, 600, 400, fill="#E0BBE4", outline="")

# Style the main label with shadow effect
label1 = Label(root, text="Video to Audio Converter", font=("Helvetica", 26, "bold"), fg="white", bg="#89CFF0")
label1_window = canvas.create_window(300, 50, anchor="center", window=label1)

# File Selection Prompt
label2 = Label(root, text="Select a Video file to Convert", font=("Arial", 16), fg="#333333", bg="#89CFF0")
label2_window = canvas.create_window(300, 120, anchor="center", window=label2)

# Select Button with rounded effect
button1 = Button(root, text="Select", font=("Arial", 12), command=select, width=10, height=1, bg="#2196F3", fg="white",
                 activebackground="#0b7dda", relief=FLAT)
button1_window = canvas.create_window(300, 170, anchor="center", window=button1)

# File Selected Label
label3 = Label(root, font=("Arial", 16, "bold"), fg="gray", bg="#89CFF0")
label3_window = canvas.create_window(300, 200, anchor="center", window=label3)

# Loading/Done Label
loading_label = Label(root, font=("Arial", 14), fg="green", bg="#E0BBE4")
loading_label_window = canvas.create_window(300, 350, anchor="center", window=loading_label)

# Progress Bar
progress_bar = ttk.Progressbar(root, orient=HORIZONTAL, length=200, mode='indeterminate')
progress_bar_window = canvas.create_window(300, 325, anchor="center", window=progress_bar)

# Audio format selection variable
format = StringVar()

# Add hover effects
button1.bind("<Enter>", lambda e: button1.config(bg="#0b7dda"))
button1.bind("<Leave>", lambda e: button1.config(bg="#2196F3"))

# Run the main loop
root.mainloop()
