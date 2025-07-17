with channels as (
  select distinct
    channel_id,
    message_json->'peer_id'->>'channel_id' as channel_id_raw,
    message_json->'peer_id'->>'_type' as channel_type
  from {{ ref('stg_telegram_messages') }}
  where channel_id is not null
)
select
  channel_id,
  channel_id_raw,
  channel_type
from channels 