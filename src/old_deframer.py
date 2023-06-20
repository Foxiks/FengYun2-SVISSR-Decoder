import bitstring, sys, Levenshtein, argparse, time, os
parser=argparse.ArgumentParser()
parser.add_argument("-o", "--output", help="Output binary file name")
parser.add_argument("-i", "--input", help="Input binary file name")
inputfile=parser.parse_args().input
outfile=parser.parse_args().output

###
sync = '72CB2EBAE79E5145E79C5149E7B451B9E5945D79CF14A27BCD18AE53E5E85C71C924B6DBB6D9B6D5B6FDB60DB42DB8ED926D6D6F6F63634B4BBBB99995557FFF'
#sync = '172e72e52e5ee5c65c95cb7cbb0b9a395c97cb70bb239ac95eb7c7b091a365cb5cbbcb98b95397e970772132c6ae97e7705321eac47e99075613f4683970972372cb2ebae79e5145e79c5149e7b451b9e5945d79cf14a27bcd18ae53e5e85c71c924b6dbb6d9b6d5b6fdb60db42db8ed926d6d6f6f63634b4bbbb99995557fff'
threshold = 158 # ~30%
#threshold = int(368)
###

def byte_inverter(derand):
    chunks=[derand[i:i+8] for i in range(0, len(derand), 8)]
    f=chunks[::2]
    two_invert=bitstring.BitArray(bin=''.join(chunks[1:][::2]))
    two_invert.invert()
    s=two_invert.bin
    s=[s[i:i+8] for i in range(0, len(s), 8)]
    return [''.join(x) for x in zip(f, s)]

def pn_derandomizer(data, mask):
    return str(bin(int(mask)^int(data)))[2:].zfill(354848)

def main(inputfile, outfile, sync, threshold):
    try:
        os.remove(str(outfile))
    except OSError:
        None
    with open('fy2_mask.bin', 'rb') as file:
        mask=int(bitstring.ConstBitStream(file).read(354848).uint)
    n=0
    sync_marker=bitstring.BitArray(hex=sync).bin
    buff=str('0'*int(len(sync_marker)))
    start_time = time.time()
    with open(str(inputfile), "rb") as file:
        stream_bytes=file.read()
    stream = bitstring.ConstBitStream(bytes=stream_bytes)
    out = open(str(outfile), 'ab')
    while True:
        try:
            bit=stream.read(1).bin
        except bitstring.ReadError:
            print("--- %s seconds ---" % (time.time() - start_time)+str(' '*50))
            sys.exit()
        buff=buff[1:]+bit
        err=int(Levenshtein.hamming(buff, str(sync_marker)))
        if(err<int(threshold)): #158
            try:
                line=stream.read(354848).uint
            except bitstring.ReadError:
                print("--- %s seconds ---" % (time.time() - start_time)+str(' '*50))
                out.close()
                sys.exit()
            derand = pn_derandomizer(data=line, mask=mask)
            bitstring.BitArray(bin=''.join(byte_inverter(derand))).tofile(out)
            n+=1
            print('New frame! '+str(n)+' | Sync word: 0x'+str(hex(int(buff, 2)))[-16:].upper()+' | BER: '+str(round(float(err/10.24), 1))+'% | Sync threshold: '+str(round(float(err/3.68), 1))+'%'+'     ', end='\r')
            try:
                #stream.read(40800).bin
                stream.read(40200).bin
            except bitstring.ReadError:
                print("--- %s seconds ---" % (time.time() - start_time)+str(' '*65))
                out.close()
                sys.exit()
        else:
            None

if __name__ == '__main__':
    main(inputfile=inputfile, outfile=outfile, sync=sync, threshold=threshold)