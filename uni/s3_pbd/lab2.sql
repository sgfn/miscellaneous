use Northwind

-- select * from Products where QuantityPerUnit like '%bottle%'
-- select Title from Employees where LastName like '[B-L]%'
-- select Title from Employees where LastName like '[BL]%'
-- select CategoryName from Categories where Description like '%,%'
-- select * from [Customers] where CompanyName like '%Store%'

-- select * from Products where UnitPrice not BETWEEN 10 and 20

-- select OrderID, OrderDate, CustomerID from Orders
--     where (ShippedDate is NULL or ShippedDate > getdate())
--           and ShipCountry = 'Argentina'

-- select CompanyName, Country from Customers
-- order by 2, 1

-- select CategoryID, ProductName, UnitPrice from Products
-- order by 1, 3 DESC

-- select CompanyName, Country from Customers
--     where Country in ('UK', 'Italy')
--     order by 2, 1

-- select distinct Country, City from Suppliers order by 1

-- select FirstName as Imie, LastName as Nazwisko, 'Nr seryjny', employeeId as 'Nr seryjny'
-- from Employees

-- select orderid, unitprice, cast(unitprice * 1.05 as money) as newunitprice
-- from [order details]

-- ZAD DOM - zadania z cw końcowego 1


---------------------------------------------------------
-- select top 5 with ties orderid, productid, quantity
-- from [Order Details]
-- order by quantity desc

-- select count(*) from Employees go
-- select count(reportsto) from employees go

-- select avg(unitprice), min(unitprice) from products

-- select count(*) from products where unitprice not between 10 and 20
-- select max(unitprice) from products where unitprice < 20
-- select max(unitprice), min(unitprice), avg(unitprice) from Products
--     where QuantityPerUnit like '%bottle%'


-- select avg(unitprice) from Products
-- select * from Products where unitprice > (select avg(UnitPrice) from Products)
-- select * from Products where unitprice > avg(unitprice) -- ERROR (aggregate nie może być w klauzuli where)

-- select round(sum(Quantity*UnitPrice*(1-Discount)),2) from [Order Details]
-- where orderID = 10250

-- select productid, sum(quantity) from orderhist group by productid

-- select orderid, max(unitprice) from [order details] group by OrderID

-- select orderid, max(unitprice) from [order details] group by OrderID order by 2 desc

-- select orderid, max(unitprice), min(unitprice) from [order details] group by OrderID

-- select shipvia, count(*) from orders group by shipvia

-- select top 1 shipvia, count(*) from orders where YEAR(shippeddate) = 1997 group by shipvia order by 2 desc
