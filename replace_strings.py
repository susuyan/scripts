import re
import sys

def load_translations(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        contents = file.read()
        pattern = re.compile(r'"([^"]+)"\s*=\s*"([^"]+)";')
        strings = pattern.findall(contents)
        return dict(strings)

def replace_strings(original_file, translations_file, output_file):
    translations = load_translations(translations_file)
    with open(original_file, 'r', encoding='utf-8') as file:
        contents = file.readlines()

    with open(output_file, 'w', encoding='utf-8') as file:
        for line in contents:
            if '/* Class' in line:
                file.write(line)
                continue
            pattern = re.compile(r'"([^"]+)"\s*=\s*"([^"]+)";')
            match = pattern.search(line)
            if match:
                key = match.group(2)
                value = translations.get(key)
                if value:
                    line = f'"{match.group(1)}" = "{value}";\n'
            file.write(line)

    print(f'Successfully replaced strings in {output_file}.')

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('Usage: python replace_strings.py <path_to_original_file> <path_to_translations_file> <path_to_output_file>')
        sys.exit(1)

    original_file = sys.argv[1]
    translations_file = sys.argv[2]
    output_file = sys.argv[3]

    replace_strings(original_file, translations_file, output_file)
