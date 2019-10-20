import pandas as pd
"""
filename = 'InsuranceData.txt'
with open(filename) as infile, open('outfile.csv','w') as outfile:
    for line in infile:
        outfile.write(line.replace(' ',','))
"""
dataset = pd.read_csv('outfile.csv')
dataset['allergy'] = dataset['allergy'].map({'yes': 1, 'no': 0})
print(dataset['allergy'])
