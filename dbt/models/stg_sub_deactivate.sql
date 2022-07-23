with source as (
    select 
        "Event ID" AS Event_ID,
        _airbyte_unique_key,
        email,
        "End Date" as End_Date,
        _ab_source_file_url,
        _ab_additional_properties,
        _ab_source_file_last_modified,
        "Subscription Termination Reason" as Subscription_Termination_Reason,
        _airbyte_ab_id,
        _airbyte_emitted_at,
        _airbyte_normalized_at,
        _airbyte_fake_sub_deactivate_hashid
    from {{ source('public', 'fake_sub_deactivate') }}
)
, renamed as (
    select 
        "Event ID" AS Event_ID,
        email,
        "End Date" as End_Date,
        "Subscription Termination Reason" as Subscription_Termination_Reason
    from source
)

select * 
from renamed