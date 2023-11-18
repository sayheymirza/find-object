from PIL import Image
import random
import os
import time

# assets directory
assets_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "..", "assets")


def generate(folders=["history", "bedroom"], output_size=(2048, 2048), image_size=(32, 32), countable=(20, 30), to_find={}):
    # generate counts of each image
    def generate_counts():
        output = []

        # get all images name with os walk
        for folder in folders:
            for root, dirs, files in os.walk(os.path.join(assets_dir, folder)):
                for file in files:
                    count = 1

                    if not file in to_find:
                        # generate random number between 1 and 10
                        count = random.randint(countable[0], countable[1])

                    for i in range(count):
                        output.append(os.path.join(assets_dir, folder, file))

        return output

    result = generate_counts()

    positions = []

    def generate_position():
        image_width = output_size[0]
        image_height = output_size[1]
        # generate random x and y
        x = random.randint(0, image_width - 1)
        y = random.randint(0, image_height - 1)

        # x position must be not out of range
        if x + image_size[0] > image_width:
            x = image_width - image_size[0]

        # y position must be not out of range
        if y + image_size[1] > image_height:
            y = image_height - image_size[1]

        return (x, y)

    def generate_image():
        image_width = output_size[0]
        image_height = output_size[1]

        canvas = Image.new("RGB", (image_width, image_height), "white")

        for level in range(len(result)):
            image = Image.open(result[level])

            image.convert("RGBA")

            # resize image to image_size without changing losing pixels
            image = image.resize(image_size, Image.Resampling.LANCZOS)

            # generate random position
            x, y = generate_position()

            filename = result[level].split("\\")[-1]

            # if level image is in to_find, set x and y
            if filename in to_find:
                to_find[filename] = (x, y)

            # paste image to canvas
            canvas.paste(image, (x, y), mask=image)

        return canvas

    output_filename = str(time.time()).split(".")[0] + ".jpg"

    output_file = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), "..", "output", output_filename)

    # save image
    generate_image().save(output_file, format='JPEG', subsampling=0, quality=100)

    return output_filename, to_find
