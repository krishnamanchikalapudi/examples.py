import pytesseract, os
from PIL import Image


folder_path = "./images"

count=1
for file_name in os.listdir(folder_path):
    if ( file_name.endswith(".jpeg") or file_name.endswith(".jpg")):
        # Prints only text file present in My Folder
        print(f" file name: {file_name}")
        image = Image.open(folder_path+"/"+file_name)
        text = pytesseract.image_to_string(image)
        print (f"{text} \n\n")

