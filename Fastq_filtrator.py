import sys
fasta = str(sys.argv[-1])
counter = 1
min_length = 1
gc_counter = False
not_filtered_file = False
name_flag = False

for i in range(counter, len(sys.argv)):
    if sys.argv[i] == "--min_length":
        min_length = sys.argv[i+1]
        counter = i+1
    elif sys.argv[i] == "--keep_filtered":
        not_filtered_file = True
    elif sys.argv[i] == "--gc_bounds":
        min_gc = float(sys.argv[i+1])
        counter = i+1
        gc_counter = True
        try:
            max_gc = float(sys.argv[i+2])
            counter = i + 2
        except ValueError:
            max_gc = min_gc
            continue
    elif sys.argv[i] == "--output_base_name":
        file_names = sys.argv[i+1]
        counter = i + 1
        name_flag = True

if name_flag == False:
    file_names = fasta[:-6]
    good_name = file_names + "_passed"
    bad_name = file_names + "_faild"
else:
    good_name = file_names + "_passed.fastq"
    bad_name = file_names + "_faild.fastq"

if not_filtered_file == True:
    good_file = open(good_name, "w")
    bad_file = open(bad_name, "w")
else:
    good_file = open(good_name, "w")



def filtration_for_lengt(lin1, min_length):
    int_length = int(lin1.split("=")[1])
    min_length = int(min_length)
    if int_length >= min_length:
        return True
    else:
        return False

def gc_counter_filter(lin2, min_gc, max_gc):
    min_gc = int(min_gc)
    max_gc = int(max_gc)
    total = len(lin2)
    c = lin2.count("C")
    g = lin2.count("G")
    gc_total = g + c
    gc_content = (gc_total/total)*100
    if max_gc == min_gc:
        if min_gc <= gc_total:
            return True
        else:
            return False
    else:
        if min_gc <= gc_total <= max_gc:
            return True
        else:
            return False



with open(fasta, "r") as fastq:
    lin1 = fastq.readline().rstrip("\n")  # reading first string to start cycle
    while lin1 != "":  # fastq files ends by empty string, and we can use it for stop cycle
        lin2 = fastq.readline().rstrip("\n")  # reading second line with nucleotide
        l, k = fastq.readline().rstrip("\n"), fastq.readline().rstrip("\n")  # this strings are not needed for our code, but we should read them
        length_filter = filtration_for_lengt(lin1, min_length)
        if  gc_counter == True:
            gc_filter = gc_counter_filter(lin2, min_gc, max_gc)
        else:
            gc_filter = True
        if not_filtered_file == True:
            if length_filter == True and gc_filter == True:
                good_file.write(lin1 + "\n")
                good_file.write(lin2 + "\n")
                good_file.write(l + "\n")
                good_file.write(k + "\n")
            else:
                bad_file.write(lin1 + "\n")
                bad_file.write(lin2 + "\n")
                bad_file.write(l + "\n")
                bad_file.write(k + "\n")
        else:
            if length_filter == True and gc_filter == True:
                good_file.write(lin1 + "\n")
                good_file.write(lin2 + "\n")
                good_file.write(l + "\n")
                good_file.write(k + "\n")
            else:
                pass
        lin1 = fastq.readline().rstrip("\n")  # reading line for stop cycle if line is empty

if not_filtered_file == True:
    good_file.close()
    bad_file.close()
else:
    good_file.close()

