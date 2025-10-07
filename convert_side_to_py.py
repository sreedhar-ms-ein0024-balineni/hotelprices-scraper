
import json
import sys
import os
from typing import List
from side_command_map import COMMAND_MAP, find_by

HEADER = '''import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

def main():
    options = Options()
    options.headless = True  
    options.add_argument('--disable-gpu')
    options.add_argument('--headless')
    options.add_argument("--width=1920")
    options.add_argument("--height=1080")
    options.add_argument("--start-maximized")
    options.set_preference(
        "general.useragent.override",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
    )
    driver = webdriver.Firefox(options=options)
    try:
'''

FOOTER = '''    finally:
        driver.quit()

if __name__ == '__main__':
    main()
'''

def indent(code: str, level: int = 2) -> str:
    return '\n'.join((' ' * level * 2) + line if line.strip() else '' for line in code.splitlines())

def step_to_python(step: dict) -> str:
    command = step.get('command')
    target = step.get('target', '')
    value = step.get('value', '')
    func = COMMAND_MAP.get(command)
    try:
        if func:
            return func(target, value)
        else:
            return f"# Unsupported command: {command}"
    except Exception as e:
        return f"# Error in command {command}: {e}"

def convert_side_to_py(side_path: str, py_path: str):
    with open(side_path, 'r') as f:
        side = json.load(f)
    tests = side.get('tests', [])
    suites = side.get('suites', [])
    base_url = side.get('url', '')
    code_lines: List[str] = []
    # Pass base_url to global scope for open command
    if not base_url:
        base_url = ''
    for suite in suites:
        for test_id in suite.get('tests', []):
            test = next((t for t in tests if t['id'] == test_id), None)
            if not test:
                continue
            for step in test.get('commands', []):
                code_lines.append(step_to_python(step))
    if not code_lines:
        print('No steps found in .side file.')
        return
    import re
    def fix_line(line):
        # Fix echo variable interpolation
        if line.strip().startswith("print('") and "${" in line:
            # Replace print('${var}') with print(var)
            return re.sub(r"print\('\$\{(\w+)}'\)", r"print(\1)", line)
        # Replace any find_by(...) call with find_by("""...""")
        line = re.sub(r'find_by\((?:[\'"])(.*?)(?:[\'"])\)', r'find_by("""\1""")', line)
        # Replace driver.find_element(*find_by(...)) with wait_find(driver, ...)
        line = re.sub(r'driver\.find_element\(\*find_by\(([^)]*)\)\)', r'wait_find(driver, \1)', line)
        return line

    # Detect indentation style from HEADER (look for the line with 'try:')
    header_lines = HEADER.splitlines()
    try_indent = ''
    for line in header_lines:
        if 'try:' in line:
            try_indent = line[:line.index('try:')]
            break
    # The indent for code inside try block is one level deeper
    if '\t' in try_indent:
        block_indent = try_indent + '\t'
    else:
        block_indent = try_indent + '    '

    def write_block(f, lines):
        for line in lines:
            for subline in line.split('\n'):
                if subline.strip() != '':
                    f.write(f'{block_indent}{subline}\n')
                else:
                    f.write(f'{block_indent}\n')

    with open(py_path, 'w') as f:
        # Write imports and find_by, wait_find helpers first
        header_lines = HEADER.split('\n')
        import_lines = []
        for line in header_lines:
            if line.strip().startswith('def main():'):
                break
            import_lines.append(line)
        f.write('\n'.join(import_lines) + '\n')
        # Write find_by and wait_find helpers before main()
        f.write('''\ndef find_by(target):
    if target.startswith('css='):
        return (By.CSS_SELECTOR, target[4:])
    elif target.startswith('id='):
        return (By.ID, target[3:])
    elif target.startswith('xpath='):
        return (By.XPATH, target[6:])
    elif target.startswith('name='):
        return (By.NAME, target[5:])
    elif target.startswith('linkText='):
        return (By.LINK_TEXT, target[9:])
    elif target.startswith('partialLinkText='):
        return (By.PARTIAL_LINK_TEXT, target[17:])
    else:
        return (By.CSS_SELECTOR, target)

def wait_find(driver, selector, timeout=30):
    from selenium.webdriver.support.ui import WebDriverWait
    return WebDriverWait(driver, timeout).until(lambda d: d.find_element(*find_by(selector)))
''')
        # Write the rest of the header (main function definition and body)
        main_start = False
        for line in header_lines:
            if line.strip().startswith('def main():'):
                main_start = True
            if main_start:
                f.write(line + '\n')
        generated_lines = []
        generated_lines.append(f'base_url = "{base_url}"')
        generated_lines.append('# --- BEGIN GENERATED CODE ---')
        for line in code_lines:
            generated_lines.append(fix_line(line))
        generated_lines.append('# --- END GENERATED CODE ---')
        # Write each generated line and all sub-lines with correct indentation
        write_block(f, generated_lines)
        f.write(FOOTER)
    print(f'Python file written to {py_path}')

def usage():
    print('Usage: python convert_side_to_py.py <input.side>')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
        sys.exit(1)
    side_path = sys.argv[1]
    if not os.path.isabs(side_path):
        side_path = os.path.join('/Users/krishnakalangi', side_path)
    if not side_path.endswith('.side'):
        print('Input file must have .side extension')
        sys.exit(1)
    py_path = os.path.splitext(side_path)[0] + '.py'
    convert_side_to_py(side_path, py_path)
