from PIL import Image
from pypdf import PdfMerger
import os
import argparse

def main(args):
    images = list()
    size = None
    for f in os.listdir(args.images_dir):
        if os.path.isfile(os.path.join(args.images_dir, f)) and f.endswith(".jpg"):
            image = Image.open(os.path.join(args.images_dir, f))
            if size is None:
                size = image.size
                
            if image.size != size:
                image = image.resize(size)
            
            images.append(image)

    if not args.out_file_name.endswith(".pdf"):
        args.out_file_name += ".pdf"

    if not os.path.exists(os.path.join(args.images_dir, args.out_file_name)):
        images[0].save(
            os.path.join(args.images_dir, args.out_file_name), "PDF", resolution=100.0, save_all=True, append_images=images[1:]
        )

    pdfs = list()
    for f in os.listdir(args.images_dir):
        if os.path.isfile(os.path.join(args.images_dir, f)) and f.endswith(".pdf"):        
            pdfs.append(f)

    merger = PdfMerger()

    for pdf in pdfs:
        merger.append(os.path.join(args.images_dir, pdf))

    merger.write(os.path.join(args.images_dir, args.out_file_name))
    merger.close()
    
    
def sanity_check(args):
    assert args.images_dir != "", "imgs2pdf: please specify your images directory path"
    assert args.out_file_name != "", "imgs2pdf: please specify the name of the resulting output pdf file"
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--images-dir", type=str, default="", help="the path where the images are stored")
    parser.add_argument("-n", "--out-file-name", type=str, default="", help="the name of the output pdf file (e.g. foo, but not foo.pdf)")
    args = parser.parse_args()
    
    sanity_check(args)
    main(args)
    
    print(f"imgs2pdf: images conversion has been completed successfully! The pdf file is located at: {os.path.join(args.images_dir, args.out_file_name)}")