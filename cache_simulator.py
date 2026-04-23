import math

def main():
    print("hello")
    ADDRESS_LENGTH_BITS = 32
    # take inputs from user
    # CACHE_SIZEx = 16,   // 16KB, 32KB, 64KB, or 128KB
    # SET_ASSOCIx = 1,    // 1, 2, 4, 8
    # BLOCK_SIZEx = 16,   // 16B, 32B, 64B, 128B  
    # REPLACEMENTx = 1    // LRU, FIFO, RANDOM
    default = "y"
    #default = str(input("Do you want to use the default settings? (y/n): "))
    if default == "y":
        CACHE_SIZE = 16
        SET_ASSOCIATIVITY = 2
        BLOCK_SIZE = 16
        REPLACEMENT = "RANDOM"
    else:
        CACHE_SIZE = int(input("Enter cache size (16, 32, 64, or 128 KB): "))
        while CACHE_SIZE not in (16, 32, 64, 128):
            CACHE_SIZE = int(input("Try again. Enter cache size (16, 32, 64, or 128 KB): "))

        SET_ASSOCIATIVITY = int(input("Enter set associativity (1, 2, 4, or 8): "))
        while SET_ASSOCIATIVITY not in (1, 2, 4, 8):
            SET_ASSOCIATIVITY = int(input("Try again. Enter set associativity (1, 2, 4, or 8): "))

        BLOCK_SIZE = int(input("Enter block size (16, 32, 64, or 128 B): "))
        while BLOCK_SIZE not in (16, 32, 64, 128):
            BLOCK_SIZE = int(input("Try again. Enter block size (16, 32, 64, or 128 B): "))

        REPLACEMENT = str((input("Enter replacement policy (LRU, FIFO, RANDOM): ")))
        while REPLACEMENT not in ("LRU", "FIFO", "RANDOM"):
            REPLACEMENT = str((input("Try again. Enter replacement policy (LRU, FIFO, RANDOM): ")))
        
    print("Cache Size is: " + str(CACHE_SIZE) + "KB")
    print("Set Associativity: " + str(SET_ASSOCIATIVITY))
    print("Block Size is: " + str(BLOCK_SIZE) + "B")
    print("Replacement Policy is: " + str(REPLACEMENT))

    # read inputs from file

    # determine the number of sets
    # number of sets = cache size / block size / set associativity
    NUM_SETS = int(CACHE_SIZE * 1024 / BLOCK_SIZE / SET_ASSOCIATIVITY)

    # determine number of bits for sets
    # number of bits for sets = log base 2 of number of sets
    SET_BIT_WIDTH = int(math.log2(NUM_SETS))

    # determine number of bits for block
    # number of bits for block = log base 2 of block size
    BLOCK_BIT_WIDTH = int(math.log2(BLOCK_SIZE))

    # create tag array
    # width is number of bits (32 - number of bits for set and block)
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


    # data cache creation
    data_cache = []
    for _ in range(NUM_SETS): # rows
        row = []
        for _ in range(SET_ASSOCIATIVITY):  # columns
            row.append(0)
        data_cache.append(row)

    print("\ndc length : " + str(len(data_cache)))
    print("dc columns: " + str(len(data_cache[0])))



















if __name__ == "__main__":
    main()