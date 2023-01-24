import bitstring, time, binascii, os, cv2, numpy, argparse, gc, sys
from PIL import Image
start_time = time.time()
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="Input binary file")
args = parser.parse_args()
inp = args.input
line=0
back_line=0
up_line=88712
if(__name__ == "__main__"):
    print("------------------------------------------------------------------------------------------------------")
    print("                                                                                                      ")
    print("                                        FengYun-2 SVISSR decoder                                      ")
    print("                                             by Egor UB1QBJ                                           ")
    print("                                                                                                      ")
    print("------------------------------------------------------------------------------------------------------")
    with open(inp, "rb") as image:
        print("Reading input frames...")
        f = image.read()
        size = os.path.getsize(inp)
        l = int(size)/int(44356)
    bbyteArray = bytearray(f)
    grayImage = numpy.array(bbyteArray).reshape(int(l), int(44356))
    print("Saving IR CH-1...")
    crop_img1 = grayImage[0:int(l), 2552:4846]
    cv2.imwrite('IR-CH_1.png', crop_img1)
    print("Saving IR CH-2...")
    crop_img2 = grayImage[0:int(l), 5102:7396]
    cv2.imwrite('IR-CH_2.png', crop_img2)
    print("Saving IR CH-3...")
    crop_img3 = grayImage[0:int(l), 7653:9947]
    cv2.imwrite('IR-CH_3.png', crop_img3)
    del crop_img1
    del crop_img2
    del crop_img3
    gc.collect()
    with open(inp, "rb") as ts_all:
        frames = ts_all.read().hex()
        size = os.path.getsize(inp)
        l = int(size)/int(44356)
    os.mkdir("Tmp")
    print('Read VIS Chunks...')
    while(int(line)<=int(l)):
        frame = frames[back_line:up_line]
        back_line = up_line
        up_line+=88712
        chunks1 = frame[20408:34160]
        chunks2 = frame[34673:48425]
        chunks3 = frame[48938:62690]
        chunks4 = frame[63203:76955]
        ir10 = frame[82466:88216]
        with open('Tmp/chunks.1', 'ab') as f1:
            f1.write(binascii.unhexlify(chunks1))
        with open('Tmp/chunks.2', 'ab') as f2:
            f2.write(binascii.unhexlify(chunks2))
        with open('Tmp/chunks.3', 'ab') as f3:
            f3.write(binascii.unhexlify(chunks3))
        with open('Tmp/chunks.4', 'ab') as f4:
            f4.write(binascii.unhexlify(chunks4))
        with open('Tmp/ir10.ch', 'ab') as f4:
            f4.write(binascii.unhexlify(ir10))
        line+=1
    print('Convert VIS Chunk 1 to 8-bit pattern...')
    file1 = open('Tmp/chunks.1', 'rb').read()
    b = bitstring.BitStream(file1).bin
    chunks = [b[i:i+6] for i in range(0, len(b), 6)]
    chunks = [str+'00' for str in chunks]
    del b
    del file1
    gc.collect()
    print('Convert VIS Chunk 2 to 8-bit pattern...')
    file2 = open('Tmp/chunks.2', 'rb').read()
    b1 = bitstring.BitStream(file2).bin
    chunks1 = [b1[i:i+6] for i in range(0, len(b1), 6)]
    chunks1 = [str+'00' for str in chunks1]
    del b1
    del file2
    gc.collect()
    print('Convert VIS Chunk 3 to 8-bit pattern...')
    file3 = open('Tmp/chunks.3', 'rb').read()
    b2 = bitstring.BitStream(file3).bin
    chunks2 = [b2[i:i+6] for i in range(0, len(b2), 6)]
    chunks2 = [str+'00' for str in chunks2]
    del b2
    del file3
    gc.collect()
    print('Convert VIS Chunk 4 to 8-bit pattern...')
    file4 = open('Tmp/chunks.4', 'rb').read()
    b3 = bitstring.BitStream(file4).bin
    chunks3 = [b3[i:i+6] for i in range(0, len(b3), 6)]
    chunks3 = [str+'00' for str in chunks3]
    del b3
    del file4
    gc.collect()
    print('Mixing VIS Chunks...')
    res = [x for y in zip(chunks, chunks1, chunks2, chunks3) for x in y]
    with open('Tmp/data.mixed', 'wb') as file:
        bitstring.BitArray(bin=''.join(res)).tofile(file)
    del res
    del chunks
    del chunks1
    del chunks2
    del chunks3
    gc.collect()
    with open('Tmp/data.mixed', "rb") as image:
        f = image.read()
    bbyteArray = bytearray(f)
    grayImage = numpy.array(bbyteArray).reshape(int(l), int(36672))
    print("Saving VIS...")
    cv2.imwrite('CH_VIS.png', grayImage)
    src = cv2.imread('CH_VIS.png', cv2.IMREAD_UNCHANGED)
    re = cv2.resize(src, (9168, int(l*4)))
    cv2.imwrite('CH_VIS.png', re)
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
    print("Done!")
    print(str(time.time()-start_time))
    os.remove('Tmp/chunks.1')
    os.remove('Tmp/chunks.2')
    os.remove('Tmp/chunks.3')
    os.remove('Tmp/chunks.4')
    os.remove('Tmp/data.mixed')
    os.remove('Tmp/ir10.bit')
    os.remove('Tmp/ir10.ch')
    os.rmdir('Tmp')
    sys.exit()