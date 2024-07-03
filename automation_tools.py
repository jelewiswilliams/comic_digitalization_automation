import os
import re
from PIL import Image
from pathlib import Path

class PDFMaker:
    def __init__(self):
        self.status = ""
        self.curr_output_name = ""
        self.total_pdfs_made = 0
        self.total_pdfs_status = ""
        

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

    def batch_pdf(self, input_folder, output_folder):
        for filename in os.listdir(input_folder):
            path = os.path.join(input_folder, filename)
            print(path)
            if Path(path).is_dir():
                output_name = str(filename) + ".pdf"
                output_pdf_path = os.path.join(output_folder, output_name)
                self.curr_output_name = output_name
                self.images_to_pdf(path, output_pdf_path)
                self.total_images_halved += 1

        num_halved_status = f"Successfully created {self.total_images_halved} PDF files."
        self.total_halved_status = num_halved_status
        print(self.total_halved_status)
    
class ImageHalver:
    def __init__(self):
        self.curr_status = ""
        self.curr_output_name = ""
        self.total_images_halved = 0
        self.total_halved_status = ""
        
    def split_image_vertically(self, image_path, output_folder):
        # open the image
        with Image.open(image_path) as img:
            # calculate dimensions of landscape image divided in half vertically
            width, height = img.size
            half_width = width // 2

            print(half_width)
            
            # get boxes for cropping each half
            left_half_box = (0, 0, half_width, height)
            right_half_box = (half_width, 0, width, height)
            
            # crop left and right halves
            left_half = img.crop(left_half_box)
            right_half = img.crop(right_half_box)
            
            # set up filenames for each half
            base_filename = os.path.basename(image_path)
            name, ext = os.path.splitext(base_filename)
            left_half_filename = os.path.join(output_folder, f"{name}_left{ext}")
            right_half_filename = os.path.join(output_folder, f"{name}_right{ext}")
            
            # save the new images
            left_half.save(left_half_filename)
            right_half.save(right_half_filename)
            
    def process_images_in_folder(self, folder_path, output_folder):
        # reset number of images halved if a previous operation was done to prevent misleading
        self.total_images_halved = 0
        
        # create output folder
        os.makedirs(output_folder, exist_ok=True)
        
        # list of all files in the folder
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            
            # check if file is an image (ignore .DS_Store, etc. that may break the splitting function)
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
                self.split_image_vertically(file_path, output_folder)
                curr_status = f"Processed and split image: {filename}"
                self.status = curr_status
                self.total_images_halved += 1
                print(self.status)
                
        num_halved_status = f"Successfully halved {self.total_images_halved} images."
        self.total_halved_status = num_halved_status
        print(self.total_halved_status)