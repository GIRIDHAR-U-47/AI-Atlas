import os
import shutil
import re

base_data = r'd:\AI-Atlas\web-app\data'

def clean_name(name):
    # Remove leading number prefix for comparison (e.g. "01-", "02-")
    return re.sub(r'^\d+-', '', name).lower()

def resolve_pillar_dupes(pillar_dir):
    full_path = os.path.join(base_data, pillar_dir)
    if not os.path.isdir(full_path):
        return

    subdirs = os.listdir(full_path)
    # Group by cleaned name
    groups = {}
    for sub in subdirs:
        if os.path.isdir(os.path.join(full_path, sub)):
            key = clean_name(sub)
            if key not in groups:
                groups[key] = []
            groups[key].append(sub)

    for key, variants in groups.items():
        if len(variants) > 1:
            # Sort variants by length (pick the most descriptive) or if one matches the hierarchy I just set
            # Let's target the one that should win.
            # I'll pick the one with the lowest numeric prefix if it exists, but actually it's better to pick the longest name usually.
            variants = sorted(variants, key=len, reverse=True)
            target_name = variants[0]
            target_path = os.path.join(full_path, target_name)
            
            for other in variants[1:]:
                other_path = os.path.join(full_path, other)
                print(f"  In {pillar_dir}: Merging sub-dir {other} into {target_name}")
                for item in os.listdir(other_path):
                    s = os.path.join(other_path, item)
                    d = os.path.join(target_path, item)
                    if not os.path.exists(d):
                        shutil.move(s, d)
                    else:
                        # If conflict, just trash the empty placeholder
                        if os.path.getsize(s) < 100: # trash placeholders
                             pass
                shutil.rmtree(other_path)

if __name__ == "__main__":
    pillars = os.listdir(base_data)
    for p in pillars:
        resolve_pillar_dupes(p)
    print("Sub-folder deduplication complete.")
