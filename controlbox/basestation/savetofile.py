from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
import os.path
import os


# Database connection
DATABASE = 'sqlite:///wolfnetdata'
DEBUG = True

# ORM base
Base = declarative_base()

engine = create_engine(DATABASE, echo=DEBUG)


# ORM types
class MyRecord(Base):
    __tablename__ = 'record'

    id = Column(Integer, primary_key=True, autoincrement=True)
    time = Column(String, nullable=False)
    sendaddress = Column(String, nullable=False)
    recaddress = Column(String, nullable=False)
    broadcast = Column(String)
    batteryvolt = Column(Integer)
    batteryperc = Column(String)
    duration = Column(Integer)
    frequency = Column(Integer)
    rssi = Column(String)
    snr = Column(String)

    def __init__(self, id, time, sendaddress, recaddress, broadcast, batteryperc, batteryvolt, duration, frequency, rssi, snr):
        self.id = id
        self.time = time
        self.sendaddress = sendaddress
        self.recaddress = recaddress
        self.broadcast = broadcast
        self.batteryperc = batteryperc
        self.batteryvolt = batteryvolt
        self.duration = duration
        self.frequency = frequency
        self.rssi = rssi
        self.snr = snr

    def __repr__(self):
        return '("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")' % (self.time, self.sendaddress, self.recaddress, self.broadcast, self.batteryvolt, self.batteryperc, self.duration, self.frequency, self.rssi, self.snr)
    
    def savedata(recdata):
        with Session(engine) as ses:
            ses.add(recdata)
            ses.commit()
    
    def showdata():
        with Session(engine) as session:
            records = session.query(MyRecord).all()
        return records
    
    def setup():
        if os.path.exists('wolfnetdata'):
            os.remove('wolfnetdata')
        Base.metadata.create_all(engine)