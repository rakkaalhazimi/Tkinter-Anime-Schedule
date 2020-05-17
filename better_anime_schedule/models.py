import os, csv, sys, re, requests
from PIL import Image
from io import BytesIO
from .scraper import current_path, filename

class CSVModel:
    """Defult CSV Model"""

    field_names = [
        "Name",
        "Episode",
        "Day",
        "Date",
        "Href",
        "Src_img"
    ]

    image_file = "images"

    def __init__(self):
        self.filename = filename
        self.desc = self.field_names[:4] # Name, Episode, Day, Date
        self.redirect = self.field_names[4]  # Href
        self.imgsrc = self.field_names[-1] # Src Img


    def get_csv(self):
        # Read CSV
        with open(os.path.join(current_path, filename), 'r') as fh:
            reader = csv.DictReader(fh)
            csvdata = list(reader)

        return csvdata


    def get_source(self, data, field):
        # Read CSV
        img_dict = {}
        for index, row in enumerate(data):
            values = row[field]
            img_dict[str(index)] = values

        return img_dict


    def open_image(self, url):
        # get image filename
        compiler = re.compile("[A-Z].+\.jpg")
        result = compiler.search(url)

        # open image from url
        response = requests.get(url)
        img_byte = Image.open(BytesIO(response.content))

        # convert image from jpg to png
        png_compiler = re.compile("\.jpg")
        img_filename = png_compiler.sub(".png", result.group())
        img_path = os.path.join(current_path, self.image_file, img_filename)

        if os.path.exists(img_path):
            pass
        else:
            img_byte.save(img_path)

        return img_path

