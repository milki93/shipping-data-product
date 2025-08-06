with base as (
  select
    s.message_id as id,
    s.channel_id as channel,
    s.message_date as date,
    s.message_text as message
  from {{ ref('stg_telegram_messages') }} s
)
select * from base 