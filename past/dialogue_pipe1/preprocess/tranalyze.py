import os
import sys

dst = "/mnt/c/Users/zolbo/whatsapp/whatsapp/dialogues/dialogue"
apps = ["sig", "tea", "wha", "tel", "mes", "dis"]
if __name__ == "__main__":
    for app in apps:
        name = f"{app}"
        if os.path.isdir(f"{dst}/trans/{name}_tran"):
            os.system(f"rm -r {dst}/trans/{name}_tran")
        file_name = None
        for f in os.listdir(f"{dst}/combined/"):
            if name+"_combined" in f:
                file_name = f
        os.system(f"tranalyzer -r {dst}/combined/{file_name} -w {dst}/trans/{name}_tran/")