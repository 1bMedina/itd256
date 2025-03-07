# Finding Query Plans

## Sequential Scan
### The query
`EXPLAIN select * from employees WHERE First_Name LIKE 'K%';`
### The query plan
```
 Seq Scan on employees  (cost=0.00..15536.00 rows=4114 width=1029)
   Filter: ((first_name)::text ~~ 'K%'::text)
(2 rows)
```
### A short explanation of why it used the operation it did
It likely did this because there is no index that clarifies first names that start with K, so it had to do a row by row scan to find all the data


## Index Scan
### The query
`EXPLAIN select * from employees WHERE employee_id = 1;`
### The query plan
```
 Index Scan using employees_pk on employees  (cost=0.29..8.31 rows=1 width=1029)
   Index Cond: (employee_id = '1'::numeric)
(2 rows)
```
### A short explanation of why it used the operation it did
This uses the index to access the data

## Index Only Scan
### The query

` EXPLAIN select count(*) from employees; `

### The query plan

```
 Limit  (cost=2859.29..2859.30 rows=1 width=8)
   ->  Aggregate  (cost=2859.29..2859.30 rows=1 width=8)
         ->  Index Only Scan using employees_pk on employees  (cost=0.29..2609.29 rows=100000 width=0)
(3 rows)

```
### A short explanation of why it used the operation it did
It only scans the index and not the rest of the table. 