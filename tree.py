import os


def write_folder_structure(folder_path, output_file):
    """
    Writes the structure of a folder and its subfolders (recursively) to a text file.

    Args:
        folder_path (str): The root folder path.
        output_file (str): The path to the output text file.
    """
    with open(output_file, "w") as file:
        for root, dirs, files in os.walk(folder_path):
            # Calculate the indentation level based on the folder depth
            level = root.replace(folder_path, "").count(os.sep)
            indent = "    " * level
            # Write the folder name
            file.write(f"{indent}[{os.path.basename(root)}]\n")
            # Write the files in the current folder
            sub_indent = "    " * (level + 1)
            for name in files:
                file.write(f"{sub_indent}{name}\n")


if __name__ == "__main__":
    # Specify the folder path to scan
    folder_path = input("Enter the folder path: ").strip()
    # Specify the output file name
    output_file = input("Enter the output file name (e.g., structure.txt): ").strip()

    if os.path.isdir(folder_path):
        write_folder_structure(folder_path, output_file)
        print(f"Folder structure has been written to {output_file}")
    else:
        print("The specified folder path does not exist.")
