# No ORM models needed. All queries use raw SQL via psycopg2.

class FctImageDetections(Base):
    __tablename__ = "fct_image_detections"
    message_id = Column(Integer, primary_key=True)
    image_path = Column(String)
    detected_object_class = Column(Integer)
    detected_object_label = Column(String)
    confidence_score = Column(Float)
    bbox = Column(String)

class FctMessages(Base):
    __tablename__ = "fct_messages"
    id = Column(Integer, primary_key=True)
    channel = Column(String)
    date = Column(DateTime)
    message = Column(String)
    # Add other relevant fields as needed
