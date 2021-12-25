# Logic-Resolution

Logic Resolution program with input file name "input.txt" and output file name "output.txt".</br>
Download those test cases and rename to "input.txt" and run py file to test.</br>
Logic statements in input files contain OR only.</br>
First row is alpha.</br>
Second row is the number of statements in KB.</br>
The following lines are the statements in KB.</br>
*Example input:*</br>
```
-A OR F
4
-A OR B OR C
-B OR D OR F
-A OR -D OR F
-C OR F
```
*Another example input:*</br>
```
-A
4
-A OR B
B OR -C
A OR -B OR C
-B
```
*The output for the latter input:*
```
3
-A
B
-C
4
-B OR C
A OR C
A OR -B
{}
YES
```
