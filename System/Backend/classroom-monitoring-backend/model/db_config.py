# imports all dependencies
from imports.imports import *
# database configuration using ORM (object relation mapping)
class dbInit:
    def __init__(self, application) -> None:
        self.app = application
        self.ExamRoom = None
        self.Admin = None
        self.cheatingincidents = None
        self.frames = None
        self.proctor = None
        self.examincidents = None
        self.proctorExamAssignment = None
        self.classroom_monitoring_db = SQLAlchemy(self.app) 
        self.Base = automap_base()
        self.Base.prepare(self.classroom_monitoring_db.engine,reflect=True)
        
    def modelTables(self) -> None:
        ## model Tables
        self.ExamRoom = self.Base.classes.examroom
        self.Admin = self.Base.classes.adminstrator
        self.cheatingincidents = self.Base.classes.cheatingincidents
        self.frames = self.Base.classes.frames
        self.proctor = self.Base.classes.proctor
        self.examincidents = self.Base.classes.examIncidents
        self.proctorExamAssignment = self.Base.classes.proctor_adminstrator_assign
