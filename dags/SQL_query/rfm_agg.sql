DECLARE today_date DATE DEFAULT '1998-05-06';
DECLARE frequencyRange INT64 DEFAULT 180; # tùy chỉnh 

CREATE OR REPLACE TABLE `OLAP.CustomerRFM_Aggregation` AS
WITH CustomerRFM_Aggregation AS (
  SELECT
    orders.CustomerID,
    MAX(CAST(orders.OrderDate AS DATE)) AS Recency,
    -- COUNT(DISTINCT o.OrderID) AS Frequency,
    COUNTIF(DATE_DIFF(today_date, CAST(OrderDate AS DATE), DAY) <= frequencyRange) / frequencyRange AS Frequency,
    SUM(order_details.Quantity * order_details.UnitPrice * (1 - order_details.Discount)) AS Monetary,
    COUNT(DISTINCT orders.OrderID) AS Total_Transaction,
    SUM(order_details.Discount) AS Total_Discount
  FROM
    `OLTP.Orders` orders
  JOIN
    `OLAP.Dim_Order_details` order_details 
  ON 
    orders.OrderID = order_details.OrderID
  GROUP BY
    orders.CustomerID
)

SELECT
  CustomerID,
  DATE_DIFF(today_date, Recency, DAY) AS Recency,
  Frequency,
  Monetary,
  Total_Transaction,
  Total_Discount
FROM
  CustomerRFM_Aggregation;

