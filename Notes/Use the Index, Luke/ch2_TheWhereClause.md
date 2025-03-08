# Chapter 2 - The Where Clause

## The Equality Operator
- `where` clauses that combine multiple conditions are vulnerable to indexing mistakes that would affect performance

### Primary Keys
 - The where clause (in some aspects) cannot match multiple rows because the primary key ensures uniqueness of the, in this case, employee_id.
    - This means that the database does not need to follow the index leaf nodes, traversing the index tree will be enough
In postgresql, operation Index Scan combines the index \[unique/range] scan and table access by index rowid operations
- There is now slow index risk with an Index Unique Scan because the operation cannot deliver more than one entry, so it cannot trigger more than one table access
    - Meaning ingredients of a slow query are not present with an Index Unique Scan

### Concatenated Keys
- A concatenated index is when the database creates an index on all primary key columns
    - Is also known as a multi-column, composite or combined index
    - The column order of a concatenated index has a great impact on its usability, so it must be chosen carefully
- When adding a subsidiary ID, theres a risk when running the `where` clause that the database will preform a table access full rather than accessing by index
    - This means the database reads the entire table, which causes execution time to grow which could be a danger in a large scale production
- A concatenated index is just a B-tree index
- Bitmap Index Scan followed by a Bitmap Heap Scan roughly correspond to Oracles Index Range Scan and Table Access By Index RowID with one important difference: it fetches all results from the index (Bitmap Index Scan), then sorts the rows according to the physical storage location of the rows in the heap table then fetchers all rows from the table (Bitmap Heap Scan)
- A database can use a concatenated index when searching with the leading (leftmost) columns. 

### Slow Indexes, Part II
- Sometimes Table Access Full can be more efficient than an index scan...?
- The operation that will be most efficient depends on the size of the table, sometimes a full table scan would be more efficient because it can read larger parts from the table in one shot
- Providing the correct statistics helps the optimizer determine which operation to do accurately
