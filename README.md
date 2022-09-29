
# A short tutorial on Phylogenetic Reconciliations using ALE

Evolution is often well represented by bifurcating trees. Different processes can create "trees within trees" structures. How those two tree structures map to each other can be inferred using phylogenetic reconciliations 

This is a simple tutorial on how to use ALE, a software that reconciles gene trees and species tree. In this tutorial, we are going to learn how to reconcile a gene tree and a species tree, and how to interpret the output of ALE.

You need two things to run a reconciliation: a gene tree and a species tree. The species tree **can** be a dated tree, but this is not a requirement (see the section differences between ALE dated and ALE undated). The gene tree **can** be a distribution of gene trees, as the ones inferred by using the ultrafast bootsrap of IQ-TREE (toggle the -w option to write the individual trees). Using a gene tree distribution instead of a single tree is encouraged, because it informs ALE about the uncertainty in the topology of the tree and allows it to make better predictions.

In this example, we are going to use some simulated data I generated using **Zombi**. I generated a small species tree with 10 leaves and I simulated 100 gene families that were present in the root. The families evolved following events of Duplications, Transfers and Losses.  Zombi outputs the final gene trees, which is what we will use in this tutorial (there is no need to use a distribution of trees in this case because given that we are using simulated dated, we are certain about the topology of the tree). 

The first thing to do is, for every gene family, (files in the Trees folder), obtain the .ale file. The .ale file contains the CCPs (conditional clade probabilities), which are used later by ALE to estimate the likelihood of the different reconciliations. The files are  very easy to obtain, the command is:

```
ALEobserve 1_prunedree.nwk
```

This will generate the file:


10_prunedtree.nwk.ale


The .ale files can be found in the folder ALEs.


Once we have this, we run the reconciliation by using the command:

```
ALEml_undated  SpeciesTree.nwk 10_prunedtree.nwk.ale
```

This will produce two files: the uml_rec file and the uTs file. All the files have already been computed antd the reader can inspect them in the different folders of this repository

### Parsing ALE results

The script ale_splitter.py can be used to obtain that information in different files, which simplifies the process of parsing them with Python or R later:

```{ssh}
python ale_splitter.py -i S_S_COG3397.ufboot.ale.uml_rec -sftr

```
If the user is dealing with a large number of reconciliations, there is a different and better way to extract that information. This script creates two big tables with all the relevant information per family

```
python ale_parser.py -i FolderWithReconciliations -sft

```

### Interpreting ALE results

ALE infers by default 100 reconciliations. The user can change that number easily.
It creates two files

* Files uTs: They contain information about the Lateral Gene Transfers. The columns indicate the donor branch, the recipient branch and the weight of the transfer, i.e. the number of times that the transfer has been found divided by the number of reconciliations

* Files uml_rec. 

1. The Species Tree. ALE renames the inner branches and uses these names to specify the different events. To view this branch nodes it is possible to use SeaView and toggle the option Br support
2. The LogLikelihood of the reconciliation 
3. The "rate" of Duplication, Transfer and Losses. Rates is the wrong name and has 
4. The reconciled gene trees. The gene trees have annotation in the inner branches that specify the exact reconciliation event.Since ALE is a probabilistic algorithm, those events might differ from tree to tree
5. The number of D, T, L and Speciation events found, divided by the number of reconciliations
6. A big table, divided by the number of reconciliations

### How to interpret fractional values?

What does it mean that a gene family has 0.5 transfers? The values represented in the table correspond to counting the total number of events in the 100 reconciled trees and dividing this number by 100. This means that if half of the reconciliations have a single transfer events (and not the other half), we will see that a family has 0.5 transfer. The correct way to interpret this number is as a probability of a transfer taking place in this family.

### What is the meaning of the different columns

Branch -  Code of the branch according to the Species Tree

BranchType - Whether the branch is a terminal branch or an inner branch

Duplications - Average number of Duplications events in the branch

Transfers- Average number of Transfer events in the branch

Losses - Average number of Loss events in the branch

Originations - Fraction of times that the Gene Family starts in this specific branch

Copies - Average number of copies in the branch

Singletons - Average number of genes that are seeing as vertically evolving, i.e. the gene can be found at the beginning of the branch and at the end

Extinctinonprob - FINISH

Presence - FINISH

LL - FINISH


### Obtaining verticality

In Coleman et al. 2021 (A rooted phylogeny of bacteria resolves early evolution), we proposed two metrics to evaluate the amount of transfers vs the amount of vertical evolution. The first one is verticality, a branch wise metric which is defined as the total number of singletons inferred in a branch divided by the singletons, originations and transfers.

This measure can be obtained with (for example) pandas. The user can find a notebook in this repository (called AnalyzingResults.ipyb) that shows how to do it.


 ```
df = pd.read_csv("TableEvents.tsv", sep = "\t")

dfb = df.groupby("Branch", as_index=False).sum()

dfb["Verticality"] = dfb["singletons"] / (dfb["singletons"] + dfb["Originations"] + dfb["Transfers"])

```

The second metric is called transfer propensity, and it is a family metric. It measures, as the name indicates, how prone to be a transferred a family is.


```

df = pd.read_csv("TableEvents.tsv", sep = "\t")

dff = df.groupby("Family").sum()

dff["TransferPropensity"] = dff["Transfers"] / (dff["singletons"] + dff["Transfers"])

```


### What are some things I need to consider when dealing with real data?

There are at least two very important things to remember:

1. Use a file fraction_missing. The reconcilation can consider that a gene might be missing from a genome not because the gene was lost, but because we don't know the complete sequence of the genome. When working with bacterial genomes for instance (Coleman 2021),  we use the genome completness estimates from CheckM.
2. Do use gene tree distributions and not single trees! See next point


###  How do you deal with the uncertainties in the Gene Trees?

The main innovation of ALE is that it does not reconcile a single gene tree to the species tree. Instead, it uses a distribution of gene trees, such as the one obtained by Bootstrap or the posterior chain of a Bayesian method. In most phylogenetic studies those trees are summarized as a single tree with some associated values for the internal nodes representing the degree of confidence in that node. What ALE does is taking the distribution of trees and reconcile the different splits that are found in the trees, weighting them by their frequency. By doing this, ALE manages to account for the uncertainty in the gene trees.


### What are some of the applications of phylogenetic reconciliations?

There are many useful things such as:

1. Rooting Species Trees (Coleman et al 2021)
2. Rooting Gene Trees 
3. Inferring the most likely origin for a given gene family
4. Inferring ancestral genomes
5. Understand the evolution of a gene family  
6. Measure trends of genome evolution (e.g. genome size increase)
7. Infer ancient Lateral Gene Transfer events
8. Improve the quality of Gene Trees
9. Obtain dated trees

Etc


### What is the difference between ALE dated and ALE undated?

ALE dated is the original model: in this model the transfers are inferred to occur between contemporary lineages. This is guaranteed by using as input a dated tree, i.e. a tree in which the branch lengths are proportional to time. These have different problems (see Davin et al 2022 for a more detailed discussion), but the main one is that obtaining dated trees is difficult. ALE dated is also slow. For that reason, ALE undated (Szollosi 2014)  was developed. Some of the transfers obtained can be time inconsistent

### How do you deal with the uncertainties in the Species Tree?
In its current version, ALE does not account for that uncertainty and Species Tree is taken at face value, so it is important to used well resolved trees. 
