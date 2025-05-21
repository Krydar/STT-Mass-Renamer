import os
import whisper
import shutil
import logging
import torch
import time
import sys

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

# Load Whisper model
model = whisper.load_model('large')

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

# Print fancy text, feel free to comment all of this out lol
print(consoleColors.OKGREEN)
print("CyAc(TM) Secure Terminal v15.193792102158E+9")
print("[UNANTICIPATED SIGNAL OVERRIDE]")
print("<<ENGAGING AI TRANSLATION LAYER>>")
print("Successfully initialized. Proceeding.")
print("")
print("               ::::::::::            ")
time.sleep(0.001)
print("           ::::::::::::::::::        ")
time.sleep(0.001)
print("         ::::::::::::::::::::::.     ")
time.sleep(0.001)
print("       ::::::::::::::::::::::::::    ")
time.sleep(0.001)
print("      ::::::::::::::::::::::::::::.  ")
time.sleep(0.001)
print("    .::::::::::::::::::::::::::::::. ")
time.sleep(0.001)
print("    :::::::::::::::::::::::::::::::: ")
time.sleep(0.001)
print("   .::::::::::::::::::::::::::::::::.")
time.sleep(0.001)
print("   ::::::::::::::::::::::::::::::::::")
time.sleep(0.001)   
print("   :::::::::::::::::     .:::::.     ")
time.sleep(0.001)
print("   .::::::::::::::::  .:::::::::::.  ")
time.sleep(0.001)
print("    :::::::::::::::: ::::::::::::::: ")
time.sleep(0.001)
print("    .:::::::::::::::.:::::::::::::::.")
time.sleep(0.001)
print("      :::::::::::::::::::::::::::::::")
time.sleep(0.001)
print("       :::::::::::::.::::::::::::::::")
time.sleep(0.001)
print("        .::::::::::: ::::::::::::::::")
time.sleep(0.001)        
print("           :::::::::  .::::::::::::::")
time.sleep(0.001)
print("               :::::     ::::::::::::")
print("")
print("Everything runs on CyAc // OR NOTHING RUNS AT ALL.\n")
progPrint("===========\n")
print("")

#Use CUDA for faster transcription if available
try:
    torch.cuda.init()
    device = "cuda"
    print("Successfully loaded CUDA.\n")
    logger.info("CUDA Initialized")
    progPrint("[##############################] 100%\n")
    print("")
except Exception as e:
    print(consoleColors.WARN + "Failed to load CUDA. Switching to CPU. Check export.log for details.")
    logger.warning("Skipped CUDA initialization. Using CPU instead.")
    logger.warning(str(e))
    pass

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
                sanitizedText = ''.join(c for c in text['text'] if c not in '\/:*?"<>|') # Sanitize text for filename
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
