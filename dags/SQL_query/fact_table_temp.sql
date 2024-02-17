DECLARE today_date DATE DEFAULT '1998-05-06';
DECLARE frequencyRange INT64 DEFAULT 180; # chỉnh tùy ý muốn
CREATE OR REPLACE TABLE 
  `OLAP.Fact_Table_temp` AS
SELECT
  orders.OrderID,
  orders.CustomerID,
  orders.OrderDate,
  order_details.ProductID,
FROM
  `OLTP.Orders` AS orders
JOIN 
  `OLAP.Dim_Order_details` AS order_details
ON
  orders.OrderID = order_details.OrderID
JOIN
  `OLAP.Dim_Products` AS products
ON
  order_details.ProductID = products.ProductID;
