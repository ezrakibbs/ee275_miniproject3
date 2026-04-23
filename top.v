`timescale 1ns / 1ps

module cache #(parameter CACHE_SIZEx = 16,   // 16KB, 32KB, 64KB, or 128KB
                         SET_ASSOCIx = 1,    // 1, 2, 4, 8
                         BLOCK_SIZEx = 16,   // 16B, 32B, 64B, 128B  // LRU, FIFO, Random
                         REPLACEMENTx = 1) 

                     (clk, reset, address);


  input wire clk;
  input wire reset;
  input wire [31:0] address;

  localparam NUM_SETSx = CACHE_SIZEx * 1024 / BLOCK_SIZEx / SET_ASSOCIx;

  reg [7:0] data_cache [CACHE_SIZEx * 1024:0];
  `include "functions.v"
  
  // figure out minimum number of bits needed to represent a number

endmodule