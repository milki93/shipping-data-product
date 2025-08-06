-- Fact table for YOLO image detections
-- Assumes a staging table or external table named stg_image_detections with columns matching the CSV

with detections as (
    select
        cast(message_id as bigint) as message_id, -- FK to fct_messages
        image_path,
        cast(detected_object_class as integer) as detected_object_class,
        detected_object_label,
        cast(confidence_score as float) as confidence_score,
        bbox
    from {{ ref('stg_image_detections') }}
)

select * from detections
