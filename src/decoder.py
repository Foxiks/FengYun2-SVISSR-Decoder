from types import NoneType
import bitstring, time, binascii, os, cv2, numpy, argparse, gc, sys
from PIL import Image
from multiprocessing import Process

start_time = time.time()
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="Input binary file")
args = parser.parse_args()


def input_data_reader(inp):
    with open(inp, "rb") as image:
        print("Reading input frames...")
        f = image.read()
        size = os.path.getsize(inp)
        l = int(size)/int(44356)
    return bytearray(f), l

def ir_1_saver(grayImage):
    print("Saving IR CH-1...")
    crop_img = grayImage[0:int(l), 2552:4846]
    cv2.imwrite('IR-CH_1.png', crop_img)
    del crop_img
    gc.collect()
    return

def ir_2_saver(grayImage):
    print("Saving IR CH-2...")
    crop_img = grayImage[0:int(l), 5102:7396]
    cv2.imwrite('IR-CH_2.png', crop_img)
    del crop_img
    gc.collect()
    return

def ir_3_saver(grayImage):
    print("Saving IR CH-3...")
    crop_img = grayImage[0:int(l), 7653:9947]
    cv2.imwrite('IR-CH_3.png', crop_img)
    del crop_img
    gc.collect()
    return

def get_frame(file):
    while(byte := file.read(44356)):
        return byte.hex()

def vis_chunks_reader(inp):
    ts_all = open(inp, "rb")
    size = int(os.path.getsize(inp)/44356)
    os.mkdir("Tmp")
    print('Read VIS Chunks...')
    f1 = open('Tmp/chunks.vis', 'ab')
    f2 = open('Tmp/ir10.ch', 'ab')
    for _ in range(size):
        frame = get_frame(ts_all)
        f1.write(binascii.unhexlify(frame[20408:34160]))
        f1.write(binascii.unhexlify(frame[34673:48425]))
        f1.write(binascii.unhexlify(frame[48938:62690]))
        f1.write(binascii.unhexlify(frame[63203:76955]))
        f2.write(binascii.unhexlify(frame[82466:88216]))
    f1.close()
    f2.close()
    return

def get_vis_chunk_frame(file):
    while(byte := file.read(6876)):
        return str(bin(int().from_bytes(byte, 'big'))[2:].zfill(55008))

def vis_chunks_converter():
    with open('Tmp/chunks.vis', 'rb') as binary_file:
        data = binary_file.read()
        data = bytearray(data)

    with open('Tmp/chunks.visscaled', 'wb') as pixel_file:
        i = 0
        four_pixels = bytearray([0,0,0,0])
        while i < len(data):
            four_bytes = data[i]*0x10000 + data[i+1]*0x100 + data[i+2]
            i += 3
            four_pixels[0] = ((four_bytes >> (18)) & 0x3f) << 2
            four_pixels[1] = ((four_bytes >> (12)) & 0x3f) << 2
            four_pixels[2] = ((four_bytes >> (6)) & 0x3f) << 2
            four_pixels[3] = ((four_bytes) & 0x3f) << 2
            pixel_file.write(four_pixels)
    return

def vis_saver():
    with open('Tmp/chunks.visscaled', "rb") as image:
        f = image.read()
    bbyteArray = bytearray(f)
    grayImage = numpy.array(bbyteArray).reshape(int(l*4), int(9168))
    print("Saving VIS...")
    cv2.imwrite('CH_VIS.png', grayImage)
    src = cv2.imread('CH_VIS.png', cv2.IMREAD_UNCHANGED)
    cv2.imwrite('CH_VIS.png', src)
    return

def ir10_saver():
    print("Saving IR CH-4 (10-bit)...")
    file5 = open('Tmp/ir10.ch', 'rb').read()
    b4 = bitstring.BitStream(file5).bin
    chunks10 = [b4[i:i+10] for i in range(0, len(b4), 10)]
    del b4
    gc.collect()
    chunks10 = [str+'000000' for str in chunks10]
    with open('Tmp/ir10.bit', 'wb') as file:
      bitstring.BitArray(bin=''.join(chunks10)[8:]+'00000000').tofile(file)
    del chunks10
    gc.collect()
    with open('Tmp/ir10.bit', mode='rb') as f:
      d = numpy.fromfile(f,dtype=numpy.uint16,count=2300*int(l)).reshape(int(l), int(2300))
    PILimage = Image.fromarray(d)
    PILimage.save('IR-CH_4.png')
    return

def rmtmp():
    os.remove('Tmp/chunks.vis')
    os.remove('Tmp/chunks.visscaled')
    os.remove('Tmp/ir10.bit')
    os.remove('Tmp/ir10.ch')
    os.rmdir('Tmp')
    return

if(__name__ == "__main__"):
    print("------------------------------------------------------------------------------------------------")
    print("                                                                                                ")
    print("                                     FengYun-2 SVISSR decoder                                   ")
    print("                                          by Egor UB1QBJ                                        ")
    print("                                                                                                ")
    print("------------------------------------------------------------------------------------------------")
    inp = args.input
    bbyteArray, l = input_data_reader(inp=inp)
    grayImage = numpy.array(bbyteArray).reshape(int(l), int(44356))

    p1 = Process(target=ir_1_saver(grayImage=grayImage))
    p1.start()
    p2 = Process(target=ir_2_saver(grayImage=grayImage))
    p2.start()
    p3 = Process(target=ir_3_saver(grayImage=grayImage))
    p3.start()
    p4 = Process(target=vis_chunks_reader(inp=inp))
    p4.start()
    p1.join()
    p2.join()
    p3.join()
    p4.join()
    del bbyteArray
    del grayImage
    gc.collect()
    #
    print('Convert VIS Chunks to 8-bit pattern...')
    vis_chunks_converter()
    ir10_saver()
    ##
    vis_saver()
    print("Done!")
    print(str(time.time()-start_time))
    rmtmp()
    sys.exit()