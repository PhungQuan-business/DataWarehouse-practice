-- Step 1: Create the Product_Aggregation table
CREATE OR REPLACE TABLE `OLAP.Product_Aggregation` AS
  SELECT
    order_details.ProductID,
    0 as High_productive_product,
    0.0 As Total_sale_by_product
  FROM
    `OLAP.Dim_Order_details` order_details 
  GROUP BY
    order_details.ProductID
;


UPDATE `OLAP.Product_Aggregation` AS dim
SET Total_sale_by_product = (
    SELECT SUM(UnitPrice*Quantity*(1-Discount))
    FROM `OLAP.Dim_Order_details` AS fact
    WHERE dim.ProductID = fact.ProductID
    Group by ProductID
)
WHERE dim.ProductID IS NOT NULL;

-- Step 2: Create the temporary table to store the results
CREATE OR REPLACE TABLE `OLAP.Temp_RankedProducts` AS
WITH RankedProducts AS (
    SELECT 
        ProductID,
        Total_sale_by_product AS Total_sale_by_product,
        PERCENT_RANK() OVER (ORDER BY Total_sale_by_product DESC) AS PercentRank
    FROM `OLAP.Product_Aggregation`
)
SELECT 
    ProductID,
    Total_sale_by_product,
    CASE 
        WHEN PercentRank <= 0.8 THEN 1  
        ELSE 0  
    END AS ContributesTo80Percent
FROM RankedProducts;

-- Step 3: Update the Product_Aggregation table using MERGE
MERGE `OLAP.Product_Aggregation` AS target
USING `OLAP.Temp_RankedProducts` AS source
ON target.ProductID = source.ProductID
WHEN MATCHED THEN
  UPDATE SET target.High_productive_product = source.ContributesTo80Percent;

-- Step 4: Drop the temporary table
DROP TABLE `OLAP.Temp_RankedProducts`;


