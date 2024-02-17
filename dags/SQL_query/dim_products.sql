-- Tạo bảng Dim_Products
CREATE OR REPLACE TABLE 
  `OLAP.Dim_Products` AS
SELECT
  products.ProductID,
  products.ProductName,
  products.UnitPrice,
  categories.CategoryID,
  categories.CategoryName,
FROM
  `OLTP.Products` AS products
JOIN
  `OLTP.Categories` AS categories
ON
  products.CategoryID = categories.CategoryID;


