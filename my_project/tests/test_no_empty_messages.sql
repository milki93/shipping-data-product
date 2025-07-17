-- Custom test: Ensure there are no messages with empty text
select * from {{ ref('fct_messages') }} where message_text is null or message_text = '' 