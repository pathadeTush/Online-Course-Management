import hashlib
import os, secrets
from PIL import Image
from flask import current_app

SALT = '1g2'

def get_hashed_msg(msg):
    msg = msg + SALT
    hash = hashlib.md5(msg.encode())
    msg = hash.hexdigest()
    return msg

def save_picture(form_picture, dir):
    # creating secret key for name of picture filename. we are saving a secret key for picture file instead of saving the name of file directly
    random_hex = secrets.token_hex(8)
    # filename we will not be using furthur so use '_' to store the filename. Because python will throw an error of unused variable. We can avoid it by using underscore.
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    # it creates the path by concatenating app path and static/profile_pics folder path with name of file
    picture_path = os.path.join(
        current_app.root_path, f'static/{dir}/', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    # it saves the picture_path to the argument passed
    i.save(picture_path)

    return picture_fn
