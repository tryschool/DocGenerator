import sys
import json
import re
import os
from odf.opendocument import load
from odf.text import P
from odf.draw import Frame, Image
from weasyprint import HTML
from fpdf import FPDF

def load_odt_file(file_path):
    """Load the ODT file content."""
    odt_file = load(file_path)
    paragraphs = odt_file.getElementsByType(P)
    text_content = ""

    # Handle paragraphs
    for p in paragraphs:
        text_content += str(p) + "<br/>"  # Add HTML line break for new paragraphs

    # Handle images and other graphic elements
    frames = odt_file.getElementsByType(Frame)
    for frame in frames:
        images = frame.getElementsByType(Image)
        for image in images:
            image_url = image.getAttribute("href")
            if not image_url.startswith("http"):
                # Correctly construct the image path
                image_url = os.path.abspath(os.path.join(os.path.dirname(file_path), "Pictures", os.path.basename(image_url)))

            if os.path.exists(image_url):  # Ensure the image exists
                text_content += f'<img src="{image_url}" alt="Image" style="max-width:100%; height:auto;"/><br/>'
            else:
                print(f"Warning: Image not found at {image_url}")

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
            result += block_copy + "<br/>"  # Add line break after each block
        return result

    return pattern.sub(replace_match, text)


def save_to_pdf(content, output_file):
    """Save the processed content as a PDF using FPDF."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Set font for the main text
    pdf.set_font("Arial", size=12)

    # Split content into lines and add them to the PDF
    for line in content.split("<br/>"):
        # Check if the line contains an image tag
        if '<img ' in line:
            # Extract the image URL from the <img> tag
            start = line.find('src="') + 5
            end = line.find('"', start)
            img_url = line[start:end]
            
            if os.path.exists(img_url):
                pdf.image(img_url, x=10, w=pdf.w - 20)  # Add the image with margins
        else:
            pdf.multi_cell(0, 10, line)  # Add line to PDF with wrapping

    pdf.output(output_file)
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
    
    # Replace placeholders
    odt_content = process_placeholders(odt_content, json_data)

    # Process array templates
    odt_content = process_array_template(odt_content, json_data)

    # Save to PDF
    save_to_pdf(odt_content, output_path)


if __name__ == "__main__":
    main()
