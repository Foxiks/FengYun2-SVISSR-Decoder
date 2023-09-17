# FengYun2-SVISSR-Decoder
### This is a decoder of images from the de-randomized transport frames of the FengYun-2 series satellites.
![1](https://github.com/Foxiks/FengYun2-SVISSR-Decoder/blob/main/img/0out.gif)

## How to use
To use this decoder, you need to use FengYun-2 satellite transport frames. This is very easy to get with the GNU-Radio schema from this repository. After receiving the transport frames, they need to be synchronized and de-randomized.

Use: 
```sh
Deframer.exe(.py) data_from_GR.bin fengyun_svissr.svissr 
```
To use the decoder, use the command:
```sh
python3 decoder.py -i fengyun_svissr.svissr
```
...or if you're using Windows:
```sh
FengYun-2_S-VISSR_Decoder.exe -i fengyun_svissr.svissr
```
You will get decoded images in decoder folder.

## Examples (Decoded Images)
![2](https://github.com/Foxiks/FengYun2-SVISSR-Decoder/blob/main/img/ch01.png)
![3](https://github.com/Foxiks/FengYun2-SVISSR-Decoder/blob/main/img/ch2.png)
![4](https://github.com/Foxiks/FengYun2-SVISSR-Decoder/blob/main/img/ch3.png)
![5](https://github.com/Foxiks/FengYun2-SVISSR-Decoder/blob/main/img/ch4.png)
![6](https://github.com/Foxiks/FengYun2-SVISSR-Decoder/blob/main/img/VIS.png)
