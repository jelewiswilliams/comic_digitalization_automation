import customtkinter as ctk
from customtkinter.windows import CTkToplevel
from tkinter import NONE, BOTH, X, TOP, BOTTOM, LEFT, RIGHT, RAISED
import os
from automation_tools import PDFMaker

# font configurations
font_family = "Helvetica"

header_font_config = (font_family, 26, "bold")
body_font_config = (font_family, 14, "italic")
button_font_config = (font_family, 16)
exec_button_font_config = (font_family, 20, "bold")
tab_font_config = (font_family, 14, "bold")

pdf_maker = PDFMaker()
   
# main window     
class root(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # GUI window config
        self.title("Jeff's Comic Digitalization Labs")

        self.resizable(width=False, height=False)
        self.opts_tabview = option_tabs(master=self, width=600, height=600)
        self.opts_tabview.grid(row=0, column=0, padx=20, pady=20)
        self.opts_tabview.grid_propagate(False)
    
# tabs
class option_tabs(ctk.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        # create tabs
        self.pdf_tab = self.add("PDF Maker")
        self.splitter_tab = self.add("Scan Splitter")

        self.target_folder_path = ctk.StringVar()
        self.target_folder_path.set(None)
        self.dest_folder_path = ctk.StringVar()
        self.dest_folder_path.set(None)
        self.status = ctk.StringVar()
        self.status.set(None)
        self.multiple_folders = False
        
        # PDF Maker pane
        # header
        header_txt = "Create PDF from folder(s) containing numbered image files"
        
        self.pdf_maker_header = ctk.CTkLabel(master=self.pdf_tab, text=header_txt, font=header_font_config, wraplength=580)
        self.pdf_maker_header.grid(row=0, column=0, padx=20, pady=(20, 0), sticky="nsew")
        
        self.pdf_tab.grid_rowconfigure(6, weight=1)
        self.pdf_tab.grid_columnconfigure((0, 0), weight=1)
        
        # multiple folders switch
        self.folder_switch_pane = ctk.CTkFrame(master=self.pdf_tab, height=60, fg_color="gray11")
        self.folder_switch_pane.grid(row=1, column=0, columnspan=2, padx=1, pady=10, sticky="ew")
        self.folder_switch_pane.grid_rowconfigure(0, weight=1)
        self.folder_switch_pane.grid_columnconfigure((0, 1), weight=1)
        self.folder_switch_pane.grid_propagate(False)
        # multiple folders switch
        self.folder_switch_default = ctk.BooleanVar(value=False)
        self.folder_switch = ctk.CTkSwitch(master=self.folder_switch_pane, text="Process multiple scan folders", command=self.set_multiple_pdfs, font=button_font_config,
                                            variable=self.folder_switch_default, onvalue=True, offvalue=False)
        self.folder_switch.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        # target path box
        self.target_path_pane = ctk.CTkFrame(master=self.pdf_tab, height=75, fg_color="gray11")
        self.target_path_pane.grid(row=2, column=0, columnspan=2, padx=1, pady=10, sticky="ew")
        self.target_path_pane.grid_rowconfigure(0, weight=1)
        self.target_path_pane.grid_columnconfigure((0, 1), weight=1)
        self.target_path_pane.grid_propagate(False)
        # grab target folder button
        self.grab_tf_btn = ctk.CTkButton(master=self.target_path_pane, text="Select Target Folder", command=self.get_target_folder, font=button_font_config)
        self.grab_tf_btn.grid(row=1, column=0, columnspan=2, padx=20, pady=5, sticky="ew")
        self.target_path_ind = ctk.CTkLabel(master=self.target_path_pane, text="Current target path: ", font=tab_font_config)
        self.target_path_ind.grid(row=0, column=0, padx=20, pady=5, sticky="nw")
        # self.target_path = ctk.CTkLabel(master=self.target_path_pane, textvariable=self.target_folder_path, font=body_font_config)
        self.target_path_popup = ctk.CTkButton(master=self.target_path_pane, text="Show File Path", command=self.show_target_path, font=button_font_config)
        self.target_path_popup.grid(row=0, column=1, padx=20, pady=5, sticky="ne")

        
        # destination path box
        self.dest_path_pane = ctk.CTkFrame(master=self.pdf_tab, height=75, fg_color="gray11")
        self.dest_path_pane.grid(row=3, column=0, columnspan=2, padx=1, pady=10, sticky="ew")
        self.dest_path_pane.grid_rowconfigure(0, weight=1)
        self.dest_path_pane.grid_columnconfigure((0, 1), weight=1)
        self.dest_path_pane.grid_propagate(False)
        # grab destination folder button
        self.grab_df_btn = ctk.CTkButton(master=self.dest_path_pane, text="Select Destination Folder", command=self.get_dest_folder, font=button_font_config)
        self.grab_df_btn.grid(row=1, column=0, columnspan=2, padx=20, pady=5, sticky="ew")
        self.dest_path_ind = ctk.CTkLabel(master=self.dest_path_pane, text="Current destination path: ", font=tab_font_config)
        self.dest_path_ind.grid(row=0, column=0, padx=20, pady=5, sticky="nw")
        # self.dest_path = ctk.CTkLabel(master=self.dest_path_pane, textvariable=self.dest_folder_path, font=body_font_config)
        self.dest_path_popup = ctk.CTkButton(master=self.dest_path_pane, text="Show File Path", command=self.show_dest_path, font=button_font_config)
        self.dest_path_popup.grid(row=0, column=1, padx=20, pady=5, sticky="ne")
                    
        # input PDF name
        self.input_pdf_name_pane = ctk.CTkFrame(master=self.pdf_tab, height=24, fg_color="gray11")
        self.input_pdf_name_pane.grid(row=4, column=0, columnspan=2, padx=1, pady=10, sticky="ew")
        self.input_pdf_name_pane.grid_rowconfigure(0, weight=1)
        self.input_pdf_name_pane.grid_columnconfigure((0, 1), weight=1)
        self.input_label = ctk.CTkLabel(master=self.input_pdf_name_pane, text="PDF Name:", font=tab_font_config)
        self.input_label.grid(row=0, column=0, padx=20, pady=5, sticky="nw")
        self.input_box = ctk.CTkEntry(master=self.input_pdf_name_pane, width=400)
        self.input_box.grid(row=0, column=1, padx=20, pady=5, sticky="ne")
        
        # create PDF button
        self.create_pdf_btn = ctk.CTkButton(master=self.pdf_tab, text="Create PDF(s)", command=self.create_pdf, font=exec_button_font_config, height=50)
        self.create_pdf_btn.grid(row=5, column=0, columnspan=2, padx=20, pady=(20, 0), sticky="ew")
        
        # output box
        self.output_pane = ctk.CTkFrame(master=self.pdf_tab, height=32, fg_color="gray11")
        self.output_pane.grid(row=6, column=0, columnspan=2, padx=1, pady=1, sticky="ew")
        self.output_pane.grid_rowconfigure(0, weight=1)
        self.output_pane.grid_columnconfigure((0, 1), weight=1)
        self.output_pane.grid_propagate(False)
        self.status_ind = ctk.CTkLabel(master=self.output_pane, text="Status: ", font=tab_font_config)
        self.status_ind.grid(row=0, column=0, padx=20, sticky="nw")
        self.status_ind = ctk.CTkLabel(master=self.output_pane, textvariable=self.status, font=body_font_config)
        self.status_ind.grid(row=0, column=1, padx=20, sticky="ne")
        
        
        """
        Image splitter pane
        """
        self.splitter_tab.grid_rowconfigure(6, weight=1)
        self.splitter_tab.grid_columnconfigure((0, 0), weight=1)
        
        header_txt = "Grab a folder with scans and split them vertically"
        body_txt = "This assumes scans are of sheets of US Letter paper divided into two pages, like a small comic book."

        self.scan_splitter_header = ctk.CTkLabel(master=self.splitter_tab, text=header_txt, font=header_font_config, wraplength=580)
        self.scan_splitter_header.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        
        self.scan_splitter_info = ctk.CTkLabel(master=self.splitter_tab, text=body_txt, font=body_font_config, wraplength=500)
        self.scan_splitter_info.grid(row=1, column=0, padx=20, pady=20, sticky="new")
        
        # target path box
        self.target_path_pane = ctk.CTkFrame(master=self.splitter_tab, height=75, fg_color="gray11")
        self.target_path_pane.grid(row=2, column=0, columnspan=2, padx=1, pady=10, sticky="ew")
        self.target_path_pane.grid_rowconfigure(0, weight=1)
        self.target_path_pane.grid_columnconfigure((0, 1), weight=1)
        self.target_path_pane.grid_propagate(False)
        # grab target folder button
        self.grab_tf_btn = ctk.CTkButton(master=self.target_path_pane, text="Select Target Folder", command=self.get_target_folder, font=button_font_config)
        self.grab_tf_btn.grid(row=1, column=0, columnspan=2, padx=20, pady=5, sticky="ew")
        self.target_path_ind = ctk.CTkLabel(master=self.target_path_pane, text="Current target path: ", font=tab_font_config)
        self.target_path_ind.grid(row=0, column=0, padx=20, pady=5, sticky="nw")
        # self.target_path = ctk.CTkLabel(master=self.target_path_pane, textvariable=self.target_folder_path, font=body_font_config)
        self.target_path_popup = ctk.CTkButton(master=self.target_path_pane, text="Show File Path", command=self.show_target_path, font=button_font_config)
        self.target_path_popup.grid(row=0, column=1, padx=20, pady=5, sticky="ne")
        
        # destination path box
        self.dest_path_pane = ctk.CTkFrame(master=self.splitter_tab, height=75, fg_color="gray11")
        self.dest_path_pane.grid(row=3, column=0, columnspan=2, padx=1, pady=10, sticky="ew")
        self.dest_path_pane.grid_rowconfigure(0, weight=1)
        self.dest_path_pane.grid_columnconfigure((0, 1), weight=1)
        self.dest_path_pane.grid_propagate(False)
        # grab destination folder button
        self.grab_df_btn = ctk.CTkButton(master=self.dest_path_pane, text="Select Destination Folder", command=self.get_dest_folder, font=button_font_config)
        self.grab_df_btn.grid(row=1, column=0, columnspan=2, padx=20, pady=5, sticky="ew")
        self.dest_path_ind = ctk.CTkLabel(master=self.dest_path_pane, text="Current destination path: ", font=tab_font_config)
        self.dest_path_ind.grid(row=0, column=0, padx=20, pady=5, sticky="nw")
        # self.dest_path = ctk.CTkLabel(master=self.dest_path_pane, textvariable=self.dest_folder_path, font=body_font_config)
        self.dest_path_popup = ctk.CTkButton(master=self.dest_path_pane, text="Show File Path", command=self.show_dest_path, font=button_font_config)
        self.dest_path_popup.grid(row=0, column=1, padx=20, pady=5, sticky="ne")
        
        # create PDF button
        self.create_pdf_btn = ctk.CTkButton(master=self.splitter_tab, text="Halve all images in folder", command=self.create_pdf, font=exec_button_font_config, height=50)
        self.create_pdf_btn.grid(row=5, column=0, columnspan=2, padx=20, pady=(20, 0), sticky="ew")
        
        # output box
        self.output_pane = ctk.CTkFrame(master=self.splitter_tab, height=32, fg_color="gray11")
        self.output_pane.grid(row=6, column=0, columnspan=2, padx=1, pady=1, sticky="ew")
        self.output_pane.grid_rowconfigure(0, weight=1)
        self.output_pane.grid_columnconfigure((0, 1), weight=1)
        self.output_pane.grid_propagate(False)
        self.status_ind = ctk.CTkLabel(master=self.output_pane, text="Status: ", font=tab_font_config)
        self.status_ind.grid(row=0, column=0, padx=20, sticky="nw")
        self.status_ind = ctk.CTkLabel(master=self.output_pane, textvariable=self.status, font=body_font_config)
        self.status_ind.grid(row=0, column=1, padx=20, sticky="ne")
            
        # def check_input_validity():
        #     if self.folder_switch
        
    # get target folder
    def get_target_folder(self):
        folder_path = ctk.filedialog.askdirectory(title = "Select a folder")
        
        print(folder_path)
        self.target_folder_path.set(folder_path)
    
    # get destination folder (where to put the new PDF file)
    def get_dest_folder(self):
        folder_path = ctk.filedialog.askdirectory(title = "Select a folder")
        
        print(folder_path)
        self.dest_folder_path.set(folder_path)
        
    def set_multiple_pdfs(self):
        self.multiple_folders = self.folder_switch_default.get()
        print(self.multiple_folders)
        if self.multiple_folders:
            self.input_box.configure(state="disabled")
        else:
            self.input_box.configure(state="normal")
    
    def create_pdf(self):
        print("button clicked")
        target_folder_path = self.target_folder_path.get()
        dest_folder_path = self.dest_folder_path.get()
        custom_name = self.input_box.get()
        if self.multiple_folders == False:
            if self.input_box.get() is "":
                pdf_maker.convert_to_pdf(target_folder_path, dest_folder_path, None)
            else:
                pdf_maker.convert_to_pdf(target_folder_path, dest_folder_path, custom_name)
            self.status.set(pdf_maker.status)
            
        elif self.multiple_folders == True:
            for filename in os.listdir(target_folder_path):
                path = os.path.join(target_folder_path, filename).replace("\\","/")
                pdf_maker.convert_to_pdf(path, dest_folder_path, None)
                self.status.set(pdf_maker.status)
                # self.status_ind.configure(textvariable=pdf_maker.status)
        
    def show_target_path(self):
        popup_window = ctk.CTkToplevel(self)
        popup_window.title("Target File Path")
        popup_window.geometry("400x100")
        
        label = ctk.CTkLabel(popup_window, textvariable=self.target_folder_path, wraplength=400, padx=20, pady=20)
        label.pack()
        
    def show_dest_path(self):
        popup_window = ctk.CTkToplevel(self)
        popup_window.title("Destination File Path")
        popup_window.geometry("400x100")
        
        label = ctk.CTkLabel(popup_window, textvariable=self.dest_folder_path, wraplength=400, padx=20, pady=20)
        label.pack()
    

# run window
root = root()
root.mainloop()