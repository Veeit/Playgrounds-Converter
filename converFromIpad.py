import os, shutil, glob
import xml.etree.ElementTree as ET
import re


path = input("Convert: Playground Path: ")
path = path.replace('\ ', " ")[:-1]

def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

newPath = path.rsplit('/', 1)[:-1][0]
newPath = newPath + "/Converted-Playground.playgroundbook"
print(newPath)
copytree(path, newPath)

def copyfiles(source, ziel):
    if os.path.isdir(source) and os.path.isdir(ziel) :
        for file_name in os.listdir(source):
            full_file_name = os.path.join(source, file_name)
            if os.path.isfile(full_file_name):
                shutil.copy(full_file_name, ziel)
    else:
        print("no folder")

PageManifest = """ 
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>Name</key>
	<string>My Playground</string>
	<key>LiveViewEdgeToEdge</key>
	<false/>
	<key>LiveViewMode</key>
	<string>HiddenByDefault</string>
</dict>
</plist>
"""

PagesArray = []

def copyPages(source, ziel):
    count = 0
    if os.path.isdir(source) and os.path.isdir(ziel) :
        for file_name in os.listdir(source):
            rex = re.compile(r'<string>(.*)</string>', re.DOTALL)

            outname = ziel + "/New Page " + str(count) + ".playgroundpage/main.swift"
            outmanifest = ziel + "/New Page " + str(count) + ".playgroundpage/Manifest.plist"
            PagesArray.append("New Page " + str(count) + ".playgroundpage")
            count += 1
            
            print(outname)
            with open(source + "/" + file_name + "/main.swift.delta" , "r") as delta:
                data = delta.read()
                m = re.compile('<string>(.*?)</string>', re.DOTALL).findall(data)
                print(max(m, key=len))
                os.makedirs(os.path.dirname(outname), exist_ok=True)
                with open(outname, "w+") as out:
                    out.write(max(m, key=len))
                with open(outmanifest, "w+") as out:
                    out.write(PageManifest)
                
    else:
        print("no folder")

def addPagesToChapter():
    tree = ET.parse(newPath + "/Contents/Chapters/Chapter1.playgroundchapter/manifest.plist")
    root = tree.getroot()

    for child in root:
        if child.tag == "dict":
            key = ET.Element("key")
            key.text = "Pages"
            pageArray = ET.Element("array")
            for pageStr in PagesArray:
                print(pageStr)
                page      = ET.Element("string")
                page.text =  str(pageStr)
                pageArray.append(page)

            child.append(key)
            child.append(pageArray)
            
            print(child.tag, child.attrib)

    tree.write(open(newPath + "/Contents/Chapters/Chapter1.playgroundchapter/manifest.plist", 'wb+'))

copyfiles(path + "/Edits/UserEdits.diffpack/UserModules/UserModule.playgroundmodule/Sources", newPath + "/Contents/UserModules/UserModule.playgroundmodule/Sources")
copyPages(path + "/Edits/UserEdits.diffpack/Chapters/Chapter1.playgroundchapter/Pages", newPath + "/Contents/Chapters/Chapter1.playgroundchapter/Pages")
addPagesToChapter()