{{ config(materialized='table') }}

with source as (

    select * from {{ source('raw', 'orders') }}

),

renamed as (

    select
        order_id::int                       as order_id,
        customer_id::int                    as customer_id,
        order_date::date                    as order_date,
        lower(trim(status))                 as status,
        amount::numeric(10, 2)              as amount,
        _loaded_at,
        current_timestamp                   as dbt_loaded_at
    from source

)

select * from renamed
