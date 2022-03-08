# v1

## introduction

tast-1-data-preprocessing's first dataset release! we will release further datasets as Dryad give us more datapacks, and intend to provide different versions for different splits and pre-processing techniques. version numbers indicate the input datapack, version letters indicate variations in split / preprocessing

please do provide us with feedback, and we will incorporate this into our future releases

## input datapack

this dataset used the updated verison of 'dryad-datapack-01.09.21-09.09.21.zip' data released on the 24/09/2021

no reference data is included in this dataset - we may include an extra csv just for reference data in future releases (just for data analysis)

## classes

the classes are encoded in encoded_specimen where:

encoded_specimen = 0 = 'clean_air'

encoded_specimen = 1 = 'in_smoke'

# A

## split

This dataset is split by experiment:

train = experiments 6, 7, 8, 9, 14

valid = experiments 10, 12

test = experiments 11, 13, 15

# B

## split

This dataset is split by sensor:

train = sensors 130, 133, 134, 136, 137

valid = sensors 132, 139

test = sensors 140, 143, 146
