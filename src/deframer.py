import time, io, os, sys
from hexhamming import hamming_distance_string
inputfile=sys.argv[1]
outfile=sys.argv[2]

def PN_mask_generator(mask):
    mask=bin(mask)[2:].zfill(15)
    out=[]
    for _ in range(354848):
        x2=mask[14:]
        x1=mask[13:14]
        xor1=int(x1)^int(x2)
        mask=str(xor1)+mask[:14]
        out.append(mask[14:])
    return int(''.join(out), 2)

def pn_derandomizer(data, mask):
    return int(int(mask)^int(data)).to_bytes(44356,'big')

def byte_inverter(derand):
    out_bytes_arr=bytearray()
    in_bytes_arr=bytearray()
    in_bytes_arr.extend(derand)
    for i in range(0,44356,2):
        out_bytes_arr.append(int(in_bytes_arr[i]))
        out_bytes_arr.append(int((~in_bytes_arr[i+1]) & 0x00ff))
    return bytes(out_bytes_arr)

def get_byte(f):
    while(byte := f.read(1)):
        return bin(int().from_bytes(byte, 'big'))[2:].zfill(8)

def get_frame_bytes(f):
    while(byte := f.read(44356)):
        return bin(int().from_bytes(byte, 'big'))[2:].zfill(354848)

def skip_end_frame(f):
    while(byte := f.read(5025)):
        return

def skip_frame(f):
    while(byte := f.read(int(49381*2))):
        return

def multi_skip(f):
    while(byte := f.read(int(49381*5))):
        return

def main(input_file, sync_buffer, mask, out, out_filename, total_len):
    bit_array=''
    k=0
    n=0
    bit_noise_counter=0
    multi_skip_counter=0
    sync_state='NO SYNC!'
    for _ in range(int(total_len+100)):
        if(len(bit_array)<=1):
            bits_array=get_byte(f=input_file)
            k=0
        if(bits_array!=None):
            bit_array=bits_array[k:]
            k+=1
            sync_buffer=sync_buffer[1:]+bit_array[:1]
            err=int(hamming_distance_string(hex(int(sync_buffer,2))[2:].zfill(128), sync))
            if(err<=int(158)): #158
                bit_noise_counter=0
                multi_skip_counter=0
                sync_state='SYNCED!'
                n+=1
                print(f'Frame: {n} | State: {sync_state} | Sync word: 0x{str(hex(int(sync_buffer, 2)))[-16:].upper()} | BER: {str(round(float(err/5.12), 1)).rjust(4, " ")}% | Sync threshold: {round(float(err/1.58), 1)}%     ', end='\r')
                frame=get_frame_bytes(f=input_file)
                frame=int(str(bit_array[1:])+str(frame[:int(354848-len(bit_array[1:]))]), 2)
                derand = pn_derandomizer(data=frame, mask=mask)
                out.write(byte_inverter(derand))
                skip_end_frame(f=input_file)
            else:
                bit_noise_counter+=1
            if(bit_noise_counter>=791120):
                if(multi_skip_counter>=10):
                    multi_skip(f=input_file)
                    multi_skip_counter=0
                    sync_state='NO SYNC!'
                    print(f'Frame: {n} | State: {sync_state} | Sync word: 0x{str(hex(int(sync_buffer, 2)))[-16:].upper()} | BER: {str(round(float(err/5.12), 1)).rjust(4, " ")}% | Sync threshold: {round(float(err/1.58), 1)}%     ', end='\r')
                else:
                    sync_state='NO SYNC!'
                    print(f'Frame: {n} | State: {sync_state} | Sync word: 0x{str(hex(int(sync_buffer, 2)))[-16:].upper()} | BER: {str(round(float(err/5.12), 1)).rjust(4, " ")}% | Sync threshold: {round(float(err/1.58), 1)}%     ', end='\r')
                    skip_frame(f=input_file)
                    multi_skip_counter+=1
                bit_noise_counter=0
        if(bits_array==None):
            print('Saving data...')
            with open(out_filename, 'wb') as out_bytes_file:
                out_bytes_file.write(out.getvalue())
            input_file.close()
            break
    return

if(__name__=='__main__'):
    f=open(inputfile, "rb")
    total_len=int(os.path.getsize(inputfile)*8)
    print(f'Total bits: {total_len}')
    out_file=io.BytesIO()
    start_time = time.time()
    sync = '72CB2EBAE79E5145E79C5149E7B451B9E5945D79CF14A27BCD18AE53E5E85C71C924B6DBB6D9B6D5B6FDB60DB42DB8ED926D6D6F6F63634B4BBBB99995557FFF'
    sync_marker=bin(int(sync, 16))[2:].zfill(int(len(sync)/2)*8)
    sync_buffer=str('0'*int(len(sync_marker)))
    mask=PN_mask_generator(mask=0x01)
    main(input_file=f, sync_buffer=sync_buffer, mask=mask, out=out_file, out_filename=outfile, total_len=total_len)
    print("--- %s seconds ---" % (time.time() - start_time)+str(' '*50))