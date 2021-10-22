import shutil
import PyInstaller.__main__

def deleteDirectory(src):
    print("deleting " + src)
    try:
        shutil.rmtree(src)
    except shutil.Error as e:
        print("Directory not copied. Error: %s" %e)
    except OSError as e:
        print("Directory not copied. Error: %s" %e)

def copyDirectory(src, dest):
    print("copying " + src + " to " + dest)
    try:
        shutil.copytree(src, dest)
    except shutil.Error as e:
        print("Directory not copied. Error: %s" %e)
    except OSError as e:
        print("Directory not copied. Error: %s" %e)
        
def build():
    PyInstaller.__main__.run(["--onefile", "main.py"])

deleteDirectory("./dist")
build()
copyDirectory("./assets", "./dist/assets")
    