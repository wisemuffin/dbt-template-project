with source as (
    select 
        "Event ID",
        _airbyte_unique_key,
        city,
        email,
        "Last Name",
        "Birth Date",
        "First Name",
        "Start Date",
        nationality,
        "Subscription Type",
        _ab_source_file_url,
        _ab_additional_properties,
        _ab_source_file_last_modified,
        _airbyte_ab_id,
        _airbyte_emitted_at,
        _airbyte_normalized_at,
        _airbyte_fake_sub_activate_hashid
    from {{ source('public', 'fake_sub_activate') }}
)
, renamed as (
    select 
        "Event ID" as Event_ID,
        city as city,
        email as email,
        "Last Name" as Last_Name,
        "Birth Date" as Birth_Date,
        "First Name" as First_Name,
        "Start Date" as Start_Date,
        nationality as nationality,
        "Subscription Type" as Subscription_Type
    from source
)

select * 
from renamed