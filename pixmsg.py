try:
    from PIL import Image
except ImportError, e:
    print
    print 'You need to install python PIL package to run this tool.'
    print 'Try: pip install PIL'
    print
    quit(4)
import sys
import optparse
def get_msg(img, start=(0,0)):
    msg=''
    for x in range(start[0], img.size[0]):
        for y in range(start[1], img.size[1]):
            c = img.getpixel((x, y))
            if c[1] == 0:
                return msg
            msg += chr(c[1])
    return msg
ascii_table = {chr(c) : c for c in range(1,256)}
def asc(c):
    return ascii_table[c]
def insert_msg(img, msg, start=(0,0)):
    count = 0
    for x in range(start[0], img.size[0]):
        for y in range(start[1], img.size[1]):
            pxl = img.getpixel((x, y))
            if count == len(msg):
                img.putpixel((x, y), (255, 0, 0, 0))
                return
            c = asc(msg[count])
            img.putpixel((x, y), (255, c, c, c))
            count +=1
    img.putpixel((x, y), (255, 0, 0, 0))

def main():
    parser = optparse.OptionParser(usage='%prog [Option(s)] -f <inputfile>', description='Hide a secret message on a image.', epilog='PixMsg - Created by LvMalware Drk', version='Beta version.')
    parser.add_option('-f', dest='filename', type='string', help='Especify the input image file')
    parser.add_option('-v', dest='view', default=False, action="store_true", help='View the message from a image')
    parser.add_option('-i', dest='insert', default=False, action="store_true", help='Insert a message in a image')
    parser.add_option('-m', dest='message', type='string', help='Especify the message')
    parser.add_option('--sX', dest='startX', default=0, type='int', help='Especify a x to start at the pixels matrix')
    parser.add_option('--sY', dest='startY', default=0, type='int', help='Especify a y to start at the pixels matrix')
    parser.add_option('-o', dest='output', type='string', help='Especify the output image file (without extension)')
    parser.add_option('--iF', dest='txtfile', type='string', help='A text file containing the message to hide')
    opts, args = parser.parse_args()
    if opts.view == opts.insert:
        print parser.get_usage()
        print 'Use -h or --help for more help'
        return 3
    if opts.filename == None:
        print 'No input file.'
        return 2    
    input_img = Image.open(opts.filename.replace('\\', '/')).convert('RGBA')
    if opts.view:
        print get_msg(input_img, (opts.startX, opts.startY))
    elif opts.insert:
        if opts.output == None:
            print 'You must especify the output file.'
            return 1
        msg = opts.message
        if opts.txtfile != None:
            msg = open(opts.txtfile.replace('\\', '/'), 'r').read()
        insert_msg(input_img, msg, (opts.startX, opts.startY))
        input_img.save(opts.output + '.png', input_img.format)
        print 'Message inserted at (%d, %d).' %(opts.startX, opts.startY)
    return 0

if __name__ == '__main__':
    quit(main())
