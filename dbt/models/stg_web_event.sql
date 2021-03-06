with source as (
    select 
        "Event End",
        _airbyte_unique_key,
        email,
        "Content",
        "Event ID",
        "Event Start",
        "Web Event Type",
        _ab_source_file_url,
        _ab_additional_properties,
        _ab_source_file_last_modified,
        _airbyte_ab_id,
        _airbyte_emitted_at,
        _airbyte_normalized_at,
        _airbyte_fake_web_events_hashid
    from {{ source('public', 'fake_web_events') }}
)
, renamed as (
    select 
        "Event End" as Event_End,
        email,
        "Content" as Content_ID,
        "Event ID" as Event_ID,
        "Event Start" as Event_Start,
        "Web Event Type" as Web_Event_Type
    from source
)

select * 
from renamed