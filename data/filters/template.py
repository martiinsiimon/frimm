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
    # width and height of source and taget images
    width = in_img.width
    height = in_img.height
    
    # Width of pixels, e.g. ARGB has pixel of width 4 (bytes)
    pix_w = in_img.pixel_width
    
    # Offsets for color channels of input image
    r_in_off = in_img.r_offset
    g_in_off = in_img.g_offset
    b_in_off = in_img.b_offset
    
    # Offsets for color channels of output image
    r_out_off = out_img.r_offset
    g_out_off = out_img.g_offset
    b_out_off = out_img.b_offset

    # Local stored data are faster!
    indata = in_img.data
    outdata = out_img.data
    
    # Initialize variable before loop = faster code
    pix_index = 0

    # Use xrange rather than range, it's more efficient
    for y in xrange(height):
        for x in xrange(width):
            pix_index = y * width * pix_w + x * pix_w 
            outdata[pix_index + r_out_off] = 0  #  R
            outdata[pix_index + g_out_off] = 0  #  G
            outdata[pix_index + b_out_off] = 0  #  B
