# Chapter 1 - Anatomy of an Index & The Preface

## Notes (preface & some of chapter 1):
- An SQL statement is a straight description of what is needed, but not instructions on how to get it done
- An index is a distinct structure in the database created by using the `CREATE INDEX` statement
- It requires its own disk space which holds a copy of the index, an index is redundant, and it goes through constant change
- The database combines to data structures to meet the challenge of keeping up with `insert` `delete` and `update` statements with doubly linked lists and a search tree. 

## Index Leaf Nodes: 
- Moving large amounts of data is very time-consuming making `insert` statements very slow when it comes to indexes. The solution is to establish a logical order that is independent of physical order in memory.
    - The logical order is established using double linked lists
    - Every node has links to two neighboring entries, like a chain
    - New nodes are inserted between two existing nodes by updating their links to refer to the new node
    - The physical location of the new node doesn't matter because the double linked list maintains the logical order
- It's called a double linked list because each node refers to the preceding and the following node
- Double linked lists are also used for collections aka containers in many programming languages like Java and C++
- Databases use double linked lists to connect the so-called index leaf nodes, each leaf node is stored in a database block or page.
    - Database blocks or pages are the databases smallest storage units

## B-Tree:
- A database needs a second structure to find the entry among the shuffled pages quickly, this is a balanced search tree aka B-tree.
- The double linked list establishes logical order between the leaf nodes, then the root and branch nodes support quick searching among the leaf nodes
- Each branch node entry corresponds to the biggest value in the respective leaf node
- The procedure repeats until all keys fit into a single node, the root node. 
- The structure is a balanced tree search because the tree depth is equal at every position 
- Once created the database maintains the index automatically

## Slow Indexes, Part I
- Even with the efficiency of tree traversal, there are still cases where an index look up is slower than expected
- The first ingredient of a slow index lookup is the leaf node chain
    - This happens when the database must read the next leaf node to see if there are anymore matching entries
    - This means that an index lookup not only needs to preform the tree traversal but also needs to follow the leaf node chain
- The second ingredient for a slow index look up is accessing the table
    - Even a single leaf node might contain many hits, often hundreds
    - The corresponding table data is often scattered across many table blocks, which means that there is an additional table access for each hit
- The last two steps of an index lookup are what it slows it down; following the leaf node chain, and fetching the table data
- The slow index myth was created through the misbelief that indexes only had to traverse the tree, hence the idea that a slow index must be caused by a broke and or unbalanced tree. 
- Index unique scan preforms the tree traversal only
- Index range scan preforms the tree traversal and follows the leaf node chain to find all matching entries. 
- Table access by index rowid operation retrieves the row from the table.
- Index range scan can potentially read a large part of an index

