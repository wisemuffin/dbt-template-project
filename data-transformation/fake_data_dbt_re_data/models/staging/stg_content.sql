with source as (
    select 
        "Content ID",
        "Genre",
        "Sub Genre",
        "Instrument",
        "Content Name",
        "Instrument Category",
        effective_from_ts
        {# _ab_source_file_url,
        _ab_additional_properties,
        _ab_source_file_last_modified,
        _airbyte_ab_id,
        _airbyte_emitted_at,
        _airbyte_normalized_at ,
        _airbyte_fake_content_hashid #}
    from {{ source('website', 'content') }}
)
, renamed as (
    select 
        "Content ID" as Content_ID,
        "Genre" as genre,
        "Sub Genre" as Sub_Genre,
        "Instrument" instrument,
        "Content Name" as Content_Name,
        "Instrument Category" as Instrument_Categor
    from source
)

select * 
from renamed