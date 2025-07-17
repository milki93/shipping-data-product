with dates as (
  select distinct
    date_trunc('day', message_date) as date_day
  from {{ ref('stg_telegram_messages') }}
  where message_date is not null
)
select
  date_day as date,
  extract(year from date_day) as year,
  extract(month from date_day) as month,
  extract(day from date_day) as day
from dates 