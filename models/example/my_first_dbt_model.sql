/*
    First model: a small set of rows with an id and a second_id.
    Materialized as a table (overrides the 'view' default in dbt_project.yml).
*/

{{ config(materialized='table') }}

with source_data as (

    select 1 as id, 101 as second_id
    union all
    select 2 as id, 102 as second_id
    union all
    select 3 as id, 103 as second_id
    union all
    select 4 as id, 104 as second_id
    union all
    select 5 as id, 105 as second_id

)

select *
from source_data
where id is not null
