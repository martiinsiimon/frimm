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

    for y in range(height):
        for x in range(width):
            pix_index = y * width * pix_w + x * pix_w 
            res = \
                in_img[pix_index + r_in_off] * 0.299 + \
                in_img[pix_index + g_in_off] * 0.587 + \
                in_img[pix_index + b_in_off] * 0.114
            out_img[pix_index + r_out_off] = \
                out_img[pix_index + g_out_off] = \
                out_img[pix_index + b_out_off] = res
