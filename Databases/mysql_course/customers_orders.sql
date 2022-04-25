CREATE TABLE customers(
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(100)
);

CREATE TABLE orders(
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_date DATE,
    amount DECIMAL(8, 2),
    customer_id INT,
    FOREIGN KEY(customer_id) REFERENCES customers(id) on delete cascade
);

select
    *
from
    orders
where
    customer_id =(
        select
            id
        from
            customers
        where
            last_name = 'George'
    );

select
    *
from
    customers,
    orders
where
    customers.id = orders.customer_id;

select
    first_name,
    last_name,
    order_date,
    amount
from
    customers,
    orders
where
    customers.id = orders.customer_id;

select
    first_name,
    last_name,
    ifnull(sum(amount), 0) as total_spent
from
    customers
    left join orders on customers.id = orders.customer_id
group by
    orders.customer_id;

select
    first_name,
    last_name,
    order_date,
    amount
from
    customers
    right join orders on customers.id = orders.customer_id;

create table students(
    id int auto_increment primary key,
    first_name varchar(100)
);

create table papers(
    title varchar(100),
    grade int,
    student_id int,
    FOREIGN KEY (student_id) references students(id) on delete cascade
);

select
    first_name,
    title,
    grade
from
    students
    inner join papers on students.id = papers.student_id
order by
    grade desc;

select
    first_name,
    title,
    grade
from
    students
    left join papers on students.id = papers.student_id;

select
    first_name,
    ifnull(title, "MISSING") as title,
    ifnull(grade, 0) as grade
from
    students
    left join papers on students.id = papers.student_id;

select
    first_name,
    ifnull(avg(grade), 0) as average
from
    students
    left join papers on students.id = papers.student_id
group by
    students.id
order by
    grade desc;

select
    first_name,
    ifnull(avg(grade), 0) as average,
    case
        when avg(grade) >= 75 then "PASSING"
        else "FAILING"
    end as passing_status
from
    students
    left join papers on students.id = papers.student_id
group by
    students.id
order by
    average desc;

-- =========================================================================
