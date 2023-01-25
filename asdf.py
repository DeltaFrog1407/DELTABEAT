with open('child.txt', 'r') as file:
    lines_final = []
    lines = []
    line = file.readline()
    list_line = line.split()
    for i in list_line:
        a = int(i)
        lines.append(a)
    lines_final.append(lines)
    lines = []
    while line != '':
        line = file.readline()
        list_line = line.split()
        for i in list_line:
            a = int(i)
            lines.append(a)
        if not list_line:
            break
        lines_final.append(lines)
        lines = []
print(lines_final)
