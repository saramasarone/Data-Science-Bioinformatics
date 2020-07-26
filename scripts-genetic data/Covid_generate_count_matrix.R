library(tximport)
library(rhdf5)
library(data.table)
library(bioplotr)
library(tidyverse)
library(ensembldb)
library(AnnotationHub)

ah <- AnnotationHub() 
ahDb94 <- query(ah, pattern = c("Homo Sapiens", "EnsDb", 94)) 
ahEdb <- ahDb94[[1]] 
gene <- transcripts(ahEdb,columns = c(listColumns(ahEdb , "gene"), "gene_name"), return.type = "data.frame")
tx <- transcripts(ahEdb, return.type = "data.frame")
ens_94 <-data.frame(tx$tx_id) #only selected two columns (not sure if it is correct)
ens_94$genes <-tx$gene_id 
ens_94$gene_name <- gene$gene_name
filtered <-ens_94[grep("ENST", ens_94$tx.tx_id),] #only get the ones starting with ENS

############# tximport covid ###########
clin <-fread("/Users/smasarone/Documents/kallisto/output_covid/sorted_folders_covid.txt")
dir <-file.path("/Users/smasarone/Documents/kallisto/output_covid")
samples <- read.table(file.path(dir, "sorted_folders_covid.txt"), header = TRUE)
files <-file.path(dir, "output", samples$run, "abundance.tsv")
names(files) <-clin$run 
txi <-tximport(files, type = 'kallisto', tx2gene = filtered, countsFromAbundance = 'lengthScaledTPM',ignoreTxVersion = TRUE)


counts <-txi$counts
saveRDS(counts,'covid_counts.rds')
saveRDS(txi,'covid_counts_length_abundance.rds')
write.table(counts, file='covid_counts.tsv', sep='\t', col.names = TRUE, row.names = TRUE)
