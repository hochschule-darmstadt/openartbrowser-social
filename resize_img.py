from PIL import Image
import os
import io

def limit_img_size(img_filename, img_target_filename, target_filesize, tolerance=5):
    img = img_orig = Image.open(img_filename)
    aspect = img.size[0] / img.size[1]

    while True:
        with io.BytesIO() as buffer:
            img.save(buffer, format="JPEG")
            data = buffer.getvalue()
        filesize = len(data)
        size_deviation = filesize / target_filesize
        print("size: {}; factor: {:.3f}".format(filesize, size_deviation))

        if size_deviation <= (100 + tolerance) / 100:
            # filesize fits
            with open(img_target_filename, "wb") as f:
                f.write(data)
            break
        else:
            # filesize not good enough => adapt width and height
            # use sqrt of deviation since applied both in width and height
            new_width = img.size[0] / size_deviation**0.5
            new_height = new_width / aspect
            # resize from img_orig to not lose quality
            img = img_orig.resize((int(new_width), int(new_height)))


