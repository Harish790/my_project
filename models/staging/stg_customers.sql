{{ config(materialized='table') }}

with source as (

    select * from {{ source('raw', 'customers') }}

),

renamed as (

    select
        customer_id::int                    as customer_id,
        trim(first_name)                    as first_name,
        trim(last_name)                     as last_name,
        trim(first_name) || ' ' || trim(last_name) as full_name,
        lower(trim(email))                  as email,
        trim(city)                          as city,
        signup_date::date                   as signup_date,
        _loaded_at,
        current_timestamp                   as dbt_loaded_at
    from source

)

select * from renamed
