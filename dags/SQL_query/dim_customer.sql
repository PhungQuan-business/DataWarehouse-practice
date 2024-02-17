-- Tạo bảng Dim_Customer 
CREATE OR REPLACE TABLE 
  `OLAP.Dim_Customers` AS
SELECT
  customers.CustomerID,
  customers.City,
  customers.Phone,
  customers.Country
FROM
  `OLTP.Customers` AS customers


