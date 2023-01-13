import bitstring, time, binascii, os, cv2, numpy, argparse, gc
start_time = time.time()
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="Input binary file")
args = parser.parse_args()
inp = args.input
width = 44356
line=0
back_line=0
up_line=88712
if(__name__ == "__main__"):
    print("""
                                        .!!J7!~~^:..                                                
                                       ~JJJ??????JJJJ?!^:.                                          
                                     :7??77?????JJJJYY5555J?!:                                      
                                   .~??777???J??JYJJYYYY55GB#BG57:                                  
                                  :??777????JJJJYJJJYYY55GBBBBB#&&B5~.                              
                                .!J?777????JJJJJJJJYYJJ5GBBGGBB###&&&#G7.                           
                               :?J777?????JJJJJJJYYJJJYGBBGPGB###&&&&&&@&G!.                        
                             .~??77???JJJJJJJJJJJYJJJJPGGPPG#####&&&&&&&&@@&5:                      
                           :...~!:.:^!7?JJJJJJ????JJYPGP5PG###&&&&&&&&&&&@@@@@#7                    
                         .:^. .7G5^ .  ..^~7??????JYYPP5PB####&&&&&&&&&&@@@@@@@@&?.                 
                        ^~~!77!~?J^..  ~Y~  ..^!7JY55PPGB####&&&&&&&&&&&@@@@@@@@@@&J.               
                      .~~!??JJJYJYYJ7~:...      .:!JPGGB####&&&&&&&&&&@@@@@@@@@@@@@@&?              
                    .^~~!??JJJYJJYYJJJJ?7~:.       .!YPB###&&&&&&&&&&@@@@@@@@@@@@@@@@@B:            
                   :~~~7?JJJJYYYYJJJ????????7~:.. :!7!7JPB&&&&&&&&&&@@@@@@@@@@@@@@@@@@@&!           
                 .~!~7?JJJJYYYYYJJJ??????????JYJ77?777?Y5PGB#&&&&&&@@@@@@@@@@@@@@@@@@&&&&?          
                ^~~7?JJJYYYYYYYJJJJ?????????JJYY5GBGP55PGGGGBB#&&@@@@@@@@@@@@@@@@@@@&&&&&&!         
              .~~!?JJJYYYYYYYYYJJJJ????????JYY55GB####&#BGGB&&#B#&@@@@@@@@@@@@@@@&&&&#&&&&B         
             :~!7JJJYYY55555YYYJJJJJ?????J?YY5PGB####&&&&&#B##&BB##&@@@@@@@@@@@@&&&####&&@P         
           .!!!7?JYYY5555P55YYYJJJJJ??JJJJY55PB####&&&&&&&&&&&#B###&&&@@@@@@@@&&&&####&&&J          
           7J??????JJYY5P555YYYJJJJJJJJ?JY55G####&&&&&&&&&&&@@&&&&&&&&&&&@@@&&&&#####&&#~              
           .~??????JJJJ??JJYYYYYJJJJY?JY55PBB###&&&&&&&&&&&&&&@@@@&&&&&#B#&&&&&#####&&5.            
             :?J??77??JYJJ???7?JJYYJ?J555PB###&&&&&&&&&&&&&&&@@@@@@@@&#BBGGB######&&#7              
               ^?J??????JJJJJJ???JJY5PPPB####&&&&&&&&&&&&&@@@@@@@@@@@@&BGGP5PB###&&B:               
                 :?YJJ????JJJJJYYJ77YPG####&&&&&&&&&&&@@&@@@@@@@@@@@@@@&#P5555B#&&J                 
                   :7JYJJJ??JJYJ7!^^^!5B#&&&&&&&&&&&&@@@@@@@@@@@@@@@@&&&@&GPPGG&#~                  
                     .!?JJJJJ??7^:^~~!?YPB#&&&&&&&&@@@@@@@@@@@@@@@@&&&@@@@&BG#&5.                   
                        .!?J7~^.  .:7JY5PPGGB#&&&&@@@@@@@@@@@@@@@@&&&@@@@@@&&#7                     
                          .^!^.     ~YPGGGGGGGGB&@@@@@@@@@@@@@@@&&&@@@@@@@@&B:                      
                           .~.    .!J5B##BBGGG5JYP#@@@@@@@@@@@&&&&&&@@@@@@&Y.                       
                           ~.    .7YGB##BGPPBGYJJJJ5B&@@@@@@@@@&&&&&&&@@@&!                         
            .~~!~^7YPGP^  ::    ^JPB##BG55PPGGYJJJJJJJP&@@@@@&&&&&&&&&&@B:                          
           ^^~^:!GG#PP&G  ^^^..!5B##BP5PPGP5YYYJJJJJYYJJ5B&@@&&&#&##&&&Y                            
          ~^^~:J#GPBPG#G..~J^:JG##BPPP5?:.~?YYYYJJJJJYYYYJ5B&&&####&&&~                             
         ~!~?.Y#GGPG5GB5!7PY?P##BGP5?:      .^!JYYJJJJJJYYYJYG#&##&&G.                              
         ~7!~7#GGBG55JJ77YGG##BGP7:             .~7YYYJJJJJJYY5G#&&?                                
          :7!PGGPGBGBGPJ?!!JYY5J7. ~YY?~:.          .^!7JJJYJJY5#B:                                 
             ?BBBBG?^!Y5YYJJJ!~!!75PPPG#BG.              .^~7???!.                                  
              ^77^.   :5Y75BBGBJ?!!!?5P#PG^                 :.                                      
                     .JJ.  .7G5JY!Y5?!JBPB.                                                         
                    :Y?      ^7?^5BGBB#PG7                                                          
                   ^Y~       !Y7JGGBB#PGJ                                                           
                  ^?.       .JJ?GBB##GG!                                                            
                 ~!          ?5Y###BG5^                                                             
                ~^            :~PBGY^                                                               
              :?^                                                                                   
             !J:                                                                                    
            .!.                                                                                     
    """)

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
        l = int(size)/int(width)
    bbyteArray = bytearray(f)
    grayImage = numpy.array(bbyteArray).reshape(int(l), int(width))
    print("Saving IR ch1...")
    crop_img1 = grayImage[0:int(l), 2552:4846]
    cv2.imwrite('ch1.png', crop_img1)
    print("Saving IR ch2...")
    crop_img2 = grayImage[0:int(l), 5102:7396]
    cv2.imwrite('ch2.png', crop_img2)
    print("Saving IR ch3...")
    crop_img3 = grayImage[0:int(l), 7653:9947]
    cv2.imwrite('ch3.png', crop_img3)
    del crop_img1
    del crop_img2
    del crop_img3
    gc.collect()
    with open(inp, "rb") as ts_all:
        frames = ts_all.read().hex()
        size = os.path.getsize(inp)
        l = int(size)/int(44356)
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
        with open('chunks.1', 'ab') as f1:
            f1.write(binascii.unhexlify(chunks1))
        with open('chunks.2', 'ab') as f2:
            f2.write(binascii.unhexlify(chunks2))
        with open('chunks.3', 'ab') as f3:
            f3.write(binascii.unhexlify(chunks3))
        with open('chunks.4', 'ab') as f4:
            f4.write(binascii.unhexlify(chunks4))
        with open('ir10.ch', 'ab') as f4:
            f4.write(binascii.unhexlify(ir10))
        line+=1
    print('Convert VIS Chunk 1 to 8-bit pattern...')
    file1 = open('chunks.1', 'rb').read()
    b = bitstring.BitStream(file1).bin
    chunks = [b[i:i+6] for i in range(0, len(b), 6)]
    chunks = [str+'00' for str in chunks]
    del b
    del file1
    gc.collect()
    print('Convert VIS Chunk 2 to 8-bit pattern...')
    file2 = open('chunks.2', 'rb').read()
    b1 = bitstring.BitStream(file2).bin
    chunks1 = [b1[i:i+6] for i in range(0, len(b1), 6)]
    chunks1 = [str+'00' for str in chunks1]
    del b1
    del file2
    gc.collect()
    print('Convert VIS Chunk 3 to 8-bit pattern...')
    file3 = open('chunks.3', 'rb').read()
    b2 = bitstring.BitStream(file3).bin
    chunks2 = [b2[i:i+6] for i in range(0, len(b2), 6)]
    chunks2 = [str+'00' for str in chunks2]
    del b2
    del file3
    gc.collect()
    print('Convert VIS Chunk 4 to 8-bit pattern...')
    file4 = open('chunks.4', 'rb').read()
    b3 = bitstring.BitStream(file4).bin
    chunks3 = [b3[i:i+6] for i in range(0, len(b3), 6)]
    chunks3 = [str+'00' for str in chunks3]
    del b3
    del file4
    gc.collect()
    print('Mixing VIS Chunks...')
    res = [x for y in zip(chunks, chunks1, chunks2, chunks3) for x in y]
    with open('data.mixed', 'wb') as file:
        bitstring.BitArray(bin=''.join(res)).tofile(file)
    del res
    del chunks
    del chunks1
    del chunks2
    del chunks3
    gc.collect()
    with open('data.mixed', "rb") as image:
        f = image.read()
    bbyteArray = bytearray(f)
    grayImage = numpy.array(bbyteArray).reshape(int(l), int(36672))
    print("Saving VIS...")
    cv2.imwrite('VIS.png', grayImage)
    src = cv2.imread('VIS.png', cv2.IMREAD_UNCHANGED)
    re = cv2.resize(src, (9168, int(l*4)))
    cv2.imwrite('VIS.png', re)
    print("Read IR ch. 10-bit...")
    file5 = open('ir10.ch', 'rb').read()
    b4 = bitstring.BitStream(file5).bin
    chunks10 = [b4[i:i+10] for i in range(0, len(b4), 10)]
    chunks10 = [str[:-2] for str in chunks10]
    del b4
    gc.collect()
    with open('ir10.bit', 'wb') as file:
        bitstring.BitArray(bin=''.join(chunks10)).tofile(file)
    del chunks10
    gc.collect()
    with open('ir10.bit', "rb") as image:
        f = image.read()
    bbyteArray = bytearray(f)
    grayImage = numpy.array(bbyteArray).reshape(int(l), int(2300))
    print("Saving IR ch. 10-bit...")
    cv2.imwrite('ch4.png', grayImage)    
    print("Done!")
    print(str(time.time()-start_time))
    os.remove('chunks.1')
    os.remove('chunks.2')
    os.remove('chunks.3')
    os.remove('chunks.4')
    os.remove('data.mixed')
    os.remove('ir10.bit')
    os.remove('ir10.ch')