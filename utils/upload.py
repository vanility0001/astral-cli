import requests, json, mimetypes, os
from urllib.parse import urlparse, parse_qs
from tkinter import Tk
# Files

import utils.accounts
import data

class upload():
    def uploadFile(self, path):
        if os.path.getsize(path) > 100000000:
            userChoice = input("[?] The file you're trying to upload is above Astral's 100mb upload limit. Do you wish to override? [y/N]: ")
            if userChoice.lower() == "n":
                print("[x] Cancelling upload...")
                return
            print("[v] Overriding local file size check...")
        
        print("[\] Uploading file " + path + "...")
        try:
            files = open(path,"rb")
        except:
            print("[x] Couldn't read file.")
            return
        
        authorization = {
            "Authorization": data.configdata["credentials"]["uploadkey"]
        }
        files = {
            "file": (files.name, files, mimetypes.guess_type(path)[0])
        }
        try:
            uploadRequest = requests.post(data.configdata["credentials"]["endpoint"] + "files", files=files, headers=authorization)
        except:
            print("[x] An unexpected error occured while uploading " + path + ".")
            return
        try:
            responseJSON = json.loads(uploadRequest.content)
        except Exception as e:
            print("[x] Received unexpected response from Astral API. Debug info below:\n\n" + str(e) + "\n\nJSON Response:\n" + str(uploadRequest.content))
            return
        if responseJSON["code"] == "success":
            r = Tk()
            r.withdraw()
            r.clipboard_clear()
            r.clipboard_append(requests.utils.unquote(requests.utils.quote(responseJSON["fileURL"].encode(), safe=':/')))
            r.update() # now it stays on the clipboard after the window is closed
            r.destroy()
            print("Upload URL: " + requests.utils.unquote(requests.utils.quote(responseJSON["fileURL"].encode(), safe=':/')) + "\nDelete URL: " + responseJSON["deletionURL"] + "\n\n[!] Upload URL has been copied to clipboard.")
        else:
            print("[x] Error uploading file.\n")
            if responseJSON["message"] == "Invalid mimetype":
                print("Invalid file type. Did you try to upload a disallowed file?")
            elif responseJSON["message"] == "The provided upload key does not exist":
                print("Invalid API key. Did you edit your key in data.json?")