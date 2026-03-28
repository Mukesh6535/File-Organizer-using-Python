import streamlit as st
import os
import shutil
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
    Returns a dictionary of folder names and the number of files moved there.
    """
    target_path = Path(target_dir)

    if not target_path.exists() or not target_path.is_dir():
        return None, f"Error: The directory '{target_dir}' does not exist or is not a valid directory."

    extension_to_folder = {}
    for folder, extensions in EXTENSION_MAPPING.items():
        for ext in extensions:
            extension_to_folder[ext.lower()] = folder

    moved_stats = {folder: 0 for folder in EXTENSION_MAPPING.keys()}
    moved_stats["Others"] = 0
    total_moved = 0

    for item in target_path.iterdir():
        if item.is_file():
            file_extension = item.suffix.lower()

            # Skip the script itself and the streamlit entry point if in the same folder
            if item.name in [os.path.basename(__file__), "organize.py"]:
                continue

            folder_name = extension_to_folder.get(file_extension, "Others")
            dest_folder = target_path / folder_name
            dest_folder.mkdir(exist_ok=True)

            destination_path = dest_folder / item.name
            
            counter = 1
            while destination_path.exists():
                name_without_ext = item.stem
                destination_path = dest_folder / f"{name_without_ext}_{counter}{item.suffix}"
                counter += 1

            try:
                shutil.move(str(item), str(destination_path))
                moved_stats[folder_name] += 1
                total_moved += 1
            except Exception as e:
                # Silently skip errors on specific files like permission denied
                pass
            
    # Clean up empty stats
    moved_stats = {k: v for k, v in moved_stats.items() if v > 0}
            
    return moved_stats, total_moved

def main():
    st.set_page_config(page_title="File Organizer", page_icon="📁", layout="centered")

    st.title("📁 File Organizer")
    st.markdown("Easily organize your messy directories by file type with one click!")

    # Input for target directory
    target_directory = st.text_input("Enter the absolute path to the directory you want to organize:", placeholder="e.g. C:\\Users\\Name\\Downloads")

    if st.button("Organize Directory", type="primary"):
        if not target_directory.strip():
            st.warning("Please enter a valid directory path.")
        else:
            with st.spinner("Organizing files..."):
                stats, result = organize_files(target_directory)
                
            if stats is None:
                st.error(result)
            else:
                if result == 0:
                    st.info("No loose files found to organize in the given directory.")
                else:
                    st.success(f"Success! Organized {result} files.")
                    
                    st.subheader("Summary")
                    cols = st.columns(3)
                    col_idx = 0
                    
                    for folder, count in stats.items():
                        cols[col_idx % 3].metric(label=folder, value=count)
                        col_idx += 1
                    
                    st.balloons()

if __name__ == "__main__":
    main()
