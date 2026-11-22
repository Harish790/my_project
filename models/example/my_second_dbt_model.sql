-- Use the `ref` function to select from other models.
-- Keeps only the rows with id 1-3 from the first model.

select
    id,
    second_id
from {{ ref('my_first_dbt_model') }}
where id <= 3
