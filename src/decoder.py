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

def vis_chunks_reader(inp):
    line=0
    back_line=0
    up_line=88712
    with open(inp, "rb") as ts_all:
        frames = ts_all.read().hex()
        size = os.path.getsize(inp)
        l = int(size)/int(44356)
    os.mkdir("Tmp")
    print('Read VIS Chunks...')
    f1 = open('Tmp/chunks.1', 'ab')
    f2 = open('Tmp/chunks.2', 'ab')
    f3 = open('Tmp/chunks.3', 'ab')
    f4 = open('Tmp/chunks.4', 'ab')
    f5 = open('Tmp/ir10.ch', 'ab')
    while(int(line)<=int(l)):
        frame = frames[back_line:up_line]
        back_line = up_line
        up_line+=88712
        chunks1 = frame[20408:34160]
        chunks2 = frame[34673:48425]
        chunks3 = frame[48938:62690]
        chunks4 = frame[63203:76955]
        ir10 = frame[82466:88216]
        f1.write(binascii.unhexlify(chunks1))
        f2.write(binascii.unhexlify(chunks2))
        f3.write(binascii.unhexlify(chunks3))
        f4.write(binascii.unhexlify(chunks4))
        f5.write(binascii.unhexlify(ir10))
        line+=1
    f1.close()
    f2.close()
    f3.close()
    f4.close()
    f5.close()
    return

def vis1_chunks_converter():
    file1 = open('Tmp/chunks.1', 'rb').read()
    b = bitstring.BitStream(file1).bin
    chunks = [b[i:i+6] for i in range(0, len(b), 6)]
    chunks = [str+'00' for str in chunks]
    del b
    del file1
    gc.collect()
    return chunks

def vis2_chunks_converter():
    file2 = open('Tmp/chunks.2', 'rb').read()
    b1 = bitstring.BitStream(file2).bin
    chunks1 = [b1[i:i+6] for i in range(0, len(b1), 6)]
    chunks1 = [str+'00' for str in chunks1]
    del b1
    del file2
    gc.collect()
    return chunks1

def vis3_chunks_converter():
    file3 = open('Tmp/chunks.3', 'rb').read()
    b2 = bitstring.BitStream(file3).bin
    chunks2 = [b2[i:i+6] for i in range(0, len(b2), 6)]
    chunks2 = [str+'00' for str in chunks2]
    del b2
    del file3
    gc.collect()
    return chunks2

def vis4_chunks_converter():
    file4 = open('Tmp/chunks.4', 'rb').read()
    b3 = bitstring.BitStream(file4).bin
    chunks3 = [b3[i:i+6] for i in range(0, len(b3), 6)]
    chunks3 = [str+'00' for str in chunks3]
    del b3
    del file4
    gc.collect()
    return chunks3

def vis_mixer(chunks, chunks1, chunks2, chunks3):
    print('Mixing VIS Chunks...')
    res = [x for y in zip(chunks, chunks1, chunks2, chunks3) for x in y]
    with open('Tmp/data.mixed', 'wb') as file:
        bitstring.BitArray(bin=''.join(res)).tofile(file)
    del res

def vis_saver():
    with open('Tmp/data.mixed', "rb") as image:
        f = image.read()
    bbyteArray = bytearray(f)
    grayImage = numpy.array(bbyteArray).reshape(int(l), int(36672))
    print("Saving VIS...")
    cv2.imwrite('CH_VIS.png', grayImage)
    src = cv2.imread('CH_VIS.png', cv2.IMREAD_UNCHANGED)
    re = cv2.resize(src, (9168, int(l*4)))
    cv2.imwrite('CH_VIS.png', re)
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
    os.remove('Tmp/chunks.1')
    os.remove('Tmp/chunks.2')
    os.remove('Tmp/chunks.3')
    os.remove('Tmp/chunks.4')
    os.remove('Tmp/data.mixed')
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
    chunks = vis1_chunks_converter()
    chunks1 = vis1_chunks_converter()
    chunks2 = vis1_chunks_converter()
    chunks3 = vis1_chunks_converter()
    ir10_saver()
    ##
    vis_mixer(chunks=chunks, chunks1=chunks1, chunks2=chunks2, chunks3=chunks3)
    del chunks
    del chunks1
    del chunks2
    del chunks3
    gc.collect()
    vis_saver()
    print("Done!")
    print(str(time.time()-start_time))
    rmtmp()
    sys.exit()