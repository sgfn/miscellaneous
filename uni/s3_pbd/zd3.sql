use Northwind

-- CW 1
-- 1
-- select orderid, sum(quantity*unitprice*(1-discount)) as 'wartosc sprzedazy' from [order details] group by orderid order by 2 desc

-- 2
-- select top 10 orderid, sum(quantity*unitprice*(1-discount)) as 'wartosc sprzedazy' from [order details] group by orderid order by 2 desc


-- CW 2
-- 1
-- select productid, sum(quantity) from [order details] where productid < 3 group by productid

-- 2
-- select productid, sum(quantity) from [order details] group by productid

-- 3
-- select orderid, sum (quantity*unitprice*(1-discount)) as 'wartosc zamowienia' from [order details] group by orderid having sum(quantity) > 250


-- CW 3
-- 1
-- select employeeid, count(*) from orders group by employeeid

-- 2
-- select shipvia, sum(freight) from orders group by shipvia

-- 3
-- select shipvia, sum(freight) from orders where year(shippeddate) between 1996 and 1997 group by shipvia


-- CW 4
-- 1
-- select employeeid, year(orderdate) as 'rok', month(orderdate) as 'miesiac', count(*) as 'zamowienia' from orders group by employeeid, year(orderdate), month(orderdate)

-- 2
-- select categoryid, max(unitprice) as 'max cena', min(unitprice) as 'min cena' from products group by categoryid
