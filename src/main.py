from audio_separator.separator import Separator
import os, re, argparse

# ANSI escape sequences for colored output
BLUE = "\033[94m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

def print_info(message):
    """
    Print an info message in blue color.

    Args:
        message (str): The message to print.
    """

    print(f"{BLUE}[INFO] {RESET}{message}")

def print_warn(message):
    """
    Print a warning message in yellow color.

    Args:
        message (str): The message to print.
    """

    print(f"{YELLOW}[WARN] {RESET}{message}")

def print_error(message):
    """
    Print an error message in red color.

    Args:
        message (str): The message to print.
    """

    print(f"{RED}[ERROR] {RESET}{message}")

def get_exclusions(exclusions_file="exclusions.txt"):
    """
    Load exclusions from a file.

    Args:
        exclusions_file (str): The path to the exclusions file. Defaults to 'exclusions.txt'.
    
    Returns:
        list: A list of file names to exclude from processing.
    """

    if os.path.exists(exclusions_file):
        with open(exclusions_file, 'r', encoding='utf-8') as file:
            exclusions = [line.strip() for line in file.readlines()]

        file.close()
        return exclusions
    return []

def check_already_separated(folder_path):
    """Check if the audio files in the specified folder have already been separated.

    Args:
        folder_path (str): The path to the folder containing audio files.

    Returns:
        bool: True if the audio files have already been separated, False otherwise.
    """
    folder = os.path.basename(folder_path)

    matching_files = 0

    for file in os.listdir(folder_path):
        # If there's any VOC or INSTR file, some separation has already been done
        if re.search(r"\[(?:VOC|INSTR)\]\.(?:mp3|wav|ogg|m4a)$", file):
            matching_files += 1

        if file == f"{folder}.txt":
            with open(os.path.join(folder_path, file), 'r', encoding='utf-8') as txt_file:
                content = txt_file.read()
                if re.search(rf"#VOCALS: ?.* \[VOC\]\.(?:mp3|wav|ogg|m4a)", content) and \
                re.search(rf"#INSTRUMENTAL: ?.* \[INSTR\]\.(?:mp3|wav|ogg|m4a)", content):
                    matching_files += 1

            txt_file.close()

    return matching_files == 3

def separate_audio_files(songs_path, exclusions=[], force=False):
    """
    Separate audio files in the specified directory, excluding those in the exclusions list.

    Args:
        separator (Separator): An instance of the Separator class for audio separation.
        songs_path (str): The path to the directory containing audio files.
        exclusions (list): A list of file names to exclude from processing. Defaults to an empty list.
        force (bool): If True, force re-separation of already processed files. Defaults to False.
    """

    folders_dir = os.listdir(songs_path)
    folders_count = len(folders_dir)
    if not folders_dir:
        print_warn(f"No directories found in {songs_path}. Exiting...")
        return
    print_info(f"Found {len(folders_dir)} directories in {songs_path}. Starting separation...")

    curr = 0
    for folder in folders_dir:
        curr += 1
        if folder in exclusions:
            print_info(f"Skipping excluded folder: {folder} ({curr}/{folders_count})")
            continue

        folder_path = os.path.join(songs_path, folder)

        if not force and check_already_separated(folder_path):
            print_info(f"Skipping already separated folder: {folder} ({curr}/{folders_count})")
            continue

        if os.path.isdir(folder_path):
            print_info(f"Processing folder: {folder} ({curr}/{folders_count})")

            mp3_name = os.path.join(folder_path, f"{folder}.mp3")
            wav_name = os.path.join(folder_path, f"{folder}.wav")
            ogg_name = os.path.join(folder_path, f"{folder}.ogg")
            m4a_name = os.path.join(folder_path, f"{folder}.m4a")
            name = ""
            
            if os.path.exists(mp3_name):
                name = mp3_name
            elif os.path.exists(wav_name):
                name = wav_name
            elif os.path.exists(ogg_name):
                name = ogg_name
            elif os.path.exists(m4a_name):
                name = m4a_name
            else:
                print_warn(f"No audio file found in {folder}. Skipping...")
                continue

            output = {
                "Vocals": f"{folder} [VOC]",
                "Instrumental": f"{folder} [INSTR]"
            }

            # We need to redefine the separator everytime just to specify the output directory
            separator = Separator(output_dir=folder_path)
            separator.load_model()
            separator.separate(name, output)

            # Add the newly created files to the .txt file only if they don't exist in the text file
            txt_file_path = os.path.join(folder_path, f"{folder}.txt")
            lines = []
            if os.path.exists(txt_file_path):
                with open(txt_file_path, 'r', encoding='utf-8') as txt_file:
                    lines = txt_file.readlines()

                txt_file.close()

            voc_line = f"#VOCALS: {folder} [VOC].wav\n"
            instr_line = f"#INSTRUMENTAL: {folder} [INSTR].wav\n"

            if voc_line in lines and instr_line in lines:
                continue

            insert_index = len(lines)
            for i, line in enumerate(lines):
                if not line.startswith("#"):
                    insert_index = i
                    break

            if not voc_line in lines:
                lines.insert(insert_index, voc_line)
                insert_index += 1
            if not instr_line in lines:
                lines.insert(insert_index, instr_line)

            with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
                txt_file.writelines(lines)

            txt_file.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audio file separator script.")
    parser.add_argument("-f", "--force", action="store_true", help="Force re-separation of already processed files.")
    parser.add_argument("input", nargs="?", type=str, help="Specify the songs directory containing audio files.")
    args = parser.parse_args()

    force = args.force
    if not args.input:
        print_warn("No input directory specified.")
        print_warn("Usage: python main.py [--force] <songs_directory>")
        exit(1)
    else:
        songs_path = args.input
        if not os.path.isabs(songs_path):
            songs_path = os.path.abspath(songs_path)
    
    exclusions = get_exclusions()

    if not os.path.exists(songs_path):
        print_error(f"Directory {songs_path} does not exist.")
        exit(1)
    else:
        separate_audio_files(songs_path, exclusions, force)