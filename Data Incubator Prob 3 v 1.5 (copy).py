# -*- coding: utf-8 -*-
"""
Created on Sun Apr 29 17:58:56 2018

@author: amedinam
"""

import csv

'''cleaning the extracted files related to national 
parks for the years 2016,2015,2014,2012'''

'''2016'''
with open('Nat_Parks_2016.csv','r') as csv_file:
    reader = csv.reader(csv_file)
    
    with open('cleaned_Nat_Parks_2016','w') as new_file:
        writer = csv.writer(new_file)        
        
        next(reader)
        for line in reader:
            del(line[0],line[0])
            line[0] = 2016
            for entry in line:
                if ',' in str(entry):
                    new_entry = entry.replace(",", "")
                    line[line.index(entry)] = new_entry 
            writer.writerow(line)

'''2015'''            
with open('Nat_Parks_2015.csv','r') as csv_file:
    reader = csv.reader(csv_file)    
        
    with open('cleaned_Nat_Parks_2015','w') as new_file:
        writer = csv.writer(new_file)        
        
        next(reader)
        for line in reader:
            del(line[0],line[0],line[5],line[5])
            line[0] = 2015
            for entry in line:
                if ',' in str(entry):
                    new_entry = entry.replace(",", "")
                    line[line.index(entry)] = new_entry             
            writer.writerow(line)

'''2014'''            
with open('Nat_Parks_2014.csv','r') as csv_file:
    reader = csv.reader(csv_file)
    
    with open('cleaned_Nat_Parks_2014','w') as new_file:
        writer = csv.writer(new_file)        
        
        next(reader)
        for line in reader:
            del(line[5],line[5])
            line[0] = 2014
            for entry in line:
                if ',' in str(entry):
                    new_entry = entry.replace(",", "")
                    line[line.index(entry)] = new_entry 
            writer.writerow(line)
          
'''2012'''
with open('Nat_Parks_2012.csv','r') as csv_file:
    reader = csv.reader(csv_file)    
    
    with open('cleaned_Nat_Parks_2012','w') as new_file:
        writer = csv.writer(new_file)        
        
        next(reader)        
        for line in reader:
            if line != ['', '', '', '']:
                    line.insert(0, 2012)
                    for entry in line:
                        if ',' in str(entry):
                            new_entry = entry.replace(",", "")
                            line[line.index(entry)] = new_entry 
                    writer.writerow(line)


cleaned_files = ['cleaned_Nat_Parks_2012','cleaned_Nat_Parks_2014','cleaned_Nat_Parks_2015','cleaned_Nat_Parks_2016']


'''___preparing data for analysis___'''


import numpy as np
               
to_from_matrices = []

for file in cleaned_files:
    with open(file,'r') as csv_file:
        reader = csv.reader(csv_file)
        
        first_line = next(reader)
        year = int(first_line[0])
        
        to_from_matrix = np.zeros((3,3),dtype=int) 
        
        #                 \_national_\_foreign_\_total_\     
        # out of patagonia\__________\_________\_______\
        # in patagonia    \__________\_________\_______\
        # anywhere        \__________\_________\_______\
        
        to_from_matrix[2,0] += int(first_line[3])
        to_from_matrix[2,1] += int(first_line[4])        
        
        for line in reader:
            if 'LOS LAGOS' in line[1] or 'XIV' in line[1] or 'AISÉN' in line[1] or 'MAGALLANES Y ANTÁRTICA' in line[1]:
                to_from_matrix[1,0] += int(line[3])
                to_from_matrix[1,1] += int(line[4])
        
        for i in range(len(to_from_matrix[0:])):
            to_from_matrix[0,i] = (to_from_matrix[2,i]-to_from_matrix[1,i])
        for i in range(len(to_from_matrix[0:])):
            to_from_matrix[i,2] = (to_from_matrix[i,0]+to_from_matrix[i,1])
        
        to_from_matrices.append(to_from_matrix)            


'''___analysis___'''

print('Proportion of foreign visitors to national parks anywhere in Chile, per year')
string = ''
for i in range(len(cleaned_files)):
    string += '   '+str(to_from_matrices[i][2,1]/to_from_matrices[i][2,2])
print(string)

print('Proportion of foreign visitors to national parks in Patagonia, per year')
string = ''
for i in range(len(cleaned_files)):
    string += '   '+str(to_from_matrices[i][1,1]/to_from_matrices[i][1,2])
print(string)

print('Proportion of foreign visitors to national parks not in Patagonia, per year')
string = ''
for i in range(len(cleaned_files)):
    string += '   '+str(to_from_matrices[i][0,1]/to_from_matrices[i][0,2])
print(string)

print('number of visitors to national parks, per year')
any_total = []
for i in range(len(cleaned_files)):
    any_total.append(to_from_matrices[i][2,2])
print(any_total)

print('number of foreign visitors to national parks, per year')
any_foreign = []
for i in range(len(cleaned_files)):
    any_foreign.append(to_from_matrices[i][2,1])
print(any_foreign)

print('number of visitors to national parks in Patagonia, per year')
pata_total = []
for i in range(len(cleaned_files)):
    pata_total.append(to_from_matrices[i][1,2])
print(pata_total)

print('number of foreign visitors to national parks in Patagonia, per year')
pata_foreign = []
for i in range(len(cleaned_files)):
    pata_foreign.append(to_from_matrices[i][1,1])
print(pata_foreign)


'''__regression__'''

from scipy import *

years = [2,4,5,6]
p1 = polyfit(years,any_total,1)
p2 = polyfit(years,any_foreign,1)
p3 = polyfit(years,pata_total,1)
p4 = polyfit(years,pata_foreign,1)
print(p1[0],p2[0],p3[0],p4[0])


'''__growth factors__'''

growth_factors = [any_total[3]/any_total[0],any_foreign[3]/any_foreign[0],pata_total[3]/pata_total[0],pata_foreign[3]/pata_foreign[0]]
print(percent_growth)