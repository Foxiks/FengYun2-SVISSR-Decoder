#include <iostream>
#include <fstream>
#include <vector>

#include "tclap/CmdLine.h"
#include "simpledeframer.h"

int main(int argc, char *argv[])
{
    TCLAP::CmdLine cmd("S-VISSR 2.0 Deframer by Egor UB1QBJ", ' ', "1.0");

    // File arguments
    TCLAP::ValueArg<std::string> valueInput("i", "input", "Raw input frames", true, "", "frames.bin");
    TCLAP::ValueArg<std::string> valueOutput("o", "output", "Output filename for frames", true, "", "out");

    // Register all of the above options
    cmd.add(valueInput);
    cmd.add(valueOutput);

    // Parse
    try
    {
        cmd.parse(argc, argv);
    }
    catch (TCLAP::ArgException &e)
    {
        std::cout << e.error() << '\n';
        return 0;
    }

    // Output and Input file
    std::ifstream data_in(valueInput.getValue(), std::ios::binary);
    std::ofstream data_out_msu_mr(valueOutput.getValue() + "-svissr.bin", std::ios::binary);

    // Read buffer
    uint8_t buffer[44356*4];

    // SVISSR data
    SimpleDeframer<uint64_t, 64, 44356 * 8, 0xC924B6DBB6D9B6D5, 0xB6FDB60DB42DB8ED, 0x926D6D6F6F63634B, 0x4BBBB99995557FFF> SVISSRDefra0;

    int SVISSR_frames0 = 0;
    int SVISSR_frames0_old = 0;
    std::cout << '\n';
    // Read until EOF
    while (!data_in.eof())
    {
        // Read buffer
        data_in.read((char *)buffer, sizeof(uint8_t) * (44356*4));

        std::vector<uint8_t> SVISSRData;
        SVISSRData.insert(SVISSRData.end(), buffer, buffer+(44356*4));

        // Deframe them all!
        std::vector<std::vector<uint8_t>> SVISSRFrames0 = SVISSRDefra0.work(SVISSRData);

        // Count them
        SVISSR_frames0 += SVISSRFrames0.size();

        // Write it out
        for (std::vector<uint8_t> &frame : SVISSRFrames0)
            for (uint8_t &byte : frame)
                data_out_msu_mr.put(byte);
            if(SVISSR_frames0>SVISSR_frames0_old){
                std::cout << "SVISSR Frames " << SVISSR_frames0 << std::endl;
                SVISSR_frames0_old = SVISSR_frames0;
            }
    }

    data_in.close();
    data_out_msu_mr.close();
}
