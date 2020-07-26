setwd('/Users/smasarone/Documents/Covid analysis/')
library(data.table)
library(edgeR)
library(bioplotr)
library(tidyverse)

#load data
object<-readRDS('/Users/smasarone/Documents/analysis/output_gen_data/counts_data/counts_length_abundance.rds')
counts <- object$counts
clin <-fread('/Users/smasarone/Documents/analysis/Data/samples.csv')%>% as.data.frame()
rownames(clin)<- clin$SampleID
sorted_clin<-clin[order(as.numeric(gsub("[^0-9]", "", row.names(clin)))),] #sort clin dataset as matrix

#filter genes
keep <-rowSums(cpm(counts)>1)  >=20
y <-DGEList(counts[keep,])
y <-calcNormFactors(y)

#Check dimensionality
dim(y)

#plot the mean variance
plot_mv(y)

#transform counts
matrix <-cpm(y, log =  TRUE, prior.count = 1)
saveRDS(mat,"counts_per_million_matrix.rds" )
write.table(mat, file='counts_per_million_matrix.tsv', sep='\t', col.names = TRUE, row.names = TRUE)

#DensityPlot
plot_density(matrix, group= list(Gender = sorted_clin$Type_of_sample))
plot_pca(matrix, sorted_clin$Type_of_sample)
plot_pca(matrix, sorted_clin$Grouping)


png('covid_plot.png',width=900,height=950)
plot_similarity(matrix, group = list(type = sorted_clin$Type_of_sample, 
                                     gender = sorted_clin$Gender,
                                     groups = sorted_clin$Grouping))
dev.off()




