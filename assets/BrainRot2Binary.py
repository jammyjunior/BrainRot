from pathlib import Path
from BrainRot import BrainRot
from assets import Binary2BrainRot

def brainrot():
    pass

def brainrot2binary():
    pass
def binary2brainrot():
    pass

def exitCommand():
    if __name__ == "__main__":
        print("Exiting...")
        exit()

def main(currentDir):
    while True:
        inputCommand = input(f"\033[1;32;40minterpreter@brainrot2binary\033[0m: \033[1;32;34m{currentDir}\033[0m$ ").split()
        if not inputCommand:
            continue

        command =  inputCommand[0]
        target = " ".join(inputCommand[1:])

        if command in commandList:
            commandList[command](target)
            continue

        else:
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
    BrainRot.brainrot: ("BrainRot", "brainrot", "br"),
    BrainRot.catFile: {"c", "cat"}, 
    BrainRot.changeDirCommand: ("cd", "CD"),
    BrainRot.listDirContent: ("ls", "LS"),
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
    currentDir = Path(__file__).resolve().parent
    main(currentDir)