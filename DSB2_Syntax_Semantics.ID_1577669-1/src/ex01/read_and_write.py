import csv

with open('ds.csv', 'r') as csv_file:
    reader = csv.reader(csv_file) 
    with open('ds.tsv', 'w') as tsv_file:
        writer = csv.writer(tsv_file, delimiter = '\t') # разделитель
        for row in reader:
            writer.writerow(row)
            
def main():
    convert_csv_to_tsv() # type: ignore

if __name__ == '__main__':
    main()