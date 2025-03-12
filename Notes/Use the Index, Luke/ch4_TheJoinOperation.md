# Chapter 4 - The Join Operation

## Notes:
### Intro to joins:
- Joins only process two tables at a time
- The join order has no impact on the final result, but it still affects the performance. 
- Optimizing a complex statement might become a performance problem. 

### Nested loops:
- Nested loop join is the most fundamental join algorithm. 
    - The outer or driving query to fetch the results from one table and a second query for each row from the driving query to fetch the corresponding data from the other table. 
- You can use 'nested selects' to implement the nested loops algorithm.
- There is the " $N+1$ selects problem" which means that it executes $N+1$ selects in total if the driving query returns $N$ rows.
- Indexing for nested loops join is therefore like indexing for select statements (given in chapter).
- There are two dimensions of performance: response time and throughput
    - In computer networks these can be called *latency* and *bandwidth*.
    - Bandwidth only has a minor impact on response time but latency has a huge impact on response time. 
- The number of database round trips is more important for the response time that the amount of data transferred. 
- ORM tools offer many ways to create SQL joins, one of the most important being *eager-fetching*.
    - Eager fetching is counterproductive if you do not need the child records when accessing the parent records.
- Nested loops join delivers good performance if the driving query returns a small result set.
