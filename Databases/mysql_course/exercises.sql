select reverse(
        upper('hello there im playing with sql ')
    ) as reverse_upper;

select replace(concat('I', ' ', 'like', ' ', 'cats'), ' ', '_');

select replace(title, ' ', '->') as title
from books;

select author_fname as forwards,
    reverse(author_fname) as backwards
from books;

select upper(concat(author_fname, ' ', author_lname)) as 'full name in caps'
from books;

select title,
    char_length(title) as 'character count'
from books;

select concat(substring(title, 1, 10), '...') as "short title",
    concat(author_lname, ',', author_fname) as author,
    concat(stock_quantity, ' in stock') as quantity
from books;