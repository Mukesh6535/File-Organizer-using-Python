import os
import shutil
import argparse
from pathlib import Path

# Mapping of folder names to their respective file extensions
EXTENSION_MAPPING = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".tiff"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".xls", ".xlsx", ".ppt", ".pptx", ".csv"],
    "Audio": [".mp3", ".wav", ".aac", ".flac", ".ogg"],
    "Video": [".mp4", ".avi", ".mov", ".mkv", ".wmv", ".flv"],
    "Archives": [".zip", ".rar", ".tar", ".gz", ".7z"],
    "Executables": [".exe", ".msi", ".bat", ".cmd", ".sh"],
    "Code": [".py", ".html", ".css", ".js", ".cpp", ".c", ".java", ".json", ".xml", ".md"],
}

def organize_files(target_dir):
    """
    Organize files in the specified directory based on their extensions.
    """
    target_path = Path(target_dir)

    if not target_path.exists() or not target_path.is_dir():
        print(f"Error: The directory '{target_dir}' does not exist or is not a typical directory.")
        return

    print(f"Organizing files in: {target_path.resolve()}")
    
    # Reverse mapping for quick lookup: extension -> folder name
    # Ensure extensions are lowercase for case-insensitive matching
    extension_to_folder = {}
    for folder, extensions in EXTENSION_MAPPING.items():
        for ext in extensions:
            extension_to_folder[ext.lower()] = folder

    moved_count = 0

    # Iterate through all items in the target directory
    for item in target_path.iterdir():
        if item.is_file():
            # Get the file extension and make it lowercase
            file_extension = item.suffix.lower()

            # Skip the script itself if ran from within the same directory
            if item.name == os.path.basename(__file__):
                continue

            # Determine the destination folder
            folder_name = extension_to_folder.get(file_extension, "Others")
            dest_folder = target_path / folder_name

            # Create the destination folder if it doesn't exist
            dest_folder.mkdir(exist_ok=True)

            # Move the file
            destination_path = dest_folder / item.name
            
            # Handle naming conflicts by appending a number if file already exists
            counter = 1
            while destination_path.exists():
                name_without_ext = item.stem
                destination_path = dest_folder / f"{name_without_ext}_{counter}{item.suffix}"
                counter += 1

            shutil.move(str(item), str(destination_path))
            print(f"Moved: '{item.name}' -> '{folder_name}/'")
            moved_count += 1
            
    print(f"\nOrganization complete! Moved {moved_count} files.")

def main():
    parser = argparse.ArgumentParser(description="Organize files in a directory by their extensions.")
    parser.add_argument(
        "directory", 
        nargs="?", 
        default=".", 
        help="The directory to organize (defaults to the current directory)"
    )
    args = parser.parse_args()

    organize_files(args.directory)

if __name__ == "__main__":
    main()
