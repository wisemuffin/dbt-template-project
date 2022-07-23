with source as (
    select 
        "Content ID",
        genre,
        "Sub Genre",
        instrument,
        "Content Name",
        "Instrument Category",
        _ab_source_file_url,
        _ab_additional_properties,
        _ab_source_file_last_modified,
        _airbyte_ab_id,
        _airbyte_emitted_at,
        _airbyte_normalized_at ,
        _airbyte_fake_content_hashid
    from {{ source('public', 'fake_content') }}
)
, renamed as (
    select 
        "Content ID" as Content_ID,
        genre,
        "Sub Genre" as Sub_Genre,
        instrument,
        "Content Name" as Content_Name,
        "Instrument Category" as Instrument_Categor
    from source
)

select * 
from renamed