# imports all dependencies
from imports.imports import *
# database configuration using ORM (object relation mapping)
class dbInit:
    def __init__(self, application) -> None:
        self.app = application
        self.exam_instance = None
        self.admin = None
        self.frames = None
        self.proctor = None
        self.exam_instance_cases = None
        self.admin_assign_proctor = None
        self.proctor_monitor_exam = None
        self.students_positions = None
        self.classroom_monitoring_db = SQLAlchemy(self.app) 
        self.Base = automap_base()
        self.Base.prepare(self.classroom_monitoring_db.engine,reflect=True)
        
    def modelTables(self) -> None:
        ## model Tables
        self.exam_instance = self.Base.classes.exam_instance
        self.admin = self.Base.classes.admin
        self.frames = self.Base.classes.frames
        self.proctor = self.Base.classes.proctor
        self.exam_instance_cases = self.Base.classes.exam_instance_cases
        self.admin_assign_proctor = self.Base.classes.admin_assign_proctor
        self.proctor_monitor_exam = self.Base.classes.proctor_monitor_exam
        self.students_positions = self.Base.classes.students_positions
