use Northwind

-- select CONCAT(ISNULL(phone, ''), ', ', ISNULL(fax, '')) from Suppliers

-- select orderID, count(*) from [Order Details] group by orderID having count(*)>5

-- select customerid, count(*) as 'ilosc zamowien', sum(freight) as 'laczny koszt dostawy' from orders where YEAR(orderdate) = 1998 group by customerid having count(*)>8 order by 3 desc

-- do domu:
-- ćw końcowe z agregatów
-- rzeczy z group by ... with rollup/cube

-- use joindb
-- select buyer_name, s.buyer_id, qty from Buyers as b INNER JOIN Sales as s ON b.buyer_id = s.buyer_id

-- SELECT companyname, customers.customerid, orderdate
-- FROM customers
-- LEFT OUTER JOIN orders
-- ON customers.customerid = orders.customerid
-- where orders.CustomerID is NULL

-- select productname, unitprice, address, city, region, postalcode, country from products inner join Suppliers
-- on products.SupplierID = Suppliers.SupplierID
-- where unitprice between 20 and 30

select customerid from orders

-- select productname, unitprice, address, city, region, postalcode, country from products inner join Suppliers
-- on products.SupplierID = Suppliers.SupplierID
-- inner join categories on categories.CategoryID = products.CategoryID
-- where unitprice between 20 and 30 and CategoryName = 'Meat/Poultry'

-- select productname, unitprice, CompanyName from products inner join categories on categories.CategoryID = products.ProductID
-- inner join suppliers on products.SupplierID = Suppliers.SupplierID
-- where CategoryName = 'Confections'

-- select orders.customerid from orders
-- inner join shippers on shipperid = shipvia
-- inner join customers on customers.CustomerID = orders.CustomerID
-- where year(shippeddate)