import sys


fastq_file = str(sys.argv[-1])           # fastq is position file
file_list = sys.argv
min_length = 1                           # min Length for filtration
gc_counter = False                       # flag for gc_counter function
not_filtered_file = False                # flag for file where non-passed reads would be written
name_flag = False                        # flag to create name
max_gc_flag = False                      # flag to find out if the upper limit has been entered for sorting by GC

if "--min_length" in file_list:          # parsing and transformation variables
    i = file_list.index("--min_length")
    min_length = file_list[i + 1]
    min_length = int(min_length)
if "--keep_filtered" in file_list:
    not_filtered_file = True
if "--gc_bounds" in file_list:
    i = file_list.index("--gc_bounds")
    min_gc = float(file_list[i + 1])
    min_gc = int(min_gc)
    gc_counter = True
    try:
        max_gc = float(file_list[i + 2])
        max_gc = int(max_gc)
        max_gc_flag = True
    except ValueError:
        max_gc = min_gc
if "--output_base_name" in file_list:
    i = file_list.index("--output_base_name")
    file_name = file_list[i + 1]
    name_flag = True

# Name new files
if name_flag is False:
    file_name = fastq_file[:-6]
    good_name = file_name + "__passed.fastq"
    bad_name = file_name + "__failed.fastq"
else:
    good_name = file_name + "_passed.fastq"
    bad_name = file_name + "_failed.fastq"


# Filter line by length
def filtration_for_length(line_2, min_length):
    int_length = len(line_2)
    if int_length >= min_length:
        return True
    else:
        return False


# Filter line by GC%
def gc_counter_filter(line_2, min_gc, max_gc, max_gc_flag):
    total = len(line_2)
    c = line_2.count("C")
    g = line_2.count("G")
    gc_total = g + c
    gc_content = (gc_total / total) * 100
    if max_gc_flag:
        if min_gc <= gc_content <= max_gc:
            return True
        else:
            return False
    else:
        if min_gc <= gc_content:
            return True
        else:
            return False


# Write lines in new files
def writing_file(line_1, line_2, line_3, line_4, length_filter, gc_filter):
    if length_filter and gc_filter:
        good_file.write(line_1 + "\n")
        good_file.write(line_2 + "\n")
        good_file.write(line_3 + "\n")
        good_file.write(line_4 + "\n")
    elif not_filtered_file:
        bad_file.write(line_1 + "\n")
        bad_file.write(line_2 + "\n")
        bad_file.write(line_3 + "\n")
        bad_file.write(line_4 + "\n")


# Read fastq files
def fastq_reader(*args):
    with open(fastq_file, "r") as fastq:
        line_1 = fastq.readline().rstrip("\n")
        while line_1 != "":                           # An empty line will mean the end of the file and we end the loop
            line_2 = fastq.readline().rstrip("\n")  # Reading line with nucleotide sequence location
            line_3, line_4 = fastq.readline().rstrip("\n"), fastq.readline().rstrip("\n")  # Read the remaining lines
            length_filter = filtration_for_length(line_2, min_length)         # Launching third-party functions
            if gc_counter:                                                             # If we have True flag
                gc_filter = gc_counter_filter(line_2, min_gc, max_gc, max_gc_flag)     # function sort by GC%
            else:
                gc_filter = True                                                       # Otherwise we do not sort by GC%
            writing_file(line_1, line_2, line_3, line_4, length_filter, gc_filter)
            line_1 = fastq.readline().rstrip("\n")      # Reading new string line 1


# Create new files
if not_filtered_file:
    with open(good_name, "w") as good_file, open(bad_name, "w") as bad_file:
        fastq_reader(good_file, bad_file)
else:
    with open(good_name, "w") as good_file:
        fastq_reader(good_file)
