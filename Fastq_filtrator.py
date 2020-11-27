with open("amp_res_1.fastq", "r") as fastq:
    lin1 = fastq.readline().rstrip("\n")  # reading first string to start cycle
    while lin1 != "":  # fastq files ends by empty string, and we can use it for stop cycle
        lin2 = fastq.readline().rstrip("\n")  # reading second line with nucleotide
        l, k = fastq.readline(), fastq.readline()  # this strings are not needed for our code, but we should read them
        lin1 = fastq.readline().rstrip("\n")  # reading line for stop cycle if line is empty