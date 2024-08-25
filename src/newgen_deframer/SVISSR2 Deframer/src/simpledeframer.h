#pragma once

/*
    An arbitrary deframer
*/

#include <vector>
#include <array>
#include <cstdint>
//#include "ccsds.h"
#define MAX_ERROR 7


template <typename SYNC_T, int SYNC_SIZE, int FRAME_SIZE, SYNC_T ASM_SYNC0, SYNC_T ASM_SYNC1, SYNC_T ASM_SYNC2, SYNC_T ASM_SYNC3>
class SimpleDeframer
{
private:
    // Main shifter
    int SKIP = 0;
    SYNC_T shifter;
    // Small function to push a bit into the frame
    void pushBit(uint8_t bit);
    // Framing variables
    uint8_t byteBuffer;
    bool writeFrame;
    uint8_t errs;
    int wroteBits, outputBits, skipCount;
    std::vector<uint8_t> frameBuffer;

public:
    SimpleDeframer();
    std::vector<std::vector<uint8_t>> work(std::vector<uint8_t> &data);
};