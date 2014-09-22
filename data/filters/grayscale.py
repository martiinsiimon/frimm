__author_name__ = 'Martin Simon'
__author_mail__ = 'martiin.siimon@gmail.com'
__filter_name__ = 'Grayscale'
__filter_description__ = 'Simple grayscale filter with no options. Only converts color image to scale of gray.'


def process(input_img, output_img):
    width = input_img.width
    height = input_img.height

    for y in range(height):
        for x in range(width):
            output_img[y * width + x].v = \
                input_img[y * width + x].r * 0.299 + \
                input_img[y * width + x].g * 0.587 + \
                input_img[y * width + x].b * 0.114
