from src import ASCII_dict
from pathlib import Path
import platform
import os

def interpreter(inputValues):
    inputValues = ''.join('1' if bit == '\t' else '0' if bit == ' ' else bit for bit in inputValues)    #Convert BrainRot to Binary
    if '//' in inputValues:
        inputValues = inputValues.split('//', 1)[0]

    if not inputValues.strip():
        return  # Skip blank/comment-only lines early
    
    valuesOutput = ""
    i = 0
    lenInputValues = len(inputValues)
    while i + 8 <= lenInputValues:
        ASCII_8bits = inputValues[i:i+8]
        i += 8

        char = ASCII_dict.reversed_ascii_dict.get(ASCII_8bits)
        if char:
            valuesOutput += char
        else:
            print(f"[\033[31mFAILED\033[0m] Unknown binary sequence: {ASCII_8bits}")
            break

    if i<lenInputValues:
        print(f"[\033[31mWARNING\033[0m] Ignoring leftover bits: {inputValues[i:]}")

    if valuesOutput:
        print(valuesOutput)

def brainrot(targetFile):
    global currentDir
    if not targetFile:
        while True:   
            inputValues = input(">>> ")
            if inputValues in ("e", "exit"):
                break
            interpreter(inputValues)
    else:
        targetFileDir = Path(currentDir / targetFile).resolve()
        if targetFileDir.exists():
            with targetFileDir.open("r") as file:
                for line in file:
                    interpreter(line)
            return

        targetFileDir = Path(targetFile).resolve() 
        if targetFileDir.exists():
            with targetFileDir.open("r") as file:
                for line in file:
                    interpreter(line)
            return
        
        print(f"[\033[31mFAILED\033[0m] No file was found!")

def brainrot2binary(targetFile):
    global currentDir
    if not targetFile:
        print("Welcome to BrainRot2Binary! Please provide the file path!")
        print("For more information, go to https://github.com/jammyjunior/BrainRot.")
    else:
        def br2bInterpreter(targetFilePath):
            targetFileContent = []
            outputFilePath = targetFilePath.with_stem(targetFilePath.stem + "_brainrot2binary")
            with targetFilePath.open("r") as tf:
                for line in tf:
                    targetFileContent.append(line)

            targetFileContent = [
                ''.join('1' if bit == '\t' else '0' if bit == ' ' else bit for bit in line)
                  for line in targetFileContent
            ]    #Convert BrainRot to Binary

            with outputFilePath.open("w") as of:
                for line in targetFileContent:
                    of.write(line)

            print(f"[\033[32mOK\033[0m] File save to: {outputFilePath}")

        targetFilePath = Path(currentDir / targetFile).resolve()
        if targetFilePath.exists():
            br2bInterpreter(targetFilePath)
            return

        targetFilePath = Path(targetFile).resolve() 
        if targetFilePath.exists():
            br2bInterpreter(targetFilePath)
            return
        
        print(f"[\033[31mFAILED\033[0m] No file was found!")

def binary2brainrot(targetFile):
    global currentDir
    if not targetFile:
        print("Welcome to Binary2BrainRot! Please provide the file path!")
        print("For more information, go to https://github.com/jammyjunior/BrainRot.")
    else:
        def b2brInterpreter(targetFilePath):
            targetFileContent = []
            outputFilePath = targetFilePath.with_stem(targetFilePath.stem + "_binary2brainrot")
            with targetFilePath.open("r") as tf:
                for line in tf:
                    targetFileContent.append(line)

            targetFileContent = [
                ''.join('\t' if bit == '1' else ' ' if bit == '0' else bit for bit in line)
                  for line in targetFileContent
            ]    #Convert BrainRot to Binary

            with outputFilePath.open("w") as of:
                for line in targetFileContent:
                    of.write(line)

            print(f"[\033[32mOK\033[0m] File save to: {outputFilePath}")

        targetFilePath = Path(currentDir / targetFile).resolve()
        if targetFilePath.exists():
            b2brInterpreter(targetFilePath)
            return

        targetFilePath = Path(targetFile).resolve() 
        if targetFilePath.exists():
            b2brInterpreter(targetFilePath)
            return
        
        print(f"[\033[31mFAILED\033[0m] No file was found!")

def catFile(targetFile):
    global currentDir
    if not targetFile:
        print("Welcome to cat! Please provide the file path!")
        print("For more information, go to https://github.com/jammyjunior/BrainRot.")
    else:
        targetFileDir = Path(currentDir / targetFile).resolve()
        if targetFileDir.exists():
            with targetFileDir.open("r") as file:
                for line in file:
                    print(line, end="")
                print()
            return

        targetFileDir = Path(targetFile).resolve() 
        if targetFileDir.exists():
            with targetFileDir.open("r") as file:
                for line in file:
                    print(line, end="")
                print()
            return
        
        print(f"[\033[31mFAILED\033[0m] No file was found!")

def changeDirCommand(targetDir):
    global currentDir
    if not targetDir:
        currentDir = Path.home()
        return

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
    
def helpCommand(_=None):
    print("""
    br        :Run the BrainRot interpreter
    br2b      :Run the BrainRot2Binary interpreter
    b2br      :Run the Binary2BrainRot interpreter
    cat       :Show file contents
    clear     :Clear the terminal
    cd        :Change directory
    exit      :Exit the interpreter
    help      :Show help
    ls      :List directory contents
          
    Note: After 'br', 'br2b', 'b2br', 'cat', 'cd', please provide the target file path or directory. 
    For more information, go to https://github.com/jammyjunior/BrainRot.
    """)

def listDirContent(_=None):
    global currentDir
    dirContentFolders = [f.name for f in currentDir.iterdir() if f.is_dir()]
    dirContentFiles = [f.name for f in currentDir.iterdir() if f.is_file()]
    print(f"\033[94m{"\t".join(dirContentFolders)}\033[0m")
    print("\t".join(dirContentFiles))

def clearCommand(_=None):
    if platform.system() == "Windows": # For Windows
        _ = os.system('cls')
    else:               # For macOS and Linux
        _ = os.system('clear')
    return

def exitCommand(_=None):
    print("Exiting...")
    exit()

def main():
    global currentDir
    while True:
        inputCommand = input(f"\033[1;32;40minterpreter@brainrot\033[0m: \033[1;32;34m{currentDir}\033[0m$ ").split()
        if not inputCommand:
            continue

        command =  inputCommand[0]
        target = " ".join(inputCommand[1:])

        if command in commandList:
            commandList[command](target)
            continue

        else:
            print("Unknown Command!")
        
greetMessage = f"""
     ############################
    #                            #
    #          BrainRot          #
    #                            #
     ############################

Version: 0.1.0
OS: {platform.system()}
Welcome to BrainRot interpreter! For a new user, type "help" for help, "exit" to exit the interpreter."""

brainrotCommand = {
    brainrot: ("BrainRot", "brainrot", "br"),
    brainrot2binary: ("br2b", "BR2B", "BrainRot2Binary", "brainrot2binary"),
    binary2brainrot: ("b2br", "B2BR", "Binary2BrainRot", "binary2brainrot"),
    catFile: {"c", "cat"}, 
    clearCommand: {"clear", "cls"},
    changeDirCommand: ("cd", "CD"),
    helpCommand: {"h", "help"},
    listDirContent: ("ls", "LS"),
    exitCommand: ("e", "E", "exit", "Exit", "EXIT")
    }

commandList = {
    alias: func
    for func, command in brainrotCommand.items()
    for alias in command
}

if __name__ == "__main__":
    currentDir = Path(__file__).resolve().parent
    print(greetMessage)
    main()




# Made by JammyJunior
# https://github.com/jammyjunior
            