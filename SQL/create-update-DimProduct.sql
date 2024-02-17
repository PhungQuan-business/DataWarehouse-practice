CREATE OR REPLACE TABLE
  `northwind-qu.Transformed_Dataset.Dim_Products` AS
SELECT
  t1.ProductName,
  t1.QuantityPerUnit,
  t1.UnitPrice,
  t1.UnitsInStock,
  t1.UnitsOnOrder,
  t1.ReorderLevel,
  t1.Discontinued,
  t2.CategoryName,
  t2.Description
FROM
  `northwind-qu.OLTP.Products` t1
LEFT JOIN
  `northwind-qu.OLTP.Categories` t2
ON
  t1.CategoryID = t2.CategoryID