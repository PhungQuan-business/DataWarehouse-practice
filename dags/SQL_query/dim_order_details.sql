-- Tạo bảng Dim_Order_details
CREATE OR REPLACE TABLE 
  `OLAP.Dim_Order_details` AS
SELECT
  *
FROM
  `OLTP.Order_details`


