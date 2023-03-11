use Northwind2


-- 2.1
-- select distinct productid, quantity
-- from [order details] as ord1
-- where quantity = (select MAX(quantity) from [order details] as ord2 where ord1.ProductID = ord2.ProductID)

-- 2.2
-- select productname, unitprice from products
-- where unitprice < (
--     select avg(unitprice) from products
-- )

-- 2.3
-- select productname, unitprice from products as p_zew
-- where unitprice < (
--     select avg(unitprice) from products as p_wew
--     where p_zew.CategoryID = p_wew.CategoryID
-- )

-- 3.1
-- select productname, unitprice, (select avg(unitprice) from products), unitprice-(select avg(unitprice) from products) from products

-- 3.2
-- select (select categoryname from categories as c where c.CategoryID = p_zew.CategoryID) as category, productname, unitprice, (select avg(unitprice) from products as p_wew where p_wew.CategoryID = p_zew.CategoryID), unitprice-(select avg(unitprice) from products as p_wew where p_wew.CategoryID = p_zew.CategoryID) from products as p_zew

-- 4.2
-- select o.orderid, o.freight+(select sum(od.quantity*od.unitprice*(1-od.discount)) from [order details] as od where od.orderid = o.orderid group by od.orderid) as total from orders as o

-- 4.3
-- select customerid, address, city, region, postalcode, country from customers
-- where not exists(select orderid from orders where year(OrderDate) = 1997 and orders.CustomerID = customers.CustomerID)

-- 4.4
-- select productid from products as p_zew
-- where (
--     select count(*) from orders as o
--     inner join [Order Details] as od on o.orderid = od.OrderID
--     where od.productid = p_zew.ProductID
--     group by productid
-- ) > 1


-- 5.1
-- select firstname, lastname, (
--     select sum(quantity*unitprice*(1-discount)) from [Order Details] as od
--     inner join orders as o on o.orderid = od.orderid
--     where e.EmployeeID = o.EmployeeID
-- ) + (
--     select sum(freight) from orders as o
--     where e.EmployeeID = o.EmployeeID
-- ) from Employees as e

-- 5.2
-- select top 1 firstname, lastname, (
--     select sum(quantity*unitprice*(1-discount)) from [Order Details] as od
--     inner join orders as o on o.orderid = od.orderid
--     where e.EmployeeID = o.EmployeeID and year(o.OrderDate) = 1997
-- ) + (
--     select sum(freight) from orders as o
--     where e.EmployeeID = o.EmployeeID and year(o.OrderDate) = 1997
-- ) from Employees as e
-- order by 3 desc

-- 5.3a,b
-- select firstname, lastname, (
--     select sum(quantity*unitprice*(1-discount)) from [Order Details] as od
--     inner join orders as o on o.orderid = od.orderid
--     where e.EmployeeID = o.EmployeeID
-- ) + (
--     select sum(freight) from orders as o
--     where e.EmployeeID = o.EmployeeID
-- ) from Employees as e
-- where
-- -- not -- UNCOMMENT FOR 5.3b
-- exists(
--     select subordinates.employeeid from employees as subordinates
--     inner join employees as e_wew on subordinates.ReportsTo = e_wew.EmployeeID
--     where e.EmployeeID = e_wew.EmployeeID
-- )

-- 5.4
-- select firstname, lastname, (
--     select sum(quantity*unitprice*(1-discount)) from [Order Details] as od
--     inner join orders as o on o.orderid = od.orderid
--     where e.EmployeeID = o.EmployeeID
-- ) + (
--     select sum(freight) from orders as o
--     where e.EmployeeID = o.EmployeeID
-- ), (
--     select top 1 orderdate from orders as o
--     where e.EmployeeID = o.EmployeeID
--     order by 1 desc
-- ) from Employees as e
-- where
-- -- not -- UNCOMMENT FOR 5.4b
-- exists(
--     select subordinates.employeeid from employees as subordinates
--     inner join employees as e_wew on subordinates.ReportsTo = e_wew.EmployeeID
--     where e.EmployeeID = e_wew.EmployeeID
-- )
