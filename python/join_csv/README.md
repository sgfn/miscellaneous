# join csv

## Description
A program joining two CSV files using a specified column, then writing the
result to stdout.

## Usage
Seeing as the program is written in Python, naturally, a Python interpreter is
required to use it.

### Syntax
As specified: `join.py file_path file_path column_name join_type`
- `file_path` - path to a CSV file
- `column_name` - name of column to join by
- `join_type` - type of join (*inner*/*left*/*right*). When omitted, *inner* by
default

## Default join type
**Inner**. Why? I've assumed that usually, when wishing to join two datasets,
one is interested most in the intersection of them. Additionally, this provides
an output with the least amount of rows by default (a reasonable idea when
working with *big data*, I believe).

## How it works
The joining is performed by creating a hashtable mapping keys: *join_column*
(from *file_being_joined*); to values: list of bytes at which appropriate rows
begin in *file_being_joined*.

At the time of printing, we look up the *join_column* from *file_to_join_to* in
the hashtable and move the file handle of *file_being_joined* to the
corresponding byte stored as value (to each byte from the list, if there are
many). We print the appropriate rows, rinse and repeat until the end of
*file_to_join_to*. If join type is *inner*, we omit the rows with no matches;
otherwise, we print them as well.

### Time complexity
Mapping is O(*rows(file_being_joined)*), the rest is just printing rows from the
other file with appropriate rows mapped to them.

### Memory complexity
O(*rows(file_being_joined)*), which makes it ill-suited for joining files with
very big amounts of rows, as it will sometimes use more memory than the files
themselves. However, it does a good job at quickly joining files with many
columns (lots of data for each row) using a fraction of their size in memory.

## Issues
- Does not check the integrity and validity of provided CSV files (files with
missing columns will probably throw an exception sooner or later)
- Does not utilise multiprocessing in any way, yet using it could possibly save
a bit of time
- Uses way too much memory sometimes (see *How it works:Memory complexity*)

## Testing
CSV files (filled with garbage) for testing purposes can be generated using the
`utils/csv_gen.py` utility, for which I'm too lazy to provide documentation for
(shouldn't be too hard to understand what's going on; `w_dict` is just a dict
with various English words from a selection of books; if you don't change
anything and just run it, it will generate two sizeable, not too small, not too
big, files to work on - join them by *owner_id*). The generated files can then
be tested using known libraries for joining databases, though I haven't had the
time to write any actual tests (everything more or less *just works*).
