with source as (
    select 
        email,
        city,
        hobby,
        skill,
        salary,
        "Last Name",
        "Birth Date",
        experience,
         "First Name",
        "Start Date",
        nationality,
        _ab_source_file_url,
        _ab_additional_properties,
        _ab_source_file_last_modified,
        _airbyte_ab_id,
        _airbyte_emitted_at,
        _airbyte_normalized_at,
        _airbyte_fake_data_employees_hashid,
        _airbyte_unique_key
    from {{ source('public', 'fake_data_employees') }}
)
, renamed as (
    select 
        email,
        city,
        hobby,
        skill,
        salary,
        "Last Name" as Last_Name,
        "Birth Date" as Birth_Date,
        experience,
        "First Name" as First_Name,
        "Start Date" as Start_Date,
        nationality
    from source
)

select * 
from renamed