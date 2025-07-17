with raw as (
  select
    message_json->>'id' as message_id,
    message_json->>'date' as message_date,
    message_json->>'message' as message_text,
    message_json->'peer_id'->>'channel_id' as channel_id,
    message_json->>'from_id' as from_id,
    message_json->>'grouped_id' as grouped_id,
    message_json->>'media' as media,
    message_json
  from raw.telegram_messages
)
select
  cast(message_id as integer) as message_id,
  cast(message_date as timestamp) as message_date,
  message_text,
  channel_id,
  from_id,
  grouped_id,
  media,
  message_json
from raw 