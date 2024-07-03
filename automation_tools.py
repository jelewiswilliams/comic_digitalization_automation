import os
import re
from PIL import Image
from pathlib import Path

class PDFMaker:
    def __init__(self):
        self.curr_status = ""
        self.total_status = ""
        self.curr_output_name = ""
        self.total_operations = 0
        

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
            self.curr_status = f"PDF created successfully: {self.curr_output_name}"
            print(self.curr_status)
        else:
            status = "No images found in the folder."
            print(self.curr_status)
            
    # for going through a single folder, setting the proper output PDF name, and passing it through images_to_pdf
    def convert_to_pdf(self, input_folder, output_folder, output_name):
        if Path(input_folder).is_dir():
            if output_name is None:
                output_name = str(input_folder.split("/")[-1]) + ".pdf"
                
            else:
                output_name = str(output_name) + ".pdf"
            
            output_pdf_path = os.path.join(output_folder, output_name)
            self.curr_output_name = output_name
            self.images_to_pdf(input_folder, output_pdf_path)
            
    # same as above, but process multiple folders in a directory into PDFs
    def batch_pdf(self, input_folder, output_folder):
        self.total_operations = 0
        for filename in os.listdir(input_folder):
            path = os.path.join(input_folder, filename)
            print("\nCurrent path:", path)
            if Path(path).is_dir():
                output_name = str(filename) + ".pdf"
                output_pdf_path = os.path.join(output_folder, output_name)
                self.curr_output_name = output_name
                
                # process images into PDF
                self.images_to_pdf(path, output_pdf_path)
                
                # update total number of PDFs made
                self.total_operations += 1

        self.total_status = f"Successfully created {self.total_operations} PDF files."
        print("\n", self.total_status, "\n________________")
    
class ImageHalver:
    def __init__(self):
        # self.curr_status = ""
        self.total_status = ""
        self.curr_output_name = ""
        self.total_operations = 0
        
    def split_image_vertically(self, image_path, output_folder):
        # open the image
        with Image.open(image_path) as img:
            # calculate dimensions of landscape image divided in half vertically
            width, height = img.size
            
            # if the image is not already in landscape position, rotate it
            if width < height:
                img = img.transpose(Image.ROTATE_90)
                width, height = img.size
                
            half_width = width // 2
            # print(img.size)
            # print(half_width)
            
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
        self.total_operations = 0
        
        # create output folder
        os.makedirs(output_folder, exist_ok=True)
        
        # list of all files in the folder
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            
            # check if file is an image (ignore .DS_Store, etc. that may break the splitting function)
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
                # split images
                self.split_image_vertically(file_path, output_folder)  
                
                # print status
                self.curr_status = f"Processed and split image: {filename}"
                print("\n", self.curr_status)
                
                # update total number of halved images
                self.total_operations += 1

        # print total number of halved images      
        self.total_status = f"Successfully halved {self.total_operations} images."
        print("\n", self.total_status, "\n________________")