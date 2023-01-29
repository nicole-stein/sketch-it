import csv
import hashlib

def read_csv(filename):
        out = []
        with open(filename, "r") as f:
            r = csv.reader(f)
            for l in r:
                out.append(l)
        return out

def write_csv(filename, content):
    with open(filename, "w") as f:
        w = csv.writer(f)
        for l in content:
            w.writerow(l)
    return read_csv(filename)

def clear_csv(filename):
    with open(filename, "r+") as f:
        f.truncate(0)

def read_file(filename):
    out = []
    with open(filename, "r") as f:
        for line in f:
            out.append(line)
    return out