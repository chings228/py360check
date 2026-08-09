from pathlib import Path

folder_path = Path("scene1")

for file_path in folder_path.iterdir():
    if file_path.is_file():
        print(f"File Name: {file_path.name}")
        print(f"Full Path: {file_path}")