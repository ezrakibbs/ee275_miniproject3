import math
import random

def main():
    ADDRESS_LENGTH_BITS = 32
    # take inputs from user
    # CACHE_SIZEx = 16,   // 16KB, 32KB, 64KB, or 128KB
    # SET_ASSOCIx = 1,    // 1, 2, 4, 8
    # BLOCK_SIZEx = 16,   // 16B, 32B, 64B, 128B  
    # REPLACEMENTx = 1    // LRU, FIFO, RANDOM
    default = "y"
    #default = str(input("Do you want to use the default settings? (y/n): "))
    CACHE_SIZE = 32
    SET_ASSOCIATIVITY = 1
    BLOCK_SIZE = 32
    REPLACEMENT = "LRU"
    FULLY_ASSOCIATIVE = 0
    if default == "y":
        pass
    else:
        CACHE_SIZE = int(input("Enter cache size (16, 32, 64, or 128 KB): "))
        while CACHE_SIZE not in (16, 32, 64, 128):
            CACHE_SIZE = int(input("Try again. Enter cache size (16, 32, 64, or 128 KB): "))

        SET_ASSOCIATIVITY = int(input("Enter set associativity (1, 2, 4, 8 or 0 for Fully Associative): "))
        while SET_ASSOCIATIVITY not in (1, 2, 4, 8, 0):
            SET_ASSOCIATIVITY = int(input("Try again. Enter set associativity (1, 2, 4, 8 or 0 for Fully Associative): "))

        BLOCK_SIZE = int(input("Enter block size (16, 32, 64, or 128 B): "))
        while BLOCK_SIZE not in (16, 32, 64, 128):
            BLOCK_SIZE = int(input("Try again. Enter block size (16, 32, 64, or 128 B): "))

        REPLACEMENT = str((input("Enter replacement policy (LRU, FIFO, RANDOM): ")))
        while REPLACEMENT not in ("LRU", "FIFO", "RANDOM"):
            REPLACEMENT = str((input("Try again. Enter replacement policy (LRU, FIFO, RANDOM): ")))
        
    print("Cache Size is: " + str(CACHE_SIZE) + "KB")
    print("Set Associativity: " + str(SET_ASSOCIATIVITY))
    print("Block Size is: " + str(BLOCK_SIZE) + "B")
    if(SET_ASSOCIATIVITY == 1):
        REPLACEMENT = "RANDOM"
        # since set assoc == 1, this is direct mapped cache. replacement policy is set to RANDOM because this covers direct mapped case
    elif(SET_ASSOCIATIVITY == 0):
        FULLY_ASSOCIATIVE = 1
        SET_ASSOCIATIVITY = 1
        pass
    print("Replacement Policy is: " + str(REPLACEMENT))

    # read inputs from file

    # determine the number of sets
    NUM_SETS = int(CACHE_SIZE * 1024 / BLOCK_SIZE / SET_ASSOCIATIVITY)

    # determine number of bits for sets
    SET_BIT_WIDTH = int(math.log2(NUM_SETS))
    if FULLY_ASSOCIATIVE:
        SET_BIT_WIDTH = 0

    # determine number of bits for block
    BLOCK_BIT_WIDTH = int(math.log2(BLOCK_SIZE))

    # determine tag array size
    TAG_LENGTH = NUM_SETS * SET_ASSOCIATIVITY
    TAG_BIT_WIDTH = ADDRESS_LENGTH_BITS - SET_BIT_WIDTH - BLOCK_BIT_WIDTH

    print("\nNumber of Sets: " + str(NUM_SETS))
    print("Bits for Sets: " + str(SET_BIT_WIDTH))
    print("Bits for Blocks: " + str(BLOCK_BIT_WIDTH))
    print("Tag Array Length (Entries): " + str(TAG_LENGTH))
    print("Tag Bits: " + str(TAG_BIT_WIDTH))

    # tag array creation
    tag_array = []
    for _ in range(NUM_SETS): # rows
        row = []
        for _ in range(SET_ASSOCIATIVITY):  # columns
            row.append(0)
        tag_array.append(row)

    print("\nta length : " + str(len(tag_array)))
    print("ta columns: " + str(len(tag_array[0])))

    # copy of tag array to keep track of LRU
    LRU_array = []
    if REPLACEMENT == "LRU":
        for j in range(NUM_SETS): # rows
            row = []
            if FULLY_ASSOCIATIVE:
                row.append(j)
                LRU_array.append(row)
            else:
                for i in range(SET_ASSOCIATIVITY):  # columns
                    row.append(i)
                LRU_array.append(row)

    # FIFO array 
    FIFO_array = [0] * NUM_SETS
    FIFO_index = 0

    # data cache creation
    data_cache = []
    for _ in range(NUM_SETS): # rows
        row = []
        for _ in range(SET_ASSOCIATIVITY):  # columns
            row.append(0)
        data_cache.append(row)

    print("\ndc length : " + str(len(data_cache)))
    print("dc columns: " + str(len(data_cache[0])))

    # read address trace
    file = open("addr_trace.txt")
    current_address_decimal = 0
    total_hits = 0
    total_miss = 0
    for line in file:
        # read in the address trace line by line
        # and convert it to an integer and then convert it into a binary string
        previous_integer = current_address_decimal
        current_integer = int(line)
        current_address_decimal = current_integer + previous_integer
        current_address_binary_string = format(current_address_decimal, "b")

        # append 0s to the front in order to make sure that the length is 32 bits
        while len(current_address_binary_string) != ADDRESS_LENGTH_BITS:
            current_address_binary_string = '0' + current_address_binary_string
        
        # partition block bits, set bits, and tag bits
        # MSB correspond to index 0 so we have to offset with ADDRESS_LENGTH_BITS
        # string[start:stop] start is inclusive; stop is exclusive
        # once partitioned, we convert the bits string into integer to be used as indices for array (i.e. tag)
        block_bits = current_address_binary_string[ADDRESS_LENGTH_BITS - BLOCK_BIT_WIDTH : ADDRESS_LENGTH_BITS]
        if not FULLY_ASSOCIATIVE:
            set_bits = current_address_binary_string[ADDRESS_LENGTH_BITS - BLOCK_BIT_WIDTH - SET_BIT_WIDTH : ADDRESS_LENGTH_BITS - BLOCK_BIT_WIDTH]
            set_bits_decimal = int(set_bits, 2)
        tag_bits = current_address_binary_string[0 : ADDRESS_LENGTH_BITS - BLOCK_BIT_WIDTH - SET_BIT_WIDTH]
        tag_bits_decimal = int(tag_bits, 2)

        # print("hello")
        # sys.exit()

        # go through tag array to see if there is a tag match
        hit = 0
        hit_index = 0
        for i in range(SET_ASSOCIATIVITY):
            if FULLY_ASSOCIATIVE:
                for j in range(NUM_SETS):
                    if tag_array[j][i] == tag_bits_decimal:
                        hit = 1
                        hit_index = j
            else:
                if tag_array[set_bits_decimal][i] == tag_bits_decimal:
                    hit = 1
                    hit_index = i
        
        if hit: # cache hit     
            total_hits = total_hits + 1     # increment total hits
            if REPLACEMENT == "RANDOM":     # do nothing for hit when replacement is RANDOM
                pass    

            elif REPLACEMENT == "LRU":      # need to update which tag is LRU for hit case
                if FULLY_ASSOCIATIVE:
                    temp = LRU_array[hit_index][0]
                    for i in range(NUM_SETS):
                        curr_value = LRU_array[i][0]
                        if curr_value == temp:
                            LRU_array[i][0] = 0
                        elif curr_value < temp:
                            LRU_array[i][0] += 1
                else:
                    temp = LRU_array[set_bits_decimal][hit_index]
                    for i in range(SET_ASSOCIATIVITY):
                        curr_value = LRU_array[set_bits_decimal][i]
                        if curr_value == temp:
                            LRU_array[set_bits_decimal][i] = 0
                        elif curr_value < temp:
                            LRU_array[set_bits_decimal][i] += 1

            elif REPLACEMENT == "FIFO":
                pass
            
        else:   # cache miss
            total_miss = total_miss + 1
            if REPLACEMENT == "RANDOM":     # replace a random tag on a miss
                if FULLY_ASSOCIATIVE:
                    replace_index = random.randint(0, NUM_SETS - 1)
                    tag_array[replace_index][0] = tag_bits_decimal
                else:
                    replace_index = random.randint(0, SET_ASSOCIATIVITY - 1)
                    tag_array[set_bits_decimal][replace_index] = tag_bits_decimal
            
            elif REPLACEMENT == "LRU":      # replace LRU tag
                if FULLY_ASSOCIATIVE:
                    for i in range(NUM_SETS):
                        if(LRU_array[i][0] == (NUM_SETS - 1)):
                            LRU_array[i][0] = 0
                            tag_array[i][0] = tag_bits_decimal
                        else:
                            LRU_array[i][0] += 1
                else:
                    for i in range(SET_ASSOCIATIVITY):
                        if(LRU_array[set_bits_decimal][i] == (SET_ASSOCIATIVITY - 1)):
                            LRU_array[set_bits_decimal][i] = 0
                            tag_array[set_bits_decimal][i] = tag_bits_decimal
                        else:
                            LRU_array[set_bits_decimal][i] += 1
            
            elif REPLACEMENT == "FIFO":     # replace oldest entry
                if FULLY_ASSOCIATIVE:
                    tag_array[FIFO_index][0] = tag_bits_decimal
                    FIFO_index += 1
                    if FIFO_index >= NUM_SETS:
                        FIFO_index = 0                   
                else:
                    replace_index = FIFO_array[set_bits_decimal]
                    tag_array[set_bits_decimal][replace_index] = tag_bits_decimal
                    FIFO_array[set_bits_decimal] += 1
                    if(FIFO_array[set_bits_decimal] >= SET_ASSOCIATIVITY):
                        FIFO_array[set_bits_decimal] = 0

    

    print("\n\nTotal hits: " + str(total_hits))
    print("Total miss: " + str(total_miss))
    print("Total addresses: " + str(total_hits + total_miss))
    miss_rate = total_miss / (total_miss + total_hits) * 100
    print("Miss rate: " + str(miss_rate) + str(" %"))
    hit_rate = total_hits / (total_miss + total_hits) * 100
    print("Hit rate: " + str(hit_rate) + str(" %"))

    file.close()


if __name__ == "__main__":
    main()