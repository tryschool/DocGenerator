import sys
import json
import re
from odf.opendocument import load
from odf.text import P
from weasyprint import HTML


def load_odt_file(file_path):
    """Load the ODT file content."""
    odt_file = load(file_path)
    # Assuming text content is in <text:p> elements
    paragraphs = odt_file.getElementsByType(P)
    text_content = ""
    for p in paragraphs:
        text_content += str(p)
    return text_content


def process_placeholders(text, data):
    """Replace single placeholders like {% firstname %} in the text."""
    for key, value in data.items():
        if not isinstance(value, list):  # Process non-array data
            text = text.replace(f"{{% {key} %}}", str(value))
    return text


def process_array_template(text, data):
    """Process array-like structures such as period_array."""
    pattern = re.compile(r"{%! for (\w+) until %}(.*?){%! end %}", re.DOTALL)
    
    def replace_match(match):
        array_name = match.group(1)  # e.g., period_array
        template_block = match.group(2)  # Template inside the loop
        array_data = data.get(array_name, [])
        result = ""
        for item in array_data:
            # Replace placeholders inside the template_block
            block_copy = template_block
            for key, value in item.items():
                block_copy = block_copy.replace(f"{{% {key} %}}", str(value))
            result += block_copy
        return result

    return pattern.sub(replace_match, text)


def save_to_pdf(content, output_file):
    """Save the processed content as a PDF."""
    html_content = f"<html><body>{content}</body></html>"  # Wrap content in HTML
    HTML(string=html_content).write_pdf(output_file)
    print(f"PDF saved to {output_file}")


def main():
    if len(sys.argv) != 4:
        print("Usage: python3 main.py <template.odt> <output.pdf> <json_data>")
        return
    
    template_path = sys.argv[1]
    output_path = sys.argv[2]
    json_data = json.loads(sys.argv[3])

    # Load ODT content
    odt_content = load_odt_file(template_path)
    print("Loaded ODT content:")
    print(odt_content)

    # Replace single placeholders
    odt_content = process_placeholders(odt_content, json_data)
    print("After replacing variables:")
    print(odt_content)

    # Replace array placeholders
    odt_content = process_array_template(odt_content, json_data)
    print("After processing array template:")
    print(odt_content)

    # Save to PDF
    save_to_pdf(odt_content, output_path)


if __name__ == "__main__":
    main()
