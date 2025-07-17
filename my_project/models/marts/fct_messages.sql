with base as (
  select
    s.message_id,
    s.message_date,
    s.message_text,
    s.channel_id,
    d.date as date_key,
    c.channel_id as channel_key,
    length(s.message_text) as message_length,
    case when s.media is not null and s.media != 'null' then true else false end as has_image
  from {{ ref('stg_telegram_messages') }} s
  left join {{ ref('dim_dates') }} d on date_trunc('day', s.message_date) = d.date
  left join {{ ref('dim_channels') }} c on s.channel_id = c.channel_id
)
select * from base 