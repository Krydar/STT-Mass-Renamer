import os
import whisper
import shutil
import logging
import torch
import time
import sys
import argparse
import threading

'''
                 ..............              
             ......................          
          ..:+:...            ...:+...       
        .-#++:.                  .:=+#-.     
       .:=+=:.                    .:=+=:.    
     ..:++++.                      :#+++:..  
     .=+++=.                        -++++=.  
    .=++++=.                        :=++++=. 
   .=+++++=.                        .=+++++=.
   .=+++++=.                        .=++++++.
   .+++++++:                        :+++++++.
   .+++++++=.                      .++++++++.
   .+++++++=:.                    ::=+++++++.
   .=+++++++=+..                .-#=+++++++=.
   .+++++++++++:...          ...:=+++++++++=.
    :+++++++++++=+:..     ...:=++++++++++++: 
    ..==++++++++++++.     .=++++++++++++=+:. 
     .:=++++++++++++.     .=+++++++++++++:.  
       -#+++++++++++.     .=+++++++++++#-    
        :.=+++++++++.     .=++++++++=+..     
          ..:=++++++.     .=++++++=...       
            ....:=++.     .=++=:....         
                .....     ......

>> Speech-to-text-recognition-powered Mass File Renamer
>> by Kry.exe
>> For the Marathon community

This tool serves a very specific purpose, though you can feel
free to repurpose it for something else and publish it, as
long as there is attribution to the original creator.

This isn't meant to be the most optimized thing ever, I'm
a hobbyist coder and this is just for fun.

Special thanks to the JakeTheAlright community for keeping
the morale high and having such a contagious passion.

I heavily recommend installing CUDA in order to make this
process quicker. CPU-bound AI-powered speech recognition
is painfully slow.

You can get CUDA from: https://developer.nvidia.com/cuda-downloads
If the version in requirements.txt doesn't work for you,
follow the solution to this Stack Overflow post:
https://stackoverflow.com/questions/57814535/assertionerror-torch-not-compiled-with-cuda-enabled-in-spite-upgrading-to-cud
'''

# Progressive console print
def progPrint(s):
    for c in s:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.01)

# Set console colors. It's pretty!
class consoleColors:
    OKGREEN = '\033[92m'
    FAILRED = '\033[91m'
    WHITE = '\033[97m'
    WARN = '\033[93m'

# Copy transcribed text to a new folder
def transferToClean(src, dest, name):
    shutil.copy(src, dest)
    new_path = f"{dest}/{name}"
    shutil.move(f"{dest}/{src}", new_path)

parser = argparse.ArgumentParser(description='Speech-to-text-recognition-powered Mass File Renamer.\nBy Kry.exe for the Marathon community.')
parser.add_argument('--model', type=str, choices=['tiny', 'base', 'small', 'medium', 'large'],
                    help='Override automatic model selection with a specific model size.\nGo to https://github.com/openai/whisper/blob/main/model-card.md for more info.')
args = parser.parse_args()

# Variables for background model loading
model = None
device = None
model_loaded = False
load_error = None
model_size = None

def load_model_background():
    global model, device, model_loaded, load_error, model_size
    try:
        if args.model:
            model_size = args.model
        else:
            if torch.cuda.is_available():
                gpu_properties = torch.cuda.get_device_properties(0)
                vram_gb = gpu_properties.total_memory / (1024**3)
                
                if vram_gb >= 11:
                    model_size = 'large'
                elif vram_gb >= 6:
                    model_size = 'medium'
                elif vram_gb >= 3:
                    model_size = 'small'
                elif vram_gb >= 2:
                    model_size = 'base'
                else:
                    model_size = 'tiny'
            else:
                model_size = 'large'  # Default for CPU
        
        # Load Whisper model
        model = whisper.load_model(model_size)
        
        # Use CUDA for faster transcription if available
        torch.cuda.init()
        device = "cuda"
        model_loaded = True
    except Exception as e:
        load_error = e
        device = "cpu"
        model_loaded = True

# Create "clean" folder if it doesn't exist
if not os.path.exists("clean"):
    os.makedirs("clean")

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('export.log')
formatter = logging.Formatter('[%(levelname)s] %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Start loading model in background
load_thread = threading.Thread(target=load_model_background)
load_thread.start()

# Print fancy text, feel free to comment all of this out lol
print("Connecting...")
time.sleep(1)
print(consoleColors.OKGREEN)

os.system('cls' if os.name == 'nt' else 'clear')

startup_ascii = [
    "CyAc(TM) Secure Terminal v15.193792102158E+9",
    "[UNANTICIPATED SIGNAL OVERRIDE]",
    "<<LOADING AI TRANSLATION LAYER>>",
    "Successfully initialized. Proceeding.",
    "",
    "               ::::::::::            ",
    "           ::::::::::::::::::        ",
    "         ::::::::::::::::::::::.     ",
    "       ::::::::::::::::::::::::::    ",
    "      ::::::::::::::::::::::::::::.  ",
    "    .::::::::::::::::::::::::::::::. ",
    "    :::::::::::::::::::::::::::::::: ",
    "   .::::::::::::::::::::::::::::::::.",
    "   ::::::::::::::::::::::::::::::::::",
    "   :::::::::::::::::     .:::::.     ",
    "   .::::::::::::::::  .:::::::::::.  ",
    "    :::::::::::::::: ::::::::::::::: ",
    "    .:::::::::::::::.:::::::::::::::.",
    "      :::::::::::::::::::::::::::::::",
    "       :::::::::::::.::::::::::::::::",
    "        .::::::::::: ::::::::::::::::",
    "           :::::::::  .::::::::::::::",
    "               :::::     ::::::::::::",
    "",
    "Everything runs on CyAc // OR NOTHING RUNS AT ALL.\n"
]

for i, line in enumerate(startup_ascii):    
    print(line)
    delay = 0.8 * (0.85 ** i)
    delay = max(delay, 0.01)
    time.sleep(delay)

progPrint("===========\n\n")
print("<<ENGAGING AI TRANSLATION LAYER>>")

# Wait for model to finish loading in the background
load_thread.join()

# Check results of model loading
if load_error:
    print(consoleColors.WARN + "Failed to load CUDA. Switching to CPU. Check export.log for details.")
    logger.warning("Skipped CUDA initialization. Using CPU instead.")
    logger.warning(str(load_error))
else:
    if device == "cuda":
        print("Successfully loaded CUDA.\n")
        logger.info("CUDA Initialized")
        if torch.cuda.is_available():
            gpu_properties = torch.cuda.get_device_properties(0)
            vram_gb = gpu_properties.total_memory / (1024**3)
            print(f"DETECTED {vram_gb:.1f}GB VRAM // SELECTING MODEL\nSELECTED    >>> ['{model_size}']")
    else:
        print("Running on CPU (no CUDA available)\n")
        logger.info("Running on CPU")
    
    if model_size != 'large':
        print(f"RECCOMENDED >>> ['large']\n[TRANSCRIPTION ACCURACY MAY BE DEGRADED]\n")
    
    progPrint("[##############################] 100%\n")
    print("")

suffix = 1
# Start loop for reading the files
for fname in os.listdir(os.getcwd()):
    fileFound = False # Set boolean for suffix adding later
    if(os.path.splitext(fname)[1] == ".wav"): # Check extension
        with open(fname, 'r') as f:
            # Remove unnecessary data from the fname
            splitFilename = str(f).split("'")
            filenameClean = splitFilename[1]
            try:
                text = model.transcribe(filenameClean, language="en", fp16=False) # Start transcription
                sanitizedText = ''.join(c for c in text['text'] if c not in '\\/:*?"<>|') # Sanitize text for filename
                if(os.path.isfile('clean\\' + sanitizedText + '.wav') == True): # Check if the dest file already exists
                    print(consoleColors.WARN + "WARNING: FILE WITH THE SAME NAME EXISTS. ADDING SUFFIX.")
                    warn = "File found: " + sanitizedText + ".wav (Source file: " + filenameClean + "). Adding suffix."
                    logger.warning(warn)
                    fileFound = True
            except Exception as e:
                if(type(e).__name__ == "UnknownValueError"): # Speech was unable to be recognized
                    print(consoleColors.WARN + "WARNING: SPEECH NOT RECOGNIZED.")
                    # Remove unnecessary data from the fname
                    transferToClean(filenameClean, "clean", "WARN_" + filenameClean)
                    warn = "File failed to transcribe: " + filenameClean + ".wav"
                    logger.warning(warn)
                    
                else:
                    print(consoleColors.FAILRED)
                    raise(e)
                    print(consoleColors.WHITE)
            else:
                # Copy the file into a separate folder with a new fname
                if(fileFound == True):
                    while(os.path.isfile('clean\\' + sanitizedText + "_" + str(suffix) + ".wav") == True):
                        suffix += 1 # Iterate until the filename doesn't exist in case there's more than 1 repeat
                    repeatFile = sanitizedText + "_" + str(suffix) + ".wav" # Add suffix
                    transferToClean(filenameClean, "clean", repeatFile) # Copy file to a new folder with the new name
                    print(consoleColors.WARN + filenameClean, "->", repeatFile) # Print source and dest
                    success = filenameClean + " -> " + repeatFile
                    logger.info(success)
                    suffix = 1 # Reset the suffix
                else:
                    suffix = 1 # Reset the suffix
                    transferToClean(filenameClean, "clean", sanitizedText + ".wav") # Copy file to new folder with the new name
                    print(consoleColors.OKGREEN + filenameClean, "->", sanitizedText + ".wav")
                    success = filenameClean + " -> " + sanitizedText + ".wav"
                    logger.info(success)
        f.close() # Remember to close your files!!
    else:
        print(consoleColors.WARN + "WARNING: Not a WAV file.")
        notWAV = "Not a WAV file. Skipping. (Filename: " + str(fname) + ")"
        logger.warning(notWAV)
        pass
print(consoleColors.WHITE) # Unless you want a permanently green/yellow/whatever console :)
