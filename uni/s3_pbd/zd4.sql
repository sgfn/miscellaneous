-- use Northwind2
-- cw s 20
-- 2
-- select productname, unitprice, companyname from products inner join categories on categories.categoryid = products.categoryid inner join suppliers on suppliers.supplierid = products.supplierid where categories.categoryname = 'Confections'

-- 3
-- select distinct customers.companyname, customers.phone from customers
-- inner join orders on orders.CustomerID = customers.CustomerID
-- inner join shippers on orders.shipvia = shippers.shipperid
-- where year(orders.shippeddate) = 1997 and shippers.companyname = 'United Package'


---- s 23?
-- use joindb
-- SELECT b1.buyer_name AS buyer1, p.prod_name, b2.buyer_name AS buyer2 FROM sales AS a
-- JOIN sales AS b ON a.prod_id = b.prod_id
-- join buyers as b1 on b1.buyer_id = a.buyer_id
-- join buyers as b2 on b2.buyer_id = b.buyer_id
-- join produce as p on p.prod_id = a.prod_id
-- WHERE a.buyer_id > b.buyer_id

-- s 28
-- 1
-- use library
-- select concat_ws(' ', firstname, lastname) as name, concat_ws(', ', street, city, state, zip) as address from member inner join adult on adult.member_no = member.member_no

-- 2
-- select item.isbn, copy_no, on_loan, title, translation, cover from copy inner join item on item.isbn = copy.isbn inner join title on title.title_no = copy.title_no where item.isbn in (1, 500, 1000) order by 1 asc

-- 3
-- select member.member_no, concat_ws(' ', firstname, lastname) as name, isbn, log_date from member inner join reservation as r on r.member_no = member.member_no
-- where member.member_no in (250, 342, 1675)

-- 3 koncowe
use northwind2

-- 1
-- 1.1
-- select sum(quantity), companyname from orders inner join [order details] as od on orders.orderid = od.orderid inner join customers as c on c.customerid = orders.customerid group by orders.orderid, c.companyname
-- -- 1.2
-- having sum(Quantity) > 250

-- 1.3
-- select round(sum(quantity * unitprice * (1-discount)), 2) as total, companyname from orders inner join [order details] as od on orders.orderid = od.orderid inner join customers as c on c.customerid = orders.customerid group by orders.orderid, c.companyname
-- -- 1.4
-- having sum(Quantity) > 250

-- 1.5
-- select round(sum(quantity * unitprice * (1-discount)), 2) as total, companyname, concat_ws(' ', firstname, lastname) as name from orders inner join [order details] as od on orders.orderid = od.orderid inner join customers as c on c.customerid = orders.customerid inner join employees as e on e.employeeid = orders.employeeid group by orders.orderid, c.companyname, firstname, lastname having sum(Quantity) > 250


-- 2
-- 2.1
-- select categoryname, sum(quantity) from categories as c inner join products as p on p.categoryid = c.categoryid inner join [order details] as od on od.productid = p.productid group by categoryname

-- 2.2
-- select categoryname, round(sum(quantity * od.unitprice * (1-discount)), 2) from categories as c inner join products as p on p.categoryid = c.categoryid inner join [order details] as od on od.productid = p.productid group by categoryname
-- -- 2.3a
-- order by 2 desc
-- -- 2.3b
-- order by sum(quantity) desc

-- 2.4
-- select o.orderid, round(sum(unitprice * quantity * (1-discount)) + freight, 2) from orders as o inner join [order details] as od on od.orderid = o.orderid group by o.orderid, freight

-- 3
-- 3.1
-- select companyname, count(*) from shippers as s inner join orders as o on s.shipperid = o.shipvia where year(shippeddate) = 1997 group by shipperid, companyname

-- 3.2
-- select top 1 companyname from shippers as s inner join orders as o on s.shipperid = o.shipvia where year(shippeddate) = 1997 group by companyname order by count(*) desc

-- 3.3
-- select concat_ws(' ', firstname, lastname) as name, round(sum(UnitPrice * Quantity * (1-discount)), 2) as total from employees as e inner join orders as o on o.EmployeeID = e.EmployeeID inner join [order details] as od on o.orderid = od.orderid group by e.employeeid, firstname, lastname order by 2 desc

-- 3.4
-- select top 1 concat_ws(' ', firstname, lastname) as name from employees as e inner join orders as o on o.EmployeeID = e.EmployeeID where year(orderdate) = 1997 group by e.employeeid, firstname, lastname order by count(*) desc

-- 3.5
-- select top 1 concat_ws(' ', firstname, lastname) as name from employees as e inner join orders as o on o.EmployeeID = e.EmployeeID inner join [order details] as od on o.orderid = od.orderid where year(orderdate) = 1997 group by e.employeeid, firstname, lastname order by round(sum(UnitPrice * Quantity * (1-discount)), 2) desc


-- 4a
-- select distinct concat_ws(' ', e.firstname, e.lastname) as name, round(sum(UnitPrice * Quantity * (1-discount)), 2) as total from employees as e inner join orders as o on o.EmployeeID = e.EmployeeID inner join [order details] as od on o.orderid = od.orderid join employees as subordinates on subordinates.reportsto = e.employeeid group by e.employeeid, e.firstname, e.lastname, subordinates.EmployeeID

-- 4b
-- select concat_ws(' ', e.firstname, e.lastname) as name, round(sum(UnitPrice * Quantity * (1-discount)), 2) as total from employees as e inner join orders as o on o.EmployeeID = e.EmployeeID inner join [order details] as od on o.orderid = od.orderid left join employees as subordinates on subordinates.reportsto = e.employeeid where subordinates.reportsto is null group by e.employeeid, e.firstname, e.lastname, subordinates.EmployeeID