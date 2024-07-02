# Jeff's Comic Digitalization Labs

When I was in elementary school, I spent much of my free time expressing my imagination artistically. I created many comic books, comic strips, single-panel comics, etc. As time progresses, I've lost interest in this activity, but I find it of interest to preserve all of my work wherever feasible digitally (work completed on regular sheets of paper is easier to work with), thus, I've taken the time to scan everything, striving for the best quality possible.

This is a simple GUI application (based on CustomTkinter) that allows me to streamline the process of managing scans of my work to create a seamless experience for revisiting my younger mind, as well as continue exercising skills in software development. Below are descriptions of two key functionalities of the application.

## PDF Maker
For a comic book or comic strip series, I organize scans into folders as appropriate, and the image files are numerically named as needed to maintain the chronology I intended long ago (I'd just need to make sure that I have the folder sorted by file name). However, clicking through each scan file in a folder to view pages is not an ideal viewing experience. It would be easier to scroll through a PDF file containing all scanned images (in order, as appropriate). 

Because the aforementioned organization has already been done, I found that automating the consolidation of images in a folder into a single PDF would be fairly simple. Thus, this application features a program that allows the selection of a folder containing scanned images for the creation of a single PDF file containing all image files, algorithmically organized by the numerical names of the loose image files.

## Image Splitter
There are unique circumstances regarding the organization of some of my work. For example, for my comic books, rather than allocating a single sheet of paper for a single page, I opted to fold a single sheet of paper (US Letter) hamburger-style to fit two pages on a single sheet, with a finished comic book product consisting of multiple folded sheets stapled together.

For the most seamless digital reading experience, I'd be required to scan the entire sheet of paper on both sides and evenly divide the scanned image file into two halves, each representing a single page. Doing this manually is tricky and unideal, hence my motivation to create a tool that automates this process.
