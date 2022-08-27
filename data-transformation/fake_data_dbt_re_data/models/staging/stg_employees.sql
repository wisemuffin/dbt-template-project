with source as (
    select 
        "Email",
        "City",
        "Hobby",
        "Skill",
        "Salary",
        "Last Name",
        "Birth Date",
        "Experience",
         "First Name",
        "Start Date",
        "Nationality",
        effective_from_ts
        {# _ab_source_file_url,
        _ab_additional_properties,
        _ab_source_file_last_modified,
        _airbyte_ab_id,
        _airbyte_emitted_at,
        _airbyte_normalized_at,
        _airbyte_fake_data_employees_hashid,
        _airbyte_unique_key #}
    from {{ source('workday', 'data_employees') }}
)
, renamed as (
    select 
        "Email" as email,
        "City" as city,
        "Hobby" as hobby,
        "Skill" as skill,
        "Salary" as salary,
        "Last Name" as Last_Name,
        "Birth Date" as Birth_Date,
        "Experience" as experience,
        "First Name" as First_Name,
        "Start Date" as Start_Date,
        "Nationality" as nationality
    from source
)

select * 
from renamed