import sys
import os
import argparse

def ale_parser(rec_folder, options):
    
    rec_files = [x for x in os.listdir(rec_folder) if x.endswith("uml_rec")]
    
    table_info = list()
    table_events = list()
    
    for rec_file in rec_files:
    
        with open(os.path.join(rec_folder, rec_file)) as f:
            
            fam = rec_file.replace(".ale.uml_rec", "")
            
            lines = f.readlines()
            stree = lines[2].strip()
            ll = lines[6].strip().split()[-1]
            dp,tp,lp = lines[8].strip().split("\t")[1:]
            n_reconciled_trees = int(lines[9].strip().split()[0])
            reconciled_trees = lines[11:n_reconciled_trees + 11]
            de,te,le,se = lines[11 + n_reconciled_trees + 1].split("\t")[1:]
            table = lines[11 + n_reconciled_trees + 3:]             
            
        table_info.append((fam,ll,dp,tp,lp,de,te,le,se))
        table_events.append((fam, table))
    
    if options[0]:
        with open("SpeciesTreeRef.newick", "w") as f:
            f.write(stree.split("\t")[-1])
            
    if options[1]:

        with open("TableInfo.tsv", "w") as f:
            head = "\t".join(["Family", "LL", "Dp", "Tp", "Lp", "De", "Te", "Le", "Se"]) + "\n"
            f.write(head)        
            for info in table_info:
                f.write("\t".join(info))            
    
    if options[2]:   
           
        
        with open("TableEvents.tsv", "w") as f:
            
            header = "Family\tBranchType\t" + table[0].replace("# of", "Branch")
            f.write(header)
            
            for fam, events in table_events:            
                for b in events[1:]:
                    f.write(fam + "\t" + b) 
  
    if options[3]:
        with open("GeneTrees.nwk", "w") as f:
            for t in reconciled_trees:
                f.write(t)
        

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", help="Folder with uml_rec files")    
        
    parser.add_argument("-s", help="Prints species tree to a different file", action='store_true', default = False)
    parser.add_argument("-f", help="Prints info about the family (LogLikelihood, probabilities and total number of events, to a different file", action='store_true', default=False)
    parser.add_argument("-t", help="Prints reconciliation table to a different file", action='store_true', default=False)
    parser.add_argument("-g", help="Prints gene trees to a different file", action='store_true', default=False)
        
    args = parser.parse_args()

    if args.i == None:
        print("use python ale_parser.py -h to see options")
        print("you can run this script just with python ale_parser -i FolderWithRecFiles -sft")
        exit(0)

    ale_parser(args.i, [args.s, args.f, args.t, args.g])


