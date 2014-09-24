__author_name__ = 'Martin Simon'
__author_mail__ = 'martiin.siimon@gmail.com'
__filter_name__ = 'Grayscale'
__filter_description__ = 'Simple grayscale filter with no options. Only converts color image to scale of gray.'

def process(in_img, out_img):
    width = in_img.width
    height = in_img.height
    pix_w = in_img.pixel_width

    r_in_off = in_img.r_offset
    g_in_off = in_img.g_offset
    b_in_off = in_img.b_offset
    
    r_out_off = out_img.r_offset
    g_out_off = out_img.g_offset
    b_out_off = out_img.b_offset

    pix_index = 0
    indata = in_img.data
    outdata = out_img.data

    for y in xrange(height):
        for x in xrange(width):
            pix_index = y * width * pix_w + x * pix_w 
            res = \
                indata[pix_index + r_in_off] * 0.299 + \
                indata[pix_index + g_in_off] * 0.587 + \
                indata[pix_index + b_in_off] * 0.114
            outdata[pix_index + r_out_off] = \
                outdata[pix_index + g_out_off] = \
                outdata[pix_index + b_out_off] = int(res)
