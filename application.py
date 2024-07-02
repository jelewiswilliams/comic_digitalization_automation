import customtkinter as ctk
from customtkinter.windows import CTkToplevel
from tkinter import NONE, BOTH, X, TOP, BOTTOM, LEFT, RIGHT, RAISED
   
# main window     
class root(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # GUI window config
        self.title("Jeff's Comic Digitalization Labs")
        self.geometry("640x640")
        self.resizable(width=False, height=False)

        self.opts_tabview = option_tabs(master=self, width=600, height=600)
        self.opts_tabview.grid(row=0, column=0, padx=20, pady=20)
        self.opts_tabview.grid_propagate(False)

# font configurations
font_family = "Helvetica"

header_font_config = (font_family, 18, "bold")
body_font_config = (font_family, 14, "italic")
button_font_config = (font_family, 16)
tab_font_config = (font_family, 14, "bold")

# tabs
class option_tabs(ctk.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        # create tabs
        self.pdf_tab = self.add("PDF Maker")
        self.splitter_tab = self.add("Scan Splitter")
        
        # PDF Maker pane
        self.pdf_maker_header = ctk.CTkLabel(master=self.pdf_tab,
                                  text="Grab a folder with organized, numbered scans and create a PDF",
                                  font=header_font_config)
        self.pdf_maker_header.grid(row=0, column=0, padx=20, pady=10)
        
        self.grab_folder_pdf = ctk.CTkButton(master=self.pdf_tab, 
                                             text="Get folder", 
                                             command=open_folder,
                                             font=button_font_config)
        self.grab_folder_pdf.grid(row=1, column=0, padx=12, pady=6)
        
        # Image Splitter pane
        self.scan_splitter_header = ctk.CTkLabel(master=self.splitter_tab,
                                  text="Grab a folder with scans and split them vertically",
                                  font=header_font_config)
        
        self.scan_splitter_info = ctk.CTkLabel(master=self.splitter_tab,
                                  text="This assumes scans are of sheets of US Letter paper divided into two pages, like a small comic book.",
                                  font=body_font_config,
                                  wraplength=600)
        
        self.scan_splitter_header.grid(row=0, column=0, padx=20, pady=10)
        self.scan_splitter_info.grid(row=1, column=0, padx=20, pady=10)
        

# functions
def open_folder():
    folder_path = ctk.filedialog.askopenfile(mode = "r",
                                          title = "Select a folder")

# run window
root = root()
root.mainloop()