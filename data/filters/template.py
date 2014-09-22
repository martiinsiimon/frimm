# Author of this filter
__author_name__ = 'Your Name'
__author_mail__ = 'your.email@address.tld'

# Name of this filter. Please, keep the length under 20 characters
__filter_name__ = 'Filter name'

# Description of this filter
__filter_description__ = '''Description of filter. Use as much characters
as you want, it's not limited at all.'''

# Filter itself. Please, use this function predefined interface,
# including name and parameters with its order
def process(input_img, output_img):
    # Here comes the filter body
    width = input_img.width
    height = input_img.height

    for y in range(height):
        for x in range(width):
            output_img[y * width + x].r = 0  #  B
            output_img[y * width + x].g = 0  #  G
            output_img[y * width + x].b = 0  #  R
