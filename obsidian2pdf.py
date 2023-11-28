import re
import os
import base64
import argparse

import markdown2
from weasyprint import HTML
from bs4 import BeautifulSoup

def convert_obsidian_to_pdf(args):
    # Read the contents of md file
    with open(args.obsidian_note_path, 'r', encoding='utf-8') as file:
        obsidian_content = file.read()

    # Convert md file from Markdown to HTML
    html_content = markdown2.markdown(obsidian_content)

    # Extract and embed images directly into HTML document
    soup = BeautifulSoup(html_content, 'html.parser')
    p_tags = soup.find_all('p')

    for p_tag in p_tags:
        # Look for <p> tags containing images
        img_match = re.search(r'!\[\[(.*?)\]\]', str(p_tag))
        if img_match:
            img_src = img_match.group(1)
            
            images_base_path = args.main_path if args.main_path != "" else os.path.dirname(args.obsidian_note_path)

            # Search for the image in the subdirectories of the main folder
            image_path = find_image_path(images_base_path, img_src)

            if image_path:
                # Read the content of the image and convert it to base64 format
                with open(image_path, 'rb') as img_file:
                    img_data = base64.b64encode(img_file.read()).decode('utf-8')

                # Create a new tag for the embedded image
                img_tag = soup.new_tag('img', src=f'data:image/png;base64,{img_data}', style='width:100%')
                p_tag.replace_with(img_tag)

    # Save the HTML to a temporary file
    temp_html_path = 'temp_obsidian_note.html'
    with open(temp_html_path, 'w', encoding='utf-8') as temp_file:
        temp_file.write(str(soup))

    # Convert HTML to PDF
    HTML(string=str(soup)).write_pdf(args.output_pdf_path)

    # Delete the temporary HTML file
    os.remove(temp_html_path)

def find_image_path(base_path, img_filename):
    # Look for the image in the subdirectories of base_path
    for subdir, _, files in os.walk(base_path):
        if img_filename in files:
            return os.path.join(subdir, img_filename)
    return None

def sanity_check(args):
    assert args.obsidian_note_path != "", "obsidian2pdf: please specify the path reaching the .md note to be converted"
    assert args.output_path != "", "obsidian2pdf: please specify where you want to store the pdf"
    
    if args.main_path == "":
        print(f"obsidian2pdf: Warning! main_path is not specified, thus images search will be done here: {os.path.dirname(args.obsidian_note_path)}")
        
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-np", "--obsidian-note-path", type=str, default="", help="the path pointing the obsidian note to be converted")
    parser.add_argument("-op", "--output-path", type=str, default="", help="the output path where the pdf will be generated")
    parser.add_argument("-mp", "--main-path", type=str, default="", help="the main obsidian vault directory which will be used to recover the note attachments (i.e. images)")
    parser.add_argument("--parent", action="store_true", help="if True images search will be done in the obsidian-note-path parent directory")
    args = parser.parse_args()
    
    sanity_check(args)
    
    args.output_pdf_name = os.path.basename(args.obsidian_note_path).split(".")[0]
    args.output_pdf_path = os.path.join(args.output_path, args.output_pdf_name + ".pdf")

    convert_obsidian_to_pdf(args)

    print(f"obsidian2pdf: note conversion has been completed successfully! The output file is located at: {args.output_pdf_path}")
