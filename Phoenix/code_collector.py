import os


def collect_code(directory):
    collected_code = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py") and file != "code_collector.py":
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                collected_code.append(f"# File: {file_path}\n\n{content}\n\n")
    return collected_code


def write_collected_code(collected_code, output_file):
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(collected_code))


if __name__ == "__main__":
    current_directory = os.path.dirname(os.path.abspath(__file__))
    collected_code = collect_code(current_directory)
    output_file = os.path.join(current_directory, "collected_code.py")
    write_collected_code(collected_code, output_file)
    print(f"Code collected and written to {output_file}")
