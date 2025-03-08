--create this table in your own pg database
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name TEXT,
    category TEXT,
    price NUMERIC(10,2),
    stock_quantity INT
);

CREATE INDEX idx_category_name ON products (category, name);

--add a bunch of products
INSERT INTO products (name, category, price, stock_quantity)
SELECT
    'Product' || generate_series,
    CASE WHEN random() < 0.5 THEN 'Electronics' ELSE 'Clothing' END,
    1,
    1
FROM generate_series(1, 10000);

--try running some of these queries - do they use the index?
EXPLAIN ANALYZE SELECT * FROM products WHERE category = 'Electronics';

EXPLAIN ANALYZE SELECT * FROM products WHERE name = 'Product100';

EXPLAIN ANALYZE SELECT * FROM products WHERE category = 'Electronics' AND name = 'Product100';

--Run the next query before and after creating an index. what changes?
EXPLAIN ANALYZE SELECT * FROM products WHERE price > 100;
CREATE INDEX idx_price ON products(price);
EXPLAIN ANALYZE SELECT * FROM products WHERE price > 100;

--now try a big update
UPDATE products SET category = 'Toys' WHERE category = 'Electronics';

EXPLAIN SELECT * FROM products WHERE category = 'Electronics';


--ok, now update
ANALYZE products;
EXPLAIN SELECT * FROM products WHERE category = 'Electronics';


--dead tuples
SELECT relname, n_live_tup, n_dead_tup 
FROM pg_stat_user_tables 
WHERE relname = 'products';

--Vaccuum,  then try again
VACCUUM products

SELECT relname, n_live_tup, n_dead_tup 
FROM pg_stat_user_tables 
WHERE relname = 'products';



--create a sales table


CREATE TABLE sales (
    id SERIAL PRIMARY KEY,
    sale_date DATE,
    amount NUMERIC(10,2)
);



-- Insert data mostly from past years
INSERT INTO sales (sale_date, amount)
SELECT 
    '2022-01-01'::DATE + (random() * 365)::INT,
    round((random() * 500 + 50)::numeric, 2)
FROM generate_series(1, 10000);

--take a look at the histograms
SELECT attname, histogram_bounds
FROM pg_stats
WHERE tablename = 'sales';


--drop the table and recreate it using partitions

DROP TABLE sales;

CREATE TABLE sales_partitioned (
    id SERIAL,
    sale_date DATE NOT NULL,
    amount NUMERIC(10,2)
) PARTITION BY RANGE (sale_date);

CREATE TABLE sales_2022 PARTITION OF sales_partitioned 
FOR VALUES FROM ('2022-01-01') TO ('2023-01-01');

CREATE TABLE sales_2023 PARTITION OF sales_partitioned 
FOR VALUES FROM ('2023-01-01') TO ('2024-01-01');

-- Insert data into partitions
INSERT INTO sales_partitioned (sale_date, amount)
SELECT 
    '2022-01-01'::DATE + (random() * 365)::INT,
    round(random() * 500 + 50, 2)
FROM generate_series(1, 10000);

--run some queries