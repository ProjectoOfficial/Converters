# Format2Format Converters
## List of the currently available converters
- [imgs2pdf](#imgs2pdf): convert a list of images in one pdf
- [obsidian2pdf](#obsidian2pdf): convert your obsidian notes in a pdf (works with images) 

## imgs2pdf
### Overview
The Image to PDF Converter (imgs2pdf) is a Python script that converts a collection of JPEG images into a single PDF file. It utilizes the Python Imaging Library (PIL) for image processing and the PyPDF library for PDF merging.

### Features
- Converts JPEG images to a single PDF file.
- Resizes images to a uniform size.
- Appends multiple PDF files into a single PDF.

### How to Use
1. Clone the repository or download the script.
2. Install the required dependencies: Pillow, pypdf.
    ```
    pip install Pillow pypdf2
    ```
3. Run the script from the command line with the following parameters:
    ```
    python imgs2pdf.py -d /path/to/images -n output_filename
    ```
    - __-d__ or __--images-dir__: Path to the directory containing JPEG images.
    - __-n__ or __--out-file-name__: Name of the output PDF file (without extension)

After execution, the script will generate a PDF file .pdf in the specified directory.

## obsidian2pdf
### Overview
The Obsidian to PDF Converter (obsidian2pdf) is a Python script designed to convert Obsidian Markdown notes, including embedded images, into a PDF file. It uses the markdown2 library for Markdown to HTML conversion, WeasyPrint for HTML to PDF conversion, and BeautifulSoup for HTML parsing.

### Features
- Converts Obsidian Markdown notes to a PDF file.
- Embeds images directly into the PDF.
- Option to specify the main Obsidian vault directory for image search.

### How to Use
1. Clone the repository or download the script.
2. Install the required dependencies: markdown2, WeasyPrint, BeautifulSoup.
    ```
    pip install markdown2 WeasyPrint beautifulsoup4
    ```
3. WeasyPrint needs gtk3 in order to work, thus it is recommended to install it and reboot the machine.
    - Windows: download it [here](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases)
    - Linux: ```sudo apt-get install libgtk-3-dev```
4. Run the script from the command line with the following parameters:
    ```
    python obsidian2pdf.py -np /path/to/obsidian_note.md -op /output/path -mp /main/vault/path
    ```
    - __-np__ or __--obsidian-note-path__: Path to the Obsidian Markdown note.
    - __-op__ or __--output-path__: Path where the PDF will be generated.
    - __-mp__ or __--main-path__: (Optional) Main Obsidian vault directory for image search.

After execution, the script will generate a PDF file .pdf in the specified output folder.

### Note
If the __*main-path*__ parameter is not specified, the script will search for images in the same directory as the Obsidian note.
