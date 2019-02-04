SELECT sal.Emp_Num,emp.EMP_FNAME,emp.EMP_LNAME, sal.SAL_AMOUNT,emp.DEPT_NUM FROM salary_history sal inner 
JOIN employee emp ON sal.Emp_Num=emp.Emp_Num 
WHERE sal.SAL_END = '1999-09-12' AND emp.DEPT_NUM=300 ORDER BY SAL_AMOUNT desc;

#2
SELECT min_sal.Employee_Emp_Num, emp.EMP_FNAME, emp.EMP_LNAME, min_sal.SAL_FROM, min_sal.SAL_AMOUNT FROM 
(SELECT Employee_Emp_Num,Sal_Amount, MIN(Sal_FROM) AS SAL_FROM FROM salary_history GROUP BY Employee_Emp_Num) AS min_sal INNER JOINemployee emp 
ON min_sal.Employee_Emp_Num=emp.Emp_Num ORDER BY min_sal.Employee_Emp_Num;

#3
SELECT line.Invoice_Inv_Num, line.LINE_NUM, line.Product_Prod_Sku, p1.PROD_DESCRIPT,p1.Brand_Brand_Id
FROM line line INNER JOIN(SELECT DISTINCT p.PROD_SKU,p.PROD_DESCRIPT,p.Brand_Brand_Id FROM product p WHERE p.PROD_CATEGORY = 'Top Coat') p1 
ON line.Product_Prod_Sku=p1.PROD_SKU INNER JOIN(SELECT DISTINCT p.PROD_SKU,p.PROD_DESCRIPT,p.Brand_Brand_Id FROM product p WHERE p.PROD_CATEGORY = 'Sealer') p2 
ON line.Product_Prod_Sku=p2.PROD_SKU WHERE p1.Brand_Brand_Id=p2.Brand_Brand_Id;


#4
#Query4
SELECT emp_num, First_name, LASt_name, email, tot_q  FROM (SELECT SUM(l1.Line_Qty) AS tot_q ,
emp1.Emp_Num AS emp_num, emp1.EMP_FNAME AS First_name, emp1.EMP_LNAME AS LASt_name, 
emp1.EMP_EMAIL AS email  FROM line l1 INNER JOIN invoice in1 
ON l1.Invoice_Inv_Num=in1.Inv_Num INNER JOIN employee emp1 
ON in1.Employee_Emp_Num=emp1.Emp_Num INNER JOIN product p1 
ON l1.Product_Prod_Sku=p1.PROD_SKU INNER JOIN brAND b1 
ON b1.Brand_Id=p1.Brand_Brand_Id WHERE b1.BRAND_NAME = 'BINDER PRIME' AND in1.Inv_Num not like '-%'
GROUP BY emp1.Emp_Num) q1 WHERE tot_q = (SELECT MAX(abc1.tot_q) FROM (SELECT SUM(l1.Line_Qty) AS tot_q ,emp1.Emp_Num AS emp_num,
emp1.EMP_FNAME AS First_name, emp1.EMP_LNAME AS LASt_name, emp1.EMP_EMAIL AS email FROM line l1 INNER JOIN invoice in1 
ON l1.Invoice_Inv_Num=in1.Inv_Num INNER JOIN employee emp1 
ON in1.Employee_Emp_Num=emp1.Emp_Num INNER JOIN product p1 ON l1.Product_Prod_Sku=p1.PROD_SKU INNER JOIN brAND b1 
ON b1.Brand_Id=p1.Brand_Brand_Id 
WHERE b1.BRAND_NAME = 'BINDER PRIME' AND in1.Inv_Num not like '-%'
AND in1.INV_DATE between ('2015-11-01') AND ('2015-12-05') GROUP BY emp1.Emp_Num) abc1) 
ORDER BY LASt_name;


#5
SELECT a.Cust_Code, a.cust_lname, a.cust_fname FROM (SELECT c.Cust_Code, c.cust_fname, c.cust_lname FROM customer c INNER JOIN
invoice i ON c.Cust_Code = i.Customer_Cust_Code WHERE i.Employee_Emp_Num = 83649) a INNER JOIN
(SELECT c.Cust_Code, c.cust_fname,c.cust_lname 
FROM customer c INNER JOIN invoice i ON c.Cust_Code = i.Customer_Cust_Code WHERE i.Employee_Emp_Num = 83677) b 
ON a.Cust_Code=b.Cust_Code ORDER BY a.cust_lname, a.cust_fname;

#6
SELECT cus.Cust_Code, cus.cust_fname, cus.cust_lname, cus.cust_street, cus.cust_city, cus.cust_state, cus.cust_zip, inv1.inv_date, 
MAX(COALESCE(inv1.Invoice_Total,0)) AS MAX_inv FROM customer cus left outer JOIN invoice inv1 ON 
cus.Cust_Code = inv1.Customer_Cust_Code WHERE cus.cust_state = 'AL' AND inv1.Inv_Num not like '-%' GROUP BY cus.Cust_Code;

#7
SELECT BRAND_NAME, BRAND_TYPE, AVGprice, UnitsSold FROM BRAND b JOIN (SELECT p.Brand_Brand_id, AVG(p.prod_price) AS AVGprice 
FROM product p GROUP BY Brand_Brand_Id) sub1 
ON b.Brand_Id = sub1.Brand_Brand_Id JOIN (SELECT p.Brand_Brand_id, SUM(l.Line_Qty) AS UnitsSold FROM product p JOIN line l 
ON p.Prod_Sku = l.Product_Prod_Sku GROUP BY Brand_Brand_Id) sub2 
ON b.Brand_Id = sub2.Brand_Brand_Id ORDER BY BRAND_NAME;

#8
SELECT brd.BRAND_NAME, brd.BRAND_TYPE, prd.prod_sku, prd.prod_descript, prd.prod_price FROM product prd INNER JOIN brand brd 
ON prd.Brand_Brand_Id=brd.Brand_Id WHERE brd.BRAND_TYPE <> 'PREMIUM' AND prd.prod_price > (SELECT MAX(prd1.prod_price) 
FROM product prd1 INNER JOIN BRAND brd1 
ON prd1.Brand_Brand_Id=brd1.Brand_Id WHERE brd1.BRAND_TYPE = 'PREMIUM');

#9
# (i)
SELECT * FROM product WHERE prod_price > 50;
# (ii)
SELECT SUM(prod_qoh*prod_price) AS 'Total_Value' FROM product;
# (iii)
SELECT count(distinct(c.Cust_Code)) AS "NumberofCustomers", SUM(c.cust_balance) AS "TotalofAll_Customer_Balances" FROM customer c;
# (iv)
SELECT cus.CUST_STATE,SUM(inv.Invoice_Total) AS inv_tot FROM customer cus INNER JOIN invoice inv 
ON cus.Cust_Code=inv.Customer_Cust_Code WHERE inv.Inv_Num not like '-%'
GROUP BY cus.CUST_STATE 
ORDER BY inv_tot desc limit 3;