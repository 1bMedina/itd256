# Use The Index, Django! - Reflection

- The results of your runtime investigation, formatted into a table
- A short summary of the takeaways of this activity. Specifically, what additional warnings would you give to Django developers who are considering using the __iexact feature in their ORM code?


## A discussion of the two indexes that Django added, and the queries that use them.

Django added two indexes, a standard one and a 'like' one.

The standard one is used as an efficent way to find the exact match in an index. For instance, this query looks at use for a row that says exactly cooking and nothing else. 

```
SELECT "db_stoves"."use" AS "use" FROM "db_stoves" WHERE "db_stoves"."use" = '''Cooking''' LIMIT 21;
```

<img src="Media/DjangoORM-IndexOnlyScan.png" alt="index scan">

The like index is used to find a pattern within the index. For instance, this query is looking for anything that starts with the letter C in the use column

```
SELECT "db_stoves"."id", "db_stoves"."stove_url", "db_stoves"."dimensions", "db_stoves"."experience", "db_stoves"."price", "db_stoves"."climate", "db_stoves"."stove_location", "db_stoves"."use" FROM "db_stoves" WHERE "db_stoves"."use" LIKE 'C%' LIMIT 21;
```

<img src="Media/Like-IndexScan.png" alt="index scan">

## A comparison of the query plans generated when you use/don't use __iexact.

Using i_exact causes the query plan to ignore the index as its making sure that it is finding the *exact* value you requested. This means it results in a seqential scan. Here is a comparision of the 2 query plans generated:

### With i_exact: 

```
 SELECT "db_stoves"."id", "db_stoves"."stove_url", "db_stoves"."dimensions", "db_stoves"."experience", "db_stoves"."price", "db_stoves"."climate", "db_stoves"."stove_location", "db_stoves"."use" FROM "db_stoves" WHERE UPPER("db_stoves"."use"::text) = UPPER('''Cooking''') LIMIT 21;
```

```
>>> s = Stoves.objects.filter(use__iexact="'Cooking'")
>>> print(s)
```

<img src="Media/iExact_SeqScan.png" alt="seq scan">

### Without i_exact:

```
SELECT "db_stoves"."id", "db_stoves"."stove_url", "db_stoves"."dimensions", "db_stoves"."experience", "db_stoves"."price", "db_stoves"."climate", "db_stoves"."stove_location", "db_stoves"."use" FROM "db_stoves" WHERE "db_stoves"."use" = '''Cooking''' LIMIT 21;
```

```
>>> s = Stoves.objects.filter(use="'Cooking'")
>>> print(s)
```

<img src="Media/noiexact_IndexScan.png" alt="index scan">

## Time difference:

for 1000 
```
With 1280 records in the table:
	- average time for query that uses index: 0.006 seconds
	- average time for query that does not use index: 0.011 seconds
```
for 10000
```
With 12280 records in the table:
	- average time for query that uses index: 0.006 seconds
	- average time for query that does not use index: 0.054 seconds
```
for 100000
```
With 112280 records in the table:
	- average time for query that uses index: 0.006 seconds
	- average time for query that does not use index: 0.502 seconds
```
for 1000000
```
With 1112280 records in the table:
	- average time for query that uses index: 0.009 seconds
	- average time for query that does not use index: 4.54 seconds
```

### Time difference in a table:

