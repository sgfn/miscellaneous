-- use Northwind

-- 1
-- select firstname, lastname, birth_date from member inner join juvenile on member.member_no = juvenile.member_no

-- 2
-- select distinct title.title from loan inner join title on title.title_no = loan.title_no

-- 3
-- select in_date, datediff(day, due_date, in_date) as 'przetrzymano dni', fine_paid from loanhist inner join title on title.title_no = loanhist.title_no where title.title = 'Tao Teh King' and due_date < in_date

-- 4
-- select isbn from reservation inner join member on member.member_no = reservation.member_no where firstname = 'Stephen' and middleinitial = 'A' and lastname = 'Graff'

----
-- 2,3 w domu

-- 1
-- select productname, unitprice, address, city, region, postalcode, country from products inner join Suppliers
-- on products.SupplierID = Suppliers.SupplierID
-- inner join categories on categories.CategoryID = products.CategoryID
-- where unitprice between 20 and 30 and CategoryName = 'Meat/Poultry'

-- 4
-- select distinct companyname, phone from customers
-- inner join orders on orders.CustomerID = customers.CustomerID
-- inner join [order details] on [order details].orderid = orders.orderid
-- inner join products on products.ProductID = [order details].[ProductID]
-- inner join categories on categories.CategoryID = products.CategoryID
-- where categoryname = 'Confections'

----
-- 1
-- use Library
-- select firstname, lastname, birth_date, concat_ws(', ', street, city, state, zip) as 'address' from member
-- inner join juvenile on member.member_no = juvenile.member_no
-- inner join adult on adult.member_no = juvenile.adult_member_no

-- 2
-- select m.firstname as 'child first name', m.lastname as 'child last name', birth_date, concat_ws(', ', street, city, state, zip) as 'address', member.firstname as 'parent first name', member.lastname as 'parent last name' from member as m
-- inner join juvenile on m.member_no = juvenile.member_no
-- inner join adult on adult.member_no = juvenile.adult_member_no
-- inner join member on member.member_no = juvenile.adult_member_no

-- w domu zamiast identa nazwe produktu, zamiast czworki imie nazwisko i zamiast jedynki imie nazwisko (na joindb)


----
-- use Northwind2
-- 1
-- select boss.firstname as 'boss fname', boss.lastname as 'boss lname', empl.FirstName as 'employee fname', empl.LastName as 'employee lname' from Employees as boss
-- join Employees as empl on empl.ReportsTo = boss.EmployeeID

-- 2 - na odwrót trzeba było
-- select empl.firstname, empl.lastname from Employees as boss right outer join Employees as empl on empl.ReportsTo = boss.EmployeeID where empl.ReportsTo is NULL

use library
-- 3
-- select distinct concat_ws(', ', p.street, p.city, p.state, p.zip) as 'address' from adult as p inner join juvenile as c on c.adult_member_no = p.member_no where c.birth_date < cast('1996-01-01' as date)

-- 4
-- select distinct concat_ws(', ', p.street, p.city, p.state, p.zip) as 'address' from adult as p inner join juvenile as c on c.adult_member_no = p.member_no left outer join loan on loan.member_no = p.member_no where c.birth_date < cast('1996-01-01' as date) and (due_date >= GETDATE() or due_date is null)

-- UNION, INTERSECT, EXCEPT
-- 1, 2, 3 w domu
-- 4
select a.firstname, a.lastname from member as a inner join adult on a.member_no = adult.member_no inner join juvenile on adult.member_no = juvenile.adult_member_no where [state] = 'AZ' group by a.member_no, a.firstname, a.lastname having count(*) > 2
-- 4+
union
select a.firstname, a.lastname from member as a inner join adult on a.member_no = adult.member_no inner join juvenile on adult.member_no = juvenile.adult_member_no where [state] = 'CA' group by a.member_no, a.firstname, a.lastname having count(*) > 3

-- w ramach przygotowania do kolosa spróbować to zrobić bez union
-- zad dom: 3_1_cw_koncowe.pdf
