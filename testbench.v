`timescale 1ns / 1ps

module name;
    // universal inputs
    reg clk;
    reg reset;

    
    // clk generation
    initial
    begin
        clk = 0;
        reset = 1;
        #5
        reset = 0;
    end

    always 
    begin
        #10
        clk = ~clk;
    end

    initial
    begin

        #500
        $finish;
    end
endmodule







