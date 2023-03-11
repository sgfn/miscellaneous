use Library

-- CW 1
-- 1
-- select title, title_no from title

-- 2
-- select title from title where title_no = 10

-- 3
-- select member_no, fine_assessed from loanhist where fine_assessed between 8 and 9

-- 4
-- select title_no, author from title where author in ('Jane Austen', 'Charles Dickens')

-- 5
-- select title_no, title from title where title like '%adventures%'

-- 6
-- select member_no, ISNULL(fine_assessed, 0) as 'f_ass', 
-- ISNULL(fine_paid, 0) as 'f_pai', ISNULL(fine_waived, 0) as 'f_wai'
-- from loanhist
-- where ISNULL([fine_assessed], 0) != ISNULL(fine_paid, 0) + ISNULL(fine_waived, 0)

-- 7
-- select distinct city, [state] from adult


-- CW 2
-- 1
-- select title from title order by title

-- 2
-- select member_no, isbn, fine_assessed, fine_assessed*2 as 'double fine' from loanhist where fine_assessed is not NULL and fine_assessed > 0

-- 3
-- select LOWER(firstname + middleinitial + SUBSTRING(lastname, 1, 2)) as 'email_name' from member where lastname = 'Anderson'

-- 4
-- select CONCAT('The title is: ', title, ' title number ', title_no) as sth from title

-- select ('The title is: ' + title + ' title number ' + CAST(title_no as VARCHAR)) as sth from title
