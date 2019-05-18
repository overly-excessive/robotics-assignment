indices_to_delete = [16, 17, 28, 29, 50, 78, 79, 80]

# delete rows from predicates.txt

predicates = []
# read in the file
with open("awa/predicates.txt") as pfile:
    for line in pfile:
        predicates.append(line[:-1])

# delete elements
for inx in reversed(indices_to_delete): # notice the use of reversed
    del predicates[inx]

# write the file
with open("awa/predicates.txt", 'w') as pfile:
    for pred in predicates:
        pfile.write(pred + "\n")

# delete columns from the predicate matrix
mlines = []

# read in matrix
with open("awa/predicate-matrix-binary.txt") as mfile:
    for line in mfile:
        mlines.append(line[:-1])

# delete elements:
new_mlines = []
for line in mlines:
    line = line.split(' ') # split the line on spaces
    for inx in reversed(indices_to_delete):
        del line[inx]
    new_line = " ".join(line) # join the list back to a string, space as separator
    new_mlines.append(new_line) # append it to the new list of matrix lines

# write into file
with open("awa/predicate-matrix-binary.txt", 'w') as mfile:
    for line in new_mlines:
        mfile.write(line + "\n")

