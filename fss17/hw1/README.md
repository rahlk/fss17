# FSS17
## HW1

### Description: 

Read each line, kill whitepsace and anything after comment characters (`#`), break each line on comma, read rows into a list of lists (one list per row), converting strings to numbers where appropriate. Note that some column headers contain `?`: all such columns should be ignored. 

Your code should contain checks for bad lines (and bad lines should be skipped over); i.e. symbols where numbers should be and wrong number of cells (we will say that row1 has the “right” length).

### Files: 

_ `read_csv.py`: python file to execute the work for this assignment 

_ `POM3A.csv`: given original csv table file 

_ `POM3A_bad.csv`: testing csv table file with added bad lines 
    + See line 1 for wrong type (column 2 is a string not a float)
    + And line 2 has fewer rows than required

### How to run:

- Install python 2.7
- Execute the command line as below in the terminal within the `hw1` folder:
```
python read_csv.py
```
Note: There are two test cases in `read_csv.py`:
    
    + `test_time_to_read_csv()` reads the correct file and prints time taken ~0.11 seconds
    
    + `test_read_bad_csv()` reads a bad csv file, prints exceptions for bad lines.

### Output:
Sample output
```
Test Case 1
Time to read file=0.11 seconds

Test Case 2
ValidationError in line #2: Row element type doesn't match column header. Skipping row.
ValidationError in line #3: Incorrect row size. Skipping row.
```
