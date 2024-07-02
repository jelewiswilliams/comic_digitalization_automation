import os
import re
from PIL import Image
from pathlib import Path

class PDFMaker:
    def __init__(self):
        self.status = ""
        self.curr_output_name = ""
        

    # for properly sorting image files with numeric filenames
    # via https://stackoverflow.com/questions/2669059/how-to-sort-alpha-numeric-set-in-python
    def sorted_nicely(self, list):
        convert = lambda text: int(text) if text.isdigit() else text.lower()
        alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
        return sorted(list, key=alphanum_key)

    # main PDF creation script
    def images_to_pdf(self, input_folder, output_pdf_path) -> None:
        """
        Takes a list of image files in a folder and consolidates them into a PDF.
        Assumes file names are numerical and in order.
        """
        
        # list of all images files in the folder (ignores other items, such as ".DS_Store" files)
        image_files = [f for f in os.listdir(input_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif'))]

        # sort files to ensure correct order
        image_files = self.sorted_nicely(image_files)
        
        # list to hold all images
        images = []
        
        # open each image and append it to the list as a PIL image
        for filename in image_files:
            file_path = os.path.join(input_folder, filename)
            img = Image.open(file_path)
            img = img.convert('RGB')  # Ensure all images are in RGB mode
            images.append(img)
        
        # consolidates all images as a single PDF file
        if images:
            images[0].save(output_pdf_path, save_all=True, append_images=images[1:])
            self.status = f"PDF created successfully: {self.curr_output_name}"
            print(self.status)
        else:
            self.status = "No images found in the folder."
            print(self.status)
            
            
    def convert_to_pdf(self, input_folder, output_folder, output_name):
        if Path(input_folder).is_dir():
            if output_name is None:
                output_name = str(input_folder.split("/")[-1]) + ".pdf"
                
            else:
                output_name = str(output_name) + ".pdf"
            
            output_pdf_path = os.path.join(output_folder, output_name)
            self.curr_output_name = output_name
            self.images_to_pdf(input_folder, output_pdf_path)

    # def batch_pdf(self, input_folder, output_folder):
    #     for filename in os.listdir(input_folder):
    #         path = os.path.join(input_folder, filename)
    #         print(path)
    #         if Path(path).is_dir():
    #             output_name = str(filename) + ".pdf"
    #             output_pdf_path = os.path.join(output_folder, output_name)
    #             self.curr_output_name = output_name
    #             self.images_to_pdf(path, output_pdf_path)