# -*- coding: utf-8 -*-
"""
Created on Sun Apr 29 17:58:56 2018

@author: amedinam
"""

import csv

'''cleaning the extracted files related to national 
parks for the years 2016,2015,2014,2012'''

'''2016'''
with open('Nat_Parks_2016.csv','r',encoding="utf8") as csv_file:
    reader = csv.reader(csv_file)
    
    with open('cleaned_Nat_Parks_2016','w',newline="") as new_file:
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
with open('Nat_Parks_2015.csv','r',encoding="utf8") as csv_file:
    reader = csv.reader(csv_file)    
        
    with open('cleaned_Nat_Parks_2015','w',newline="") as new_file:
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
with open('Nat_Parks_2014.csv','r',encoding="utf8") as csv_file:
    reader = csv.reader(csv_file)
    
    with open('cleaned_Nat_Parks_2014','w',newline="") as new_file:
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
with open('Nat_Parks_2012.csv','r',encoding="utf8") as csv_file:
    reader = csv.reader(csv_file)    
    
    with open('cleaned_Nat_Parks_2012','w',newline="") as new_file:
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


print('For years\n[2012,2014,2015,2016]')

print('\nNumber of visitors to national parks')
any_total = []
for i in range(len(cleaned_files)):
    any_total.append(to_from_matrices[i][2,2])
print(any_total)

print('\nNumber of foreign visitors to national parks')
any_foreign = []
for i in range(len(cleaned_files)):
    any_foreign.append(to_from_matrices[i][2,1])
print(any_foreign)

print('\nNumber of visitors to national parks in Patagonia')
pata_total = []
for i in range(len(cleaned_files)):
    pata_total.append(to_from_matrices[i][1,2])
print(pata_total)

print('\nNumber of foreign visitors to national parks in Patagonia')
pata_foreign = []
for i in range(len(cleaned_files)):
    pata_foreign.append(to_from_matrices[i][1,1])
print(pata_foreign)

print('\nProportion of foreign visitors to national parks anywhere in Chile')
foreign__over_any_anywhere = []
for i in range(len(cleaned_files)):
    foreign__over_any_anywhere.append(to_from_matrices[i][2,1]/to_from_matrices[i][2,2])
print(foreign__over_any_anywhere)

print('\nProportion of foreign visitors to national parks in Patagonia')
foreign__over_any_pata = []
for i in range(len(cleaned_files)):
    foreign__over_any_pata.append(to_from_matrices[i][1,1]/to_from_matrices[i][1,2])
print(foreign__over_any_pata)

print('\nProportion of foreign visitors to national parks not in Patagonia')
foreign__over_any_not_pata = []
for i in range(len(cleaned_files)):
    foreign__over_any_not_pata.append(to_from_matrices[i][0,1]/to_from_matrices[i][0,2])
print(foreign__over_any_not_pata)


'''__linear_regression__'''


from scipy import *
from numpy.polynomial.polynomial import polyval

years = [2012,2014,2015,2016]
p0 = polyfit(years,any_total,1)
#p1 = polyfit(years,any_foreign,1)
#p2 = polyfit(years,pata_total,1)
#p3 = polyfit(years,pata_foreign,1)


'''__growth factors__'''


growth_factors = [any_total[3]/any_total[0],any_foreign[3]/any_foreign[0],pata_total[3]/pata_total[0],pata_foreign[3]/pata_foreign[0]]
print('\nThe total number of visitors to patagonia grew by a factor of\n',growth_factors[2])


'''__plotting__'''

import matplotlib.pyplot as plt

'''visitors to national parks in Chile vs. year with superimposed linear regression'''
 
x = years + [2017,2018,2019]
y = polyval(x,[p0[1],p0[0]])
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(x, y, color='lightblue', linewidth=3)
ax.scatter(years, any_total, color = 'darkblue', marker='^')
ax.set_xlim(2011.8, 2019.2)
ax.set_ylim(0, 4000000)
ax.set(title='Visitors to National Parks in Chile',ylabel='Number of visitors',xlabel='Years')
plt.savefig('linreg_total_any.png') 
plt.show()
plt.clf()

    
'''contrasting proportion of foreign visitors to national parks in patagonia'''


fig = plt.figure()
ax = fig.add_subplot(111)
x1 = [ x-.2 for x in years]
in_pata = ax.bar(x1,foreign__over_any_pata, width=.3, color='green')
x2 = [ x+.2 for x in years]
out_pata = ax.bar(x2,foreign__over_any_not_pata, width=.3, color='lightgreen')

ax.set_ylim(0, 1)
ax.legend((in_pata,out_pata), ('Inside Patagonia','Outside Patagonia'))
ax.set(title='Proportion of Foreign Visitors to Chilean National Parks',ylabel=' ',xlabel='Years')

plt.savefig('proportion_foreign_pata.png') 
plt.show()
plt.clf()

