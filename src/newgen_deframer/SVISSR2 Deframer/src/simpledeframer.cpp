#include "simpledeframer.h"
#include "svissr_derand.h"

#include <math.h>

fengyun_svissr::PNDerandomizer derand;

// Returns the asked bit!
template <typename T>
inline bool getBit(T &data, int &bit)
{
    return (data >> bit) & 1;
}

template <typename TMarker, typename TMarkerTest>
inline uint8_t checkSyncMarker(TMarker marker, TMarkerTest &totest)
{
    uint8_t errors = 0;
    for (int i = 63; i >= 0; i--)
    {
        bool markerBit, testBit;
        markerBit = getBit<TMarker>(marker, i);
        testBit = getBit<TMarkerTest>(totest, i);
        if (markerBit != testBit)
            errors++;

        if (errors > MAX_ERROR)
            return errors;
    }
    return errors;
}

template <typename SYNC_T, int SYNC_SIZE, int FRAME_SIZE, SYNC_T ASM_SYNC0, SYNC_T ASM_SYNC1, SYNC_T ASM_SYNC2, SYNC_T ASM_SYNC3>
SimpleDeframer<SYNC_T, SYNC_SIZE, FRAME_SIZE, ASM_SYNC0, ASM_SYNC1, ASM_SYNC2, ASM_SYNC3>::SimpleDeframer()
{
    // Default values
    writeFrame = false;
    wroteBits = 0;
    outputBits = 0;
}

// Write a single bit into the frame
template <typename SYNC_T, int SYNC_SIZE, int FRAME_SIZE, SYNC_T ASM_SYNC0, SYNC_T ASM_SYNC1, SYNC_T ASM_SYNC2, SYNC_T ASM_SYNC3>
void SimpleDeframer<SYNC_T, SYNC_SIZE, FRAME_SIZE, ASM_SYNC0, ASM_SYNC1, ASM_SYNC2, ASM_SYNC3>::pushBit(uint8_t bit)
{
    byteBuffer = (byteBuffer << 1) | bit;
    wroteBits++;
    if (wroteBits == 8)
    {
        frameBuffer.push_back(byteBuffer);
        wroteBits = 0;
    }
}

template <typename SYNC_T, int SYNC_SIZE, int FRAME_SIZE, SYNC_T ASM_SYNC0, SYNC_T ASM_SYNC1, SYNC_T ASM_SYNC2, SYNC_T ASM_SYNC3>
std::vector<std::vector<uint8_t>> SimpleDeframer<SYNC_T, SYNC_SIZE, FRAME_SIZE, ASM_SYNC0, ASM_SYNC1, ASM_SYNC2, ASM_SYNC3>::work(std::vector<uint8_t> &data)
{
    // Output buffer
    std::vector<std::vector<uint8_t>> framesOut;

    // Loop in all bytes
    for (uint8_t &byte : data)
    {
        // Loop in all bits!
        for (int i = 7; i >= 0; i--)
        {
            // Get a bit, push it
            uint8_t bit = getBit<uint8_t>(byte, i);

            if (sizeof(SYNC_T) * 8 != SYNC_SIZE)
                shifter = ((shifter << 1) % (long)pow(2, SYNC_SIZE)) | bit;
            else
                shifter = (shifter << 1) | bit;

            // Writing a frame!
            if (writeFrame)
            {
                // First run : push header
                // Это нам не нужно
                /*
                if (outputBits == 0)
                {
                    SYNC_T syncAsm = ASM_SYNC;
                    for (int y = SYNC_SIZE - 1; y >= 0; y--)
                    {
                        pushBit(getBit<SYNC_T>(syncAsm, y));
                        outputBits++;
                    }
                }*/

                // Push current bit
                if(SKIP)
                {
                    if(skipCount<SKIP) skipCount++;
                    else
                    {
                        pushBit(bit);
                        outputBits++;
                    }
                }
                else
                {
                    pushBit(bit);
                    outputBits++;
                }

                // Once we wrote a frame, exit!
                if (outputBits == FRAME_SIZE)
                {
                    writeFrame = false;
                    skipCount=0;
                    wroteBits = 0;
                    outputBits = 0;
                    derand.derandData(frameBuffer.data(), 44356);
                    framesOut.push_back(frameBuffer);
                    frameBuffer.clear();
                }

                continue;
            }

            // Find SYNC!

            errs=checkSyncMarker(ASM_SYNC0, shifter);
            if (errs <= MAX_ERROR)
            {
                skipCount=0;
                writeFrame = true;
                SKIP = (64*3);
            } else
            {
                errs=checkSyncMarker(ASM_SYNC1, shifter);
                if (errs <= MAX_ERROR)
                {
                    skipCount=0;
                    writeFrame = true;
                    SKIP = (64*2);
                } else
                {
                    errs=checkSyncMarker(ASM_SYNC2, shifter);
                    if (errs <= MAX_ERROR)
                    {
                        skipCount=0;
                        writeFrame = true;
                        SKIP = 64;
                    } else
                    {
                        errs=checkSyncMarker(ASM_SYNC3, shifter);
                        if (errs <= MAX_ERROR)
                        {
                            skipCount=0;
                            writeFrame = true;
                            SKIP = 0;
                        }
                    }
                }
            }

        }
    }

    // Output what we found if anything
    return framesOut;
}

// Build this template for SVISSR2-0 data in 0 state
template class SimpleDeframer<uint64_t, 64, 44356 * 8, 0xC924B6DBB6D9B6D5, 0xB6FDB60DB42DB8ED, 0x926D6D6F6F63634B, 0x4BBBB99995557FFF>;