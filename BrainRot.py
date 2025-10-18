from src import ASCII_dict
from assets import Binary2BrainRot
from assets import BrainRot2Binary
from pathlib import Path
import platform

currentDir = Path(__file__).resolve().parent

def newCommand():
    return input(f"\033[1;32;40minterpreter@brainrot\033[0m: \033[1;32;34m{currentDir}\033[0m$ ").split()

def interpreter(inputValues):
    inputValues = ''.join('1' if bit == '\t' else '0' if bit == ' ' else bit for bit in inputValues)    #Convert BrainRot to Binary
    linesList = inputValues.split('\n')     #Split lines

    for line in linesList:
        if '//' in line:
            line = line.split('//', 1)[0]

        if not line.strip():
            continue  # Skip blank/comment-only lines early

        binary = list(line) # Convert the line into a list of characters again
        lineOutput = ""
        i = 0
        lenLine = len(line)
        while i + 8 <= lenLine:
            ASCII_8bits = line[i:i+8]
            i += 8

            char = ASCII_dict.reversed_ascii_dict.get(ASCII_8bits)
            if char:
                lineOutput += char
            else:
                print(f"[\033[31mFAILED\033[0m] Unknown binary sequence: {ASCII_8bits}")
                break

        if binary:
            print(f"[\033[31mWARNING\033[0m] Ignoring leftover bits: {line[i:]}")

        if lineOutput:
            print(lineOutput)

        

def brainrotTranslateDirectly(_=None):
    inputValues = ""
    while inputValues not in ("e", "exit"):
        inputValues = input(">>> ")
        interpreter(inputValues)
    return


def changeDirCommand(inputCommand):
    global currentDir

    if len(inputCommand) < 2:
        currentDir = Path.home()
        return

    targetDir = inputCommand[1]

    if targetDir == "/":
        # Linux/macOS root is / and Windows is C:\
        currentDir = Path(currentDir.anchor)
        return
    
    if platform.system() == "Windows" and len(targetDir) == 2 and targetDir[1] == ":":
        windowsDrive = Path(targetDir + "\\")  # e.g. "D:\\"
        if windowsDrive.exists():
            currentDir = windowsDrive
            return
        else:
            print(f"[\033[31mERROR\033[0m] cd: {targetDir}: Drive not found")
            return

    if targetDir.startswith("..") and all(dot == '.' for dot in targetDir): #Go up dir
        dotCount = len(targetDir) - 1  # ".." = 0 extra dots. number of levels to go up

        for _ in range(dotCount):
            currentDir = currentDir.parent
        return

    newDir = (currentDir / targetDir).resolve()

    if newDir.exists() and newDir.is_dir():
        currentDir = newDir
        return
    else:
        print(f"[\033[31mERROR\033[0m] cd: {targetDir}: No such file or directory")
        return

def listDirContent(_=None):
    global currentDir
    dirContentFolders = [f.name for f in currentDir.iterdir() if f.is_dir()]
    dirContentFiles = [f.name for f in currentDir.iterdir() if f.is_file()]
    print(f"\033[94m{"\t".join(dirContentFolders)}\033[0m")
    print("\t".join(dirContentFiles))


def exitCommand(_=None):
    print("Exiting...")
    exit()

def brainrot2binary():
    print("Hello from BrainRot2Binary!")

def binary2brainrot():
    print("Hello from Binary2BrainRot!")

def main():
    while True:
        inputCommand = newCommand()
        if not inputCommand:
            continue

        command =  inputCommand[0]

        if command in commandList:
            commandList[command](inputCommand)
            continue

        else:
            # Navigate to the file to translate it
            print("Unknown Command!")
        



greetMessage = """
     ############################
    #                            #
    #          BrainRot          #
    #                            #
     ############################

Welcome to BrainRot interpreter!
"""
brainrotCommand = {
    changeDirCommand: ("cd", "CD"),
    listDirContent: ("ls", "LS"),
    brainrotTranslateDirectly: ("BrainRot", "brainrot", "br"), 
    brainrot2binary: ("BrainRot2Binary", "brainrot2binary", "br2b"), 
    binary2brainrot: ("Binary2BrainRot", "binary2brainrot", "b2br"),
    exitCommand: ("e", "E", "exit", "Exit", "EXIT")
}

commandList = {
    alias: func
    for func, command in brainrotCommand.items()
    for alias in command
}

if __name__ == "__main__":
    print(greetMessage)
    main()
            
            