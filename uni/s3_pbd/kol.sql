-- Zad. 1.
use library
select concat(firstname, ' ', middleinitial, '. ', lastname) as ChildName
from juvenile as j
inner join member as m on m.member_no = j.member_no
inner join loanhist as l on l.member_no = j.member_no
inner join title as t on t.title_no = l.title_no
where datediff(day, in_date, cast('2001-12-14' as date)) = 0 and title = 'Walking'

-- Zad. 2.
use Northwind2
select CompanyName, (
    select top 1 categoryname from Categories as cat
    inner join products as p on p.CategoryID = cat.CategoryID
    inner join [order details] as od on od.ProductID = p.ProductID
    inner join orders as o on o.orderid = od.OrderID
    where o.CustomerID = c_zew.CustomerID and year(orderdate) = 1997
    group by categoryname
    order by count(*) desc
) as MostFrequentlyOrderedCategory from Customers as c_zew

-- Zad. 3.
use library
select concat(m.firstname, ' ', m.middleinitial, '. ', m.lastname) as ChildName,
concat_ws(', ', street, city, [state], zip) as 'Address',
concat(ainfo.firstname, ' ', ainfo.middleinitial, '. ', ainfo.lastname) as ParentName,
(
    select count(*) from loanhist as lh
    where year(in_date) = 2001 and month(in_date) = 12 and lh.member_no = j.member_no
) as BooksReturnedByChild,
(
    select count(*) from loanhist as lh
    where year(in_date) = 2001 and month(in_date) = 12 and lh.member_no = a.member_no
) as BooksReturnedByParent
from juvenile as j
inner join member as m on m.member_no = j.member_no
inner join adult as a on a.member_no = j.adult_member_no
inner join member as ainfo on ainfo.member_no = a.member_no
