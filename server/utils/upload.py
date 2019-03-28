from binascii import a2b_base64

from django.core.files.base import ContentFile


# def binary_From_data_uri(data_uri):
#     head, image_data = data_uri.split(',')
#     return a2b_base64(image_data)


def file_from_data_uri(data_uri, basename):
    head, image_data = data_uri.split(',')
    binary_image_data = a2b_base64(image_data)
    image_type = head.split(';')[0].split('/')[1]
    img_suffix = {'jpeg': 'jpg'}.get(image_type, image_type)
    return ContentFile(binary_image_data, "{}.{}".format(basename, img_suffix))
