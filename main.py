#!/usr/bin/env python3

import sys
import json
import zipfile
import re
import subprocess
import tempfile
import os
import shutil

def extract_content_xml(odt_path):
    with zipfile.ZipFile(odt_path, 'r') as odt:
        content = odt.read('content.xml').decode('utf-8')
    print("Extracted content.xml from the ODT file.")
    return content

def replace_variables_in_text(text, data):
    # Replace simple variables
    pattern = re.compile(r'{%\s*(\w+)\s*%}')
    def replace_match(match):
        key = match.group(1)
        value = str(data.get(key, ''))
        print(f"Replacing variable '{key}' with '{value}'.")
        return value
    return pattern.sub(replace_match, text)

def process_loops_in_content(content, data):
    loop_pattern = re.compile(r'{%!\s*for\s+(\w+)\s+until\s*%}(.*?){%!\s*end\s*%}', re.DOTALL)
    iteration = 1
    while True:
        match = loop_pattern.search(content)
        if not match:
            break
        array_name = match.group(1)
        loop_block = match.group(2)
        print(f"\nProcessing loop #{iteration}: array '{array_name}'.")
        if array_name in data and isinstance(data[array_name], list):
            replacement = ''
            for index, item in enumerate(data[array_name], start=1):
                print(f"  Iteration {index} with data: {item}")
                temp_block = loop_block
                # Replace variables in temp_block with item data
                temp_block = replace_variables_in_text(temp_block, item)
                replacement += temp_block
            print("Loop replacement content:")
            print(replacement)
            content = content[:match.start()] + replacement + content[match.end():]
        else:
            # Remove the loop block if data is not available
            print(f"Array '{array_name}' not found or is not a list. Removing loop block.")
            content = content[:match.start()] + content[match.end():]
        iteration += 1
    return content

def replace_variables(content, data):
    print("Starting loop processing...")
    # First process loops
    content = process_loops_in_content(content, data)
    print("Loop processing completed.\n")
    print("Starting variable replacement...")
    # Then replace simple variables
    content = replace_variables_in_text(content, data)
    print("Variable replacement completed.")
    return content

def repackage_odt(original_odt_path, new_odt_path, content_xml):
    # Copy the original ODT file to a new ODT file
    with zipfile.ZipFile(original_odt_path, 'r') as zin:
        with zipfile.ZipFile(new_odt_path, 'w') as zout:
            for item in zin.infolist():
                if item.filename != 'content.xml':
                    buffer = zin.read(item.filename)
                    zout.writestr(item, buffer)
            # Write the modified content.xml
            zout.writestr('content.xml', content_xml)
    print(f"Repackaged ODT file saved as '{new_odt_path}'.")

def convert_to_pdf(odt_path, pdf_path):
    # Use LibreOffice in headless mode to convert ODT to PDF
    print(f"Converting '{odt_path}' to PDF...")
    output_dir = os.path.dirname(pdf_path) or '.'
    subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', '--outdir',
                    output_dir, odt_path], check=True)
    # The output PDF will have the same base name as the input ODT file
    odt_base_name = os.path.splitext(os.path.basename(odt_path))[0]
    generated_pdf = os.path.join(output_dir, odt_base_name + '.pdf')
    if os.path.abspath(generated_pdf) != os.path.abspath(pdf_path):
        shutil.move(generated_pdf, pdf_path)
    print(f"PDF saved as '{pdf_path}'.")

def main(template_path, output_pdf_path, json_data):
    print("Loading data...")
    data = json.loads(json_data)
    print("Data loaded:")
    print(json.dumps(data, indent=2))
    print("\nExtracting content.xml...")
    content = extract_content_xml(template_path)
    print("Replacing variables and processing loops...")
    content = replace_variables(content, data)
    # Create a temporary directory to store the modified ODT
    with tempfile.TemporaryDirectory() as tmpdirname:
        modified_odt_path = os.path.join(tmpdirname, 'modified.odt')
        print("\nRepackaging the ODT file with modified content...")
        repackage_odt(template_path, modified_odt_path, content)
        print("\nConverting the modified ODT file to PDF...")
        convert_to_pdf(modified_odt_path, output_pdf_path)
    print("\nProcessing completed successfully.")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 main.py template.odt output.pdf '{\"json\":\"data\"}'")
        sys.exit(1)
    template_path = sys.argv[1]
    output_pdf_path = sys.argv[2]
    json_data = sys.argv[3]
    main(template_path, output_pdf_path, json_data)
