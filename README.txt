Group 49

Members:
Evan Steer
Yunato Sun
Julianna Stainer (dropped out)
Luke Clark

How to use our code:

All code can be run from the terminal using '$ python cw3.py'

If you want to use flags:

- for --explain, use '$ python cw3.py --explain'
- for --hint N, use '$ python cw3.py --hint x' but replace x with an integer
- for --file, use '$ python cw3.py -f INPUT.txt'
- for --profile, use '$ python cw3.py --profile'

Our program has a set of 9 grids hardcoded into the program which can be found
at the top of the file, they reprsent a range of grids of a range of difficulty and size

You can replace these grids with anything else by editting the grids.
It is important you make sure that if you replace the grid you also update the grids[]
list to have the appropiate rows/columns per square.

It is possible when trying to run --profile you will encounter an error saying matplotlib was not found.
If this happens do 'python.exe -m pip install matplotlib' and that will fix your problem.

In the folder you will find INPUT.txt which contains a (very hard) 3x3 example grid for --file.
The results of --file are in OUTPUT, which is overwritten each time the program is run.

The wavefront algorithm is only designed to work alone or with --profile, in which case it will output
the times for each run on both normal and wavefront and then the mean time for each solver

In the case of using wavefront normally it uses a self generated set of grids, 
if using it with --profile it will use the same grids as shown at the top of the program
