CREATE OR REPLACE TABLE `OLAP.Fact_Table` AS
WITH CustomerRFM AS (
  SELECT
    temp.CustomerID,
    temp.ProductID,
    temp.OrderID,
    temp.OrderDate,
    rmf.Recency,
    rmf.Frequency,
    rmf.Monetary,
    rmf.Total_Transaction,
    rmf.Total_Discount,
    pd.High_productive_product,
    pd.Total_sale_by_product
  FROM
    `OLAP.Fact_Table_temp` as temp
  JOIN
    `OLAP.CustomerRFM_Aggregation` as rmf
  ON
    temp.CustomerID = rmf.CustomerID
  JOIN
    `OLAP.Product_Aggregation` as pd
  ON 
    temp.ProductID = pd.ProductID
)
SELECT * FROM CustomerRFM;



