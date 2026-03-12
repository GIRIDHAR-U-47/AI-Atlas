import os
import shutil

base_data = r'd:\AI-Atlas\web-app\data'

# Map existing name to new numeric prefix
merges = {
    "02-Machine-Learning": "03-Machine-Learning",
    "03-Deep-Learning": "04-Deep-Learning",
    "04-Computer-Vision": "05-Computer-Vision",
    "05-Natural-Language-Processing": "06-Natural-Language-Processing",
    "06-Multimodal-AI": "07-Generative-AI",
    "07-Large-Language-Models": "07-Generative-AI",
    "08-Responsible-Explainable-AI": "10-Society-and-Ethics"
}

def merge_folders():
    for old_name, new_name in merges.items():
        old_path = os.path.join(base_data, old_name)
        new_path = os.path.join(base_data, new_name)

        if os.path.exists(old_path):
            print(f"Merging {old_name} into {new_name}...")
            # If new_path doesn't exist, just rename
            if not os.path.exists(new_path):
                os.rename(old_path, new_path)
            else:
                # Iterate and move contents
                for item in os.listdir(old_path):
                    s = os.path.join(old_path, item)
                    d = os.path.join(new_path, item)
                    if os.path.isdir(s):
                        if os.path.exists(d):
                            # Recursively merge files
                            for subitem in os.listdir(s):
                                ss = os.path.join(s, subitem)
                                dd = os.path.join(d, subitem)
                                if not os.path.exists(dd):
                                    shutil.copy2(ss, dd)
                            shutil.rmtree(s)
                        else:
                            shutil.move(s, d)
                    else:
                        if not os.path.exists(d):
                            shutil.move(s, d)
                shutil.rmtree(old_path)

def cleanup():
    # Remove any stray empty numbered folders that don't match the 1-10 sequence
    # Actually, the merges handle most of it.
    pass

if __name__ == "__main__":
    merge_folders()
    print("Merge complete.")
