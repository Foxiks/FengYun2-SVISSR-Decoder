import bitstring, Levenshtein, argparse, time
parser=argparse.ArgumentParser()
parser.add_argument("-o", "--output", help="Output binary file name")
parser.add_argument("-i", "--input", help="Input binary file name")
inputfile=parser.parse_args().input
outfile=parser.parse_args().output

def pn_derandomizer(data, mask):
    return str(bin(int(mask)^int(data)))[2:].zfill(354848)

def byte_inverter(derand):
    chunks=[derand[i:i+8] for i in range(0, len(derand), 8)]
    f=chunks[::2]
    two_invert=bitstring.BitArray(bin=''.join(chunks[1:][::2]))
    two_invert.invert()
    s=two_invert.bin
    s=[s[i:i+8] for i in range(0, len(s), 8)]
    return [''.join(x) for x in zip(f, s)]

def get_byte(f):
    while(byte := f.read(1)):
        return bin(int().from_bytes(byte, 'big'))[2:].zfill(8)
    
def get_frame_bytes(f):
    while(byte := f.read(44356)):
        return bin(int().from_bytes(byte, 'big'))[2:].zfill(354848)

def skip_end_frame(f):
    while(byte := f.read(5025)):
        return
    
def main(input_file, sync_marker, sync_buffer, mask, out):
    bit_array=''
    k=0
    n=0
    while True:
        if(len(bit_array)<=1):
            bits_array=get_byte(f=input_file)
            k=0
        if(bits_array!=None):
            bit_array=bits_array[k:]
            k+=1
            sync_buffer=sync_buffer[1:]+bit_array[:1]
            err=int(Levenshtein.hamming(sync_buffer, str(sync_marker)))
            if(err<=int(158)): #158
                n+=1
                print('New frame! '+str(n)+' | Sync word: 0x'+str(hex(int(sync_buffer, 2)))[-16:].upper()+' | BER: '+str(round(float(err/10.24), 1))+'% | Sync threshold: '+str(round(float(err/3.68), 1))+'%'+'     ', end='\r')
                frame=get_frame_bytes(f=f)
                #frame=int(str(bit_array)+str(frame[:int(354848-len(bit_array))]), 2)
                frame=int(str(bit_array[1:])+str(frame[:int(354848-len(bit_array[1:]))]), 2)
                derand = pn_derandomizer(data=frame, mask=mask)
                out.write(int(''.join(byte_inverter(derand)), 2).to_bytes(44356, byteorder='big', signed=False))
                skip_end_frame(f=f)
        else:
            input_file.close()
            break
    return

if(__name__=='__main__'):
    f=open(inputfile, "rb")
    out_file=open(outfile, 'ab')
    start_time = time.time()
    sync = '72CB2EBAE79E5145E79C5149E7B451B9E5945D79CF14A27BCD18AE53E5E85C71C924B6DBB6D9B6D5B6FDB60DB42DB8ED926D6D6F6F63634B4BBBB99995557FFF'
    sync_marker=bitstring.BitArray(hex=sync).bin
    sync_buffer=str('0'*int(len(sync_marker)))
    with open('fy2_mask.bin', 'rb') as file:
        mask=int(bitstring.ConstBitStream(file).read(354848).uint)
    main(input_file=f, sync_buffer=sync_buffer, sync_marker=sync_marker, mask=mask, out=out_file)
    print("--- %s seconds ---" % (time.time() - start_time)+str(' '*50))