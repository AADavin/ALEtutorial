import sys
import os
import argparse

def ale_splitter(rec_file, options):
    
    with open(rec_file) as f:
        
        lines = f.readlines()
        
        stree = lines[2].strip()
        ll = lines[6].strip().split()[-1]
        rates = lines[8].strip().split("\t")[1:]
        
        n_reconciled_trees = int(lines[9].strip().split()[0])
        reconciled_trees = lines[11:n_reconciled_trees + 11]
        n_of_events = lines[11 + n_reconciled_trees + 1].split("\t")[1:]
        table = lines[11 + n_reconciled_trees + 3:]             
    
    if options[0]:
        with open(rec_file.replace("uml_rec","stree"),"w") as f:
            f.write(stree.split("\t")[-1])
    if options[1]:
        with open(rec_file.replace("uml_rec","info"), "w") as f:
            f.write("LL:" + "\t" + ll + "\n")
            f.write("Dp:" + "\t" + rates[0] + "\n")
            f.write("Tp:" + "\t" + rates[1] + "\n")
            f.write("Lp:" + "\t" + rates[2] + "\n")
            f.write("De:" + "\t" + n_of_events[0] + "\n")
            f.write("Te:" + "\t" + n_of_events[1] + "\n")
            f.write("Le:" + "\t" + n_of_events[2] + "\n")
            f.write("Se:" + "\t" + n_of_events[3] + "\n")            
            
    if options[2]:
        with open(rec_file.replace("uml_rec","recs"),"w") as f:
            for t in reconciled_trees:
                f.write(t)
    if options[3]:
        with open(rec_file.replace("uml_rec","rec_table"), "w") as f:
            for e in table:
                f.write(e)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", help="Uml_rec file")    
    parser.add_argument("-s", help="Prints species tree to a different file", action='store_true', default = False)
    parser.add_argument("-f", help="Prints info about the family (LogLikelihood, probabilities and total number of events, to a different file", action='store_true', default=False)
    parser.add_argument("-t", help="Prints reconciliation table to a different file", action='store_true', default=False)
    parser.add_argument("-r", help="Prints reconciled gene trees to a different file", action='store_true', default = False)
    args = parser.parse_args()

    if args.i == None:
        print("use python ale_splitter.py -h to see options")
        print("you can run this script just with python ale_splitter -i XXXX.uml_rec")
        exit(0)

    ale_splitter(args.i, [args.s, args.f, args.t, args.r])

