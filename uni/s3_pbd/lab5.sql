use Northwind2

-- SELECT T.orderid, T.customerid
-- FROM ( SELECT orderid, customerid
-- FROM orders ) AS T

-- SELECT productname, unitprice
-- ,( SELECT AVG(unitprice) FROM products) AS average
-- ,unitprice-(SELECT AVG(unitprice) FROM products) AS difference
-- FROM products

-- SELECT productname, unitprice
-- ,( SELECT AVG(unitprice) FROM products) AS average
-- ,unitprice-(SELECT AVG(unitprice) FROM products) AS difference
-- FROM products
-- WHERE unitprice > ( SELECT AVG(unitprice) FROM products)

-- SELECT productname, unitprice
-- ,( SELECT AVG(unitprice)
-- FROM products as p_wew
-- WHERE p_zew.categoryid = p_wew.categoryid ) AS
-- average
-- FROM products as p_zew

-- SELECT productname, unitprice
-- ,( SELECT AVG(unitprice) FROM products as p_wew
-- WHERE p_zew.categoryid = p_wew.categoryid ) AS
-- average
-- FROM products as p_zew
-- WHERE unitprice >
-- ( SELECT AVG(unitprice) FROM products as p_wew
-- WHERE p_zew.categoryid = p_wew.categoryid )


-- select distinct companyname, phone from customers as c_zew
-- where exists (
--     select * from orders as o
--     where c_zew.customerid = o.customerid and year(ShippedDate) = 1997 and shipvia = (
--         select shipperid from shippers where companyname = 'United Package'
--     )
-- )

-- select distinct companyname, phone from customers as c_zew
-- where exists (
--     select * from [order details] as od
--     where ???
-- )

-- select round(sum(unitprice*quantity*(1-discount))+freight, 2) from Orders
-- inner join [order details] as od on orders.orderid = od.orderid
-- where orders.orderid = 10250
-- group by orders.orderid, freight

select f.orderid, round(sum(unitprice*quantity*(1-discount))+f.freight, 2) from (
    select * from orders
) as f
inner join [order details] as od on f.orderid = od.orderid
group by f.orderid, freight

-- cw koncowe 4: 2, 3, 4.2-4, 5 -> do domu