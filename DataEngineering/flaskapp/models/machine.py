from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String
from sqlalchemy.types import DateTime, Integer, String, DateTime, JSON, Float,Boolean,BIGINT
# from pangres import upsert
from sqlalchemy.orm import relationship
from app import db



class Line(db.Model):
    __tablename__ = 'line'

    LineID = db.Column(Integer, primary_key=True, autoincrement=False)

    LineCode = db.Column(String(64))
    LineDescription = db.Column(String(64))
    CreatedAt = db.Column(DateTime)
    UpdatedAt = db.Column(DateTime)



class Machine(db.Model):
    __tablename__ = 'machine'

    MachineID  = db.Column(Integer, primary_key=True,  autoincrement=False)

    MachineCode = db.Column(String(64))
    MachineDescription = db.Column( String(64))
    MachineImageUrl = db.Column( String(2056))
    MachineThumbnailUrl = db.Column( String(2056))
    MachineTypeID = db.Column( Integer,db.ForeignKey("machine_type.MachineTypeID"))
    ActiveWorkerID =db.Column( Integer, db.ForeignKey("worker.WorkerID"))
    LineID = db.Column( Integer,db.ForeignKey("line.LineID"))
    Operations =db.Column(JSON)
    CreatedAt=db.Column(DateTime)
    UpdatedAt =db.Column(DateTime)
    BoxID=db.Column(Integer)
    #db.ColumnS ADDED LATER
    IsMachineDown=db.Column(Boolean)
    LineCode =db.Column( String(64))
    LineDescription =db.Column( String(64))  
    WorkerID=db.Column(Integer)
    WorkerCode=db.Column(String(64))
    WorkerDescription=db.Column( String(64))
    WorkerImageUrl=db.Column(String(2056))
    WorkerThumbnailUrl=db.Column(String(2056))
    AllocatedMachines=db.Column(JSON)
    MachineTypeCode =db.Column(String(64))
    MachineTypeDescription=db.Column( String(64))
    Allowance=db.Column( Float)    

    line = relationship("Line")
    machine_type = relationship("MachineType")
    worker = relationship("Worker")




class MachineType(db.Model):
    __tablename__ = 'machine_type'

    MachineTypeID=db.Column(Integer, primary_key = True, autoincrement=False)

    MachineTypeCode=db.Column(String(64))
    MachineTypeDescription=db.Column(String(64))
    Allowance=db.Column(Float)
    CreatedAt=db.Column(DateTime)
    UpdatedAt=db.Column(DateTime)


class Worker(db.Model):
    __tablename__ = 'worker'

    WorkerID=db.Column(Integer, primary_key = True, autoincrement=False)

    WorkerCode=db.Column(String(64))
    WorkerDescription=db.Column(String(64))
    WorkerImageUrl=db.Column(String(2056))
    WorkerThumbnailUrl=db.Column(String(2056))
    AllocatedMachines=db.Column(JSON)
    CreatedAt=db.Column( DateTime)
    UpdatedAt=db.Column(DateTime)

# db.Model.metadata.create_all(engine_postgres)


class WorkerScan(db.Model):
    __tablename__ = 'worker_scan'
    # additional arguments to be supplied to the Table constructor should be provided using the __table_args__ declarative class attribute.
    __table_args__ = {'extend_existing': True}

    WorkerScanID=db.Column(BIGINT, primary_key = True, autoincrement=False) 

    WorkerID =db.Column(Integer, db.ForeignKey("worker.WorkerID"))
    LineID=db.Column(Integer,db.ForeignKey("line.LineID"))
    MachineID=db.Column(Integer,db.ForeignKey("machine.MachineID"))
    WorkerOperations=db.Column(JSON)
    CreatedAt=db.Column(DateTime) 
    UpdatedAt=db.Column(DateTime)  
    HasExpired=db.Column(Integer)
    EndedAt=db.Column(DateTime) 
    LineCode=db.Column(String(64))
    LineDescription=db.Column(String(64)) 
    WorkerCode=db.Column(String(64))
    WorkerDescription=db.Column(String(64)) 
    WorkerImageUrl=db.Column(String(2056)) 
    WorkerThumbnailUrl=db.Column(String(2056)) 
    AllocatedMachines=db.Column(JSON)
    MachineCode=db.Column(String(64))
    MachineDescription=db.Column(String(64))
    MachineImageUrl=db.Column(String(2056)) 
    MachineThumbnailUrl=db.Column(String(2056))
    MachineTypeID=db.Column(Integer, db.ForeignKey("machine_type.MachineTypeID"))
    ActiveWorkerID=db.Column(Integer)
    Operations=db.Column(JSON)
    BoxID=db.Column(Integer)
    #db.Column ADDED LATER
    IsMachineDown=db.Column(Boolean)
    MachineTypeCode=db.Column(String(64)) 
    MachineTypeDescription=db.Column(String(64)) 
    Allowance=db.Column(Float)
    

    line = relationship("Line")
    machine = relationship("Machine")
    worker = relationship("Worker")
    machine_type = relationship("MachineType") 

class ProductionOrder(db.Model):
    __tablename__ = 'production_order'
    __table_args__ = {'extend_existing': True}

    ProductionOrderID=db.Column(Integer, primary_key = True, autoincrement=False) 
    
    ProductionOrderCode=db.Column(String(64))
    SaleOrderID=db.Column(Integer, db.ForeignKey("sale_order.SaleOrderID"))
    StyleTemplateID=db.Column(Integer, db.ForeignKey("style_template.StyleTemplateID"))    
    IsFollowOperationSequence=db.Column(Boolean)
    CreatedAt=db.Column(DateTime) 
    UpdatedAt=db.Column(DateTime)  
    
    SaleOrderCode=db.Column(String(100))
    Customer=db.Column(String(64))
    OrderQuantity=db.Column(Integer)            

    StyleTemplateCode=db.Column(String(64))

    
    sale_order = relationship("SaleOrder")
    style_template = relationship("StyleTemplate")


class SaleOrder(db.Model):
    __tablename__ = 'sale_order'
    __table_args__ = {'extend_existing': True}

    SaleOrderID=db.Column(Integer, primary_key = True, autoincrement=False) 
    SaleOrderCode=db.Column(String(100))

    Customer=db.Column(String(64))
    OrderQuantity=db.Column(Integer)     
    CreatedAt=db.Column(DateTime) 
    UpdatedAt=db.Column(DateTime)  


class StyleTemplate(db.Model):
    __tablename__ = 'style_template'
    __table_args__ = {'extend_existing': True}

    StyleTemplateID=db.Column(Integer, primary_key = True, autoincrement=False) 
    StyleTemplateCode=db.Column(String(64))     
    CreatedAt=db.Column(DateTime) 
    UpdatedAt=db.Column(DateTime) 


# db.Model.metadata.create_all(engine_postgres)
class Marker(db.Model):
    __tablename__ = 'marker'
    __table_args__ = {'extend_existing': True}

    MarkerID=db.Column(Integer, primary_key = True, autoincrement=False) 
    MarkerCode=db.Column(String(64))    
    ProductionOrderID=db.Column(Integer, db.ForeignKey("production_order.ProductionOrderID"))
    MarkerMapping=db.Column(JSON)  
    CreatedAt=db.Column(DateTime) 
    UpdatedAt=db.Column(DateTime)  
    ProductionOrderCode=db.Column(String(64))
    
    SaleOrderID=db.Column(Integer, db.ForeignKey("sale_order.SaleOrderID"))
    StyleTemplateID=db.Column(Integer, db.ForeignKey("style_template.StyleTemplateID"))

    IsFollowOperationSequence=db.Column(Boolean)
    SaleOrderCode=db.Column(String(100))
    Customer=db.Column(String(64))
    OrderQuantity=db.Column(Integer)    
    
    StyleTemplateCode=db.Column(String(64))   
    
    # Size=db.Column(Integer) 
    # Inseam=db.Column(Integer) 
    # Ratio=db.Column(Integer) 


    production_order = relationship("ProductionOrder")
    sale_order = relationship("SaleOrder")
    style_template = relationship("StyleTemplate")


class CutJob(db.Model):
    __tablename__ = 'cut_job'
    __table_args__ = {'extend_existing': True}

    CutJobID=db.Column(Integer, primary_key = True, autoincrement=False) 
    CutNo=db.Column(Integer)
    ProductionOrderID=db.Column(Integer, db.ForeignKey("production_order.ProductionOrderID"))
    CutQuantity=db.Column(Integer)




    MarkerID=db.Column(Integer, db.ForeignKey("marker.MarkerID")) 
    CreatedAt=db.Column(DateTime) 
    UpdatedAt=db.Column(DateTime)  
    ProductionOrderCode=db.Column(String(64))
    SaleOrderID=db.Column(Integer, db.ForeignKey("sale_order.SaleOrderID"))
    StyleTemplateID=db.Column(Integer, db.ForeignKey("style_template.StyleTemplateID"))
    IsFollowOperationSequence=db.Column(Boolean)
    SaleOrderCode=db.Column(String(100))
    Customer=db.Column(String(64))


    
    OrderQuantity=db.Column(Integer)    
    
    StyleTemplateCode=db.Column(String(64))   
    MarkerCode=db.Column(String(64))    
    
    MarkerMapping=db.Column(JSON)    

    production_order = relationship("ProductionOrder")
    sale_order = relationship("SaleOrder")
    style_template = relationship("StyleTemplate")
    marker = relationship("Marker")


class CutReport(db.Model):
    __tablename__ = 'cut_report'
    __table_args__ = {'extend_existing': True}

    BundleCode=db.Column(String(64))
    BundleQuantity=db.Column(Integer)
    ScannedQuantity=db.Column(Integer)

    RemainingQuantity=db.Column(Integer)
    CutJobID=db.Column(Integer, db.ForeignKey("cut_job.CutJobID"))
    CreatedAt=db.Column(DateTime) 
    UpdatedAt=db.Column(DateTime)  
    CutNo=db.Column(Integer)
    ProductionOrderID=db.Column(Integer, db.ForeignKey("production_order.ProductionOrderID"))
    CutQuantity=db.Column(Integer)
    
    MarkerID=db.Column(Integer, db.ForeignKey("marker.MarkerID")) 
    ProductionOrderCode=db.Column(String(64))
    SaleOrderID=db.Column(Integer, db.ForeignKey("sale_order.SaleOrderID"))
    StyleTemplateID=db.Column(Integer, db.ForeignKey("style_template.StyleTemplateID"))
    IsFollowOperationSequence=db.Column(Boolean)
    SaleOrderCode=db.Column(String(100))
    
    Customer=db.Column(String(64))
    
    
    OrderQuantity=db.Column(Integer)    
    
    StyleTemplateCode=db.Column(String(64))   
    MarkerCode=db.Column(String(64))    
    MarkerMapping=db.Column(JSON)    

    cut_job = relationship("CutJob")
    production_order = relationship("ProductionOrder")
    sale_order = relationship("SaleOrder")
    style_template = relationship("StyleTemplate")
    marker = relationship("Marker")


class Operation(db.Model):
    __tablename__ = 'operation'
    __table_args__ = {'extend_existing': True}

    OperationID=db.Column(Integer, primary_key = True, autoincrement=False) 
    OperationCode=db.Column(String(64))    
    OperationName =db.Column(String(64))
    OperationDescription = db.Column(String(64))    
    Department = db.Column(String(64))
    PieceRate=db.Column(Integer)      

    OperationType=db.Column(String(64))
    OperationImageUrl=db.Column(String(2056))
    OperationThumbnailUrl=db.Column(String(2056))

    SectionID = db.Column(Integer, db.ForeignKey("section.SectionID"))
    CreatedAt=db.Column(DateTime) 
    UpdatedAt=db.Column(DateTime)  
    SectionCode=db.Column(String(64))
    SectionDescription=db.Column(String(64))    


    section = relationship("Section")


class Section(db.Model):
    __tablename__ = 'section'
    __table_args__ = {'extend_existing': True}

    SectionID=db.Column(Integer, primary_key = True, autoincrement=False) 
    SectionCode=db.Column(String(64))
    SectionDescription=db.Column(String(64))
    CreatedAt=db.Column(DateTime) 
    UpdatedAt=db.Column(DateTime) 


class PieceWiseCutReport(db.Model):
    __tablename__ = 'piece_wise_cut_report'
    __table_args__ = {'extend_existing': True}

    PieceID=db.Column(Integer, primary_key = True, autoincrement=False)
    BundleID=db.Column(Integer, db.ForeignKey("cut_report.BundleID"))
    PieceNumber=db.Column(Integer)
    CreatedAt=db.Column(DateTime) 
    UpdatedAt=db.Column(DateTime)  
    BundleCode=db.Column(String(64)) 
    BundleQuantity=db.Column(Integer)
    ScannedQuantity=db.Column(Integer)
    RemainingQuantity=db.Column(Integer)
    CutJobID=db.Column(Integer, db.ForeignKey("cut_job.CutJobID"))
    CutNo=db.Column(Integer) 
    ProductionOrderID=db.Column(Integer, db.ForeignKey("production_order.ProductionOrderID"))
    CutQuantity=db.Column(Integer)
    MarkerID=db.Column(Integer, db.ForeignKey("marker.MarkerID")) 
    ProductionOrderCode=db.Column(String(64))
    SaleOrderID=db.Column(Integer, db.ForeignKey("sale_order.SaleOrderID"))
    StyleTemplateID=db.Column(Integer, db.ForeignKey("style_template.StyleTemplateID"))
    IsFollowOperationSequence=db.Column(Boolean)
    SaleOrderCode=db.Column(String(100))
    Customer=db.Column(String(64))
    OrderQuantity=db.Column(Integer)    
    StyleTemplateCode=db.Column(String(64))   
    MarkerCode=db.Column(String(64))    
    MarkerMapping=db.Column(JSON)    

    production_order = relationship("ProductionOrder")
    sale_order = relationship("SaleOrder")
    style_template = relationship("StyleTemplate")
    marker = relationship("Marker")
    cut_report = relationship("CutReport")
    cut_job = relationship("CutJob")


class Scan(db.Model):
    __tablename__ = 'scan'
    __table_args__ = {'extend_existing': True}

    ScanID=db.Column(BIGINT, primary_key = True, autoincrement=False)
    ShortAddress=db.Column(String(64)) 
    LongAddress=db.Column(String(64)) 
    HostIP=db.Column(String(64)) 
    CreatedAt=db.Column(DateTime) 
    UpdatedAt=db.Column(DateTime)  
    LineID=db.Column(Integer,db.ForeignKey("line.LineID"))
    LineCode=db.Column(String(64))
    LineDescription=db.Column(String(64)) 
    WorkerID =db.Column(Integer, db.ForeignKey("worker.WorkerID"))
    WorkerCode=db.Column(String(64))
    WorkerDescription=db.Column(String(64))    
    WorkerImageUrl=db.Column(String(2056)) 
    WorkerThumbnailUrl=db.Column(String(2056)) 
    AllocatedMachines=db.Column(JSON)
    BundleID=db.Column(Integer, db.ForeignKey("cut_report.BundleID"))
    BundleCode=db.Column(String(64)) 
    BundleQuantity=db.Column(Integer)
    ScannedQuantity=db.Column(Integer)
    RemainingQuantity=db.Column(Integer)
    CutJobID=db.Column(Integer, db.ForeignKey("cut_job.CutJobID"))
    CutNo=db.Column(Integer) 
    ProductionOrderID=db.Column(Integer, db.ForeignKey("production_order.ProductionOrderID"))
    CutQuantity=db.Column(Integer)
    MarkerID=db.Column(Integer, db.ForeignKey("marker.MarkerID")) 
    ProductionOrderCode=db.Column(String(64))
    SaleOrderID=db.Column(Integer, db.ForeignKey("sale_order.SaleOrderID"))
    StyleTemplateID=db.Column(Integer, db.ForeignKey("style_template.StyleTemplateID"))
    IsFollowOperationSequence=db.Column(Boolean)
    SaleOrderCode=db.Column(String(100))
    Customer=db.Column(String(64))
    OrderQuantity=db.Column(Integer)    
    StyleTemplateCode=db.Column(String(64))   
    MarkerCode=db.Column(String(64))    
    MarkerMapping=db.Column(JSON)    
    MachineID=db.Column(Integer,db.ForeignKey("machine.MachineID"))
    MachineCode=db.Column(String(64))
    MachineDescription=db.Column(String(64))
    MachineImageUrl=db.Column(String(2056)) 
    MachineThumbnailUrl=db.Column(String(2056))
    MachineTypeID=db.Column(Integer)
    ActiveWorkerID=db.Column(Integer)
    Operations=db.Column(JSON)
    BoxID=db.Column(Integer)
    MachineTypeCode=db.Column(String(64)) 
    MachineTypeDescription=db.Column(String(64)) 
    Allowance=db.Column(Float)
    OperationID=db.Column(Integer,db.ForeignKey("operation.OperationID"))
    OperationCode=db.Column(String(64))
    OperationName=db.Column(String(64))
    OperationDescription=db.Column(String(64))
    Department=db.Column(String(64))
    PieceRate=db.Column(Integer)
    OperationType=db.Column(String(64))
    OperationImageUrl=db.Column(String(2056))
    OperationThumbnailUrl=db.Column(String(2056))
    SectionID=db.Column(Integer, db.ForeignKey("section.SectionID"))
    SectionCode=db.Column(String(64))
    SectionDescription=db.Column(String(64))
    PieceID=db.Column(Integer)
    PieceNumber=db.Column(Integer)
    WorkerScanID=db.Column(BIGINT, db.ForeignKey("worker_scan.WorkerScanID")) 
    WorkerOperations=db.Column(JSON)
    HasExpired=db.Column(Integer)
    EndedAt=db.Column(DateTime) 


    section = relationship("Section")
    operation = relationship("Operation")

    production_order = relationship("ProductionOrder")
    sale_order = relationship("SaleOrder")
    style_template = relationship("StyleTemplate")
    marker = relationship("Marker")
    cut_report = relationship("CutReport")
    cut_job = relationship("Cutjob")
    machine = relationship("Machine")
    line = relationship("Line")
    worker = relationship("Worker")    
    worker_scan = relationship("WorkerScan")  



class StyleTemplate(db.Model):
    __tablename__ = 'style_template'
    __table_args__ = {'extend_existing': True}

    StyleTemplateID=db.Column(Integer, primary_key = True, autoincrement=False) 
    StyleTemplateCode=db.Column(String(64))     
    CreatedAt=db.Column(DateTime) 
    UpdatedAt=db.Column(DateTime) 


# db.Model.metadata.create_all(engine_postgres)
class Marker(db.Model):
    __tablename__ = 'marker'
    __table_args__ = {'extend_existing': True}

    MarkerID=db.Column(Integer, primary_key = True, autoincrement=False) 
    MarkerCode=db.Column(String(64))    
    ProductionOrderID=db.Column(Integer, db.ForeignKey("production_order.ProductionOrderID"))
    MarkerMapping=db.Column(JSON)  
    CreatedAt=db.Column(DateTime) 
    UpdatedAt=db.Column(DateTime)  
    ProductionOrderCode=db.Column(String(64))
    
    SaleOrderID=db.Column(Integer, db.ForeignKey("sale_order.SaleOrderID"))
    StyleTemplateID=db.Column(Integer, db.ForeignKey("style_template.StyleTemplateID"))

    IsFollowOperationSequence=db.Column(Boolean)
    SaleOrderCode=db.Column(String(100))
    Customer=db.Column(String(64))
    OrderQuantity=db.Column(Integer)    
    
    StyleTemplateCode=db.Column(String(64))   
    
    # Size=db.Column(Integer) 
    # Inseam=db.Column(Integer) 
    # Ratio=db.Column(Integer) 


    production_order = relationship("ProductionOrder")
    sale_order = relationship("SaleOrder")
    style_template = relationship("StyleTemplate")


class CutJob(db.Model):
    __tablename__ = 'cut_job'
    __table_args__ = {'extend_existing': True}

    CutJobID=db.Column(Integer, primary_key = True, autoincrement=False) 
    CutNo=db.Column(Integer)
    ProductionOrderID=db.Column(Integer, db.ForeignKey("production_order.ProductionOrderID"))
    CutQuantity=db.Column(Integer)




    MarkerID=db.Column(Integer, db.ForeignKey("marker.MarkerID")) 
    CreatedAt=db.Column(DateTime) 
    UpdatedAt=db.Column(DateTime)  
    ProductionOrderCode=db.Column(String(64))
    SaleOrderID=db.Column(Integer, db.ForeignKey("sale_order.SaleOrderID"))
    StyleTemplateID=db.Column(Integer, db.ForeignKey("style_template.StyleTemplateID"))
    IsFollowOperationSequence=db.Column(Boolean)
    SaleOrderCode=db.Column(String(100))
    Customer=db.Column(String(64))


    
    OrderQuantity=db.Column(Integer)    
    
    StyleTemplateCode=db.Column(String(64))   
    MarkerCode=db.Column(String(64))    
    
    MarkerMapping=db.Column(JSON)    

    production_order = relationship("ProductionOrder")
    sale_order = relationship("SaleOrder")
    style_template = relationship("StyleTemplate")
    marker = relationship("Marker")


class CutReport(db.Model):
    __tablename__ = 'cut_report'
    __table_args__ = {'extend_existing': True}

    BundleID=db.Column(Integer, primary_key = True, autoincrement=False)
    
    BundleCode=db.Column(String(64))
    BundleQuantity=db.Column(Integer)
    ScannedQuantity=db.Column(Integer)

    RemainingQuantity=db.Column(Integer)
    CutJobID=db.Column(Integer, db.ForeignKey("cut_job.CutJobID"))
    CreatedAt=db.Column(DateTime) 
    UpdatedAt=db.Column(DateTime)  
    CutNo=db.Column(Integer)
    ProductionOrderID=db.Column(Integer, db.ForeignKey("production_order.ProductionOrderID"))
    CutQuantity=db.Column(Integer)
    
    MarkerID=db.Column(Integer, db.ForeignKey("marker.MarkerID")) 
    ProductionOrderCode=db.Column(String(64))
    SaleOrderID=db.Column(Integer, db.ForeignKey("sale_order.SaleOrderID"))
    StyleTemplateID=db.Column(Integer, db.ForeignKey("style_template.StyleTemplateID"))
    IsFollowOperationSequence=db.Column(Boolean)
    SaleOrderCode=db.Column(String(100))
    
    Customer=db.Column(String(64))
    
    
    OrderQuantity=db.Column(Integer)    
    
    StyleTemplateCode=db.Column(String(64))   
    MarkerCode=db.Column(String(64))    
    MarkerMapping=db.Column(JSON)    

    cut_job = relationship("CutJob")
    production_order = relationship("ProductionOrder")
    sale_order = relationship("SaleOrder")
    style_template = relationship("StyleTemplate")
    marker = relationship("Marker")


class Operation(db.Model):
    __tablename__ = 'operation'
    __table_args__ = {'extend_existing': True}

    OperationID=db.Column(Integer, primary_key = True, autoincrement=False) 
    OperationCode=db.Column(String(64))    
    OperationName =db.Column(String(64))
    OperationDescription = db.Column(String(64))    
    Department = db.Column(String(64))
    PieceRate=db.Column(Integer)      

    OperationType=db.Column(String(64))
    OperationImageUrl=db.Column(String(2056))
    OperationThumbnailUrl=db.Column(String(2056))

    SectionID = db.Column(Integer, db.ForeignKey("section.SectionID"))
    CreatedAt=db.Column(DateTime) 
    UpdatedAt=db.Column(DateTime)  
    SectionCode=db.Column(String(64))
    SectionDescription=db.Column(String(64))    


    section = relationship("Section")


class Section(db.Model):
    __tablename__ = 'section'
    __table_args__ = {'extend_existing': True}

    SectionID=db.Column(Integer, primary_key = True, autoincrement=False) 
    SectionCode=db.Column(String(64))
    SectionDescription=db.Column(String(64))
    CreatedAt=db.Column(DateTime) 
    UpdatedAt=db.Column(DateTime)  


class PieceWiseCutReport(db.Model):
    __tablename__ = 'piece_wise_cut_report'
    __table_args__ = {'extend_existing': True}

    PieceID=db.Column(Integer, primary_key = True, autoincrement=False)
    BundleID=db.Column(Integer, db.ForeignKey("cut_report.BundleID"))
    PieceNumber=db.Column(Integer)
    CreatedAt=db.Column(DateTime) 
    UpdatedAt=db.Column(DateTime)  
    BundleCode=db.Column(String(64)) 
    BundleQuantity=db.Column(Integer)
    ScannedQuantity=db.Column(Integer)
    RemainingQuantity=db.Column(Integer)
    CutJobID=db.Column(Integer, db.ForeignKey("cut_job.CutJobID"))
    CutNo=db.Column(Integer) 
    ProductionOrderID=db.Column(Integer, db.ForeignKey("production_order.ProductionOrderID"))
    CutQuantity=db.Column(Integer)
    MarkerID=db.Column(Integer, db.ForeignKey("marker.MarkerID")) 
    ProductionOrderCode=db.Column(String(64))
    SaleOrderID=db.Column(Integer, db.ForeignKey("sale_order.SaleOrderID"))
    StyleTemplateID=db.Column(Integer, db.ForeignKey("style_template.StyleTemplateID"))
    IsFollowOperationSequence=db.Column(Boolean)
    SaleOrderCode=db.Column(String(100))
    Customer=db.Column(String(64))
    OrderQuantity=db.Column(Integer)    
    StyleTemplateCode=db.Column(String(64))   
    MarkerCode=db.Column(String(64))    
    MarkerMapping=db.Column(JSON)    

    production_order = relationship("ProductionOrder")
    sale_order = relationship("SaleOrder")
    style_template = relationship("StyleTemplate")
    marker = relationship("Marker")
    cut_report = relationship("CutReport")
    cut_job = relationship("CutJob") 


class Scan(db.Model):
    __tablename__ = 'scan'
    __table_args__ = {'extend_existing': True}

    ScanID=db.Column(BIGINT, primary_key = True, autoincrement=False)
    ShortAddress=db.Column(String(64)) 
    LongAddress=db.Column(String(64)) 
    HostIP=db.Column(String(64)) 
    CreatedAt=db.Column(DateTime) 
    UpdatedAt=db.Column(DateTime)  
    LineID=db.Column(Integer,db.ForeignKey("line.LineID"))
    LineCode=db.Column(String(64))
    LineDescription=db.Column(String(64)) 
    WorkerID =db.Column(Integer, db.ForeignKey("worker.WorkerID"))
    WorkerCode=db.Column(String(64))
    WorkerDescription=db.Column(String(64))    
    WorkerImageUrl=db.Column(String(2056)) 
    WorkerThumbnailUrl=db.Column(String(2056)) 
    AllocatedMachines=db.Column(JSON)
    BundleID=db.Column(Integer, db.ForeignKey("cut_report.BundleID"))
    BundleCode=db.Column(String(64)) 
    BundleQuantity=db.Column(Integer)
    ScannedQuantity=db.Column(Integer)
    RemainingQuantity=db.Column(Integer)
    CutJobID=db.Column(Integer, db.ForeignKey("cut_job.CutJobID"))
    CutNo=db.Column(Integer) 
    ProductionOrderID=db.Column(Integer, db.ForeignKey("production_order.ProductionOrderID"))
    CutQuantity=db.Column(Integer)
    MarkerID=db.Column(Integer, db.ForeignKey("marker.MarkerID")) 
    ProductionOrderCode=db.Column(String(64))
    SaleOrderID=db.Column(Integer, db.ForeignKey("sale_order.SaleOrderID"))
    StyleTemplateID=db.Column(Integer, db.ForeignKey("style_template.StyleTemplateID"))
    IsFollowOperationSequence=db.Column(Boolean)
    SaleOrderCode=db.Column(String(100))
    Customer=db.Column(String(64))
    OrderQuantity=db.Column(Integer)    
    StyleTemplateCode=db.Column(String(64))   
    MarkerCode=db.Column(String(64))    
    MarkerMapping=db.Column(JSON)    
    MachineID=db.Column(Integer,db.ForeignKey("machine.MachineID"))
    MachineCode=db.Column(String(64))
    MachineDescription=db.Column(String(64))
    MachineImageUrl=db.Column(String(2056)) 
    MachineThumbnailUrl=db.Column(String(2056))
    MachineTypeID=db.Column(Integer)
    ActiveWorkerID=db.Column(Integer)
    Operations=db.Column(JSON)
    BoxID=db.Column(Integer)
    MachineTypeCode=db.Column(String(64)) 
    MachineTypeDescription=db.Column(String(64)) 
    Allowance=db.Column(Float)
    OperationID=db.Column(Integer,db.ForeignKey("operation.OperationID"))
    OperationCode=db.Column(String(64))
    OperationName=db.Column(String(64))
    OperationDescription=db.Column(String(64))
    Department=db.Column(String(64))
    PieceRate=db.Column(Integer)
    OperationType=db.Column(String(64))
    OperationImageUrl=db.Column(String(2056))
    OperationThumbnailUrl=db.Column(String(2056))
    SectionID=db.Column(Integer, db.ForeignKey("section.SectionID"))
    SectionCode=db.Column(String(64))
    SectionDescription=db.Column(String(64))
    PieceID=db.Column(Integer)
    PieceNumber=db.Column(Integer)
    WorkerScanID=db.Column(BIGINT, db.ForeignKey("worker_scan.WorkerScanID")) 
    WorkerOperations=db.Column(JSON)
    HasExpired=db.Column(Integer)
    EndedAt=db.Column(DateTime) 


    section = relationship("Section")
    operation = relationship("Operation")

    production_order = relationship("ProductionOrder")
    sale_order = relationship("SaleOrder")
    style_template = relationship("StyleTemplate")
    marker = relationship("Marker")
    cut_report = relationship("CutReport")
    cut_job = relationship("Cutjob")
    machine = relationship("Machine")
    line = relationship("Line")
    worker = relationship("Worker")    
    worker_scan = relationship("WorkerScan")        

class ScanGroup(db.Model):
    __tablename__ = 'scan_group'
    __table_args__ = {'extend_existing': True}

    GroupID=db.Column(Integer, primary_key = True, autoincrement=False) 
    CreatedAt=db.Column(DateTime) 
    UpdatedAt=db.Column(DateTime)  
class PieceWiseScan(db.Model):
    __tablename__ = 'piece_wise_scan'
    __table_args__ = {'extend_existing': True}

    PieceWiseScanningID=db.Column(Integer, primary_key = True, autoincrement=False)
    WorkerID =db.Column(Integer, db.ForeignKey("worker.WorkerID"))
    LineID=db.Column(Integer,db.ForeignKey("line.LineID"))
    MachineID=db.Column(Integer,db.ForeignKey("machine.MachineID"))
    CreatedAt=db.Column(DateTime) 
    UpdatedAt=db.Column(DateTime)  
    PieceID=db.Column(Integer, db.ForeignKey("piece_wise_cut_report.PieceID"))
    PieceNumber=db.Column(Integer)
    BundleCode=db.Column(String(64)) 
    BundleQuantity=db.Column(Integer)
    ScannedQuantity=db.Column(Integer)
    RemainingQuantity=db.Column(Integer)
    CutJobID=db.Column(Integer, db.ForeignKey("cut_job.CutJobID"))
    CutNo=db.Column(Integer)
    ProductionOrderID=db.Column(Integer, db.ForeignKey("production_order.ProductionOrderID"))
    CutQuantity=db.Column(Integer)
    MarkerID=db.Column(Integer, db.ForeignKey("marker.MarkerID")) 
    ProductionOrderCode=db.Column(String(64))
    SaleOrderID=db.Column(Integer, db.ForeignKey("sale_order.SaleOrderID"))
    StyleTemplateID=db.Column(Integer, db.ForeignKey("style_template.StyleTemplateID"))
    IsFollowOperationSequence=db.Column(Boolean)
    SaleOrderCode=db.Column(String(100))
    Customer=db.Column(String(64))
    OrderQuantity=db.Column(Integer)    
    StyleTemplateCode=db.Column(String(64))   
    MarkerCode=db.Column(String(64))    
    MarkerMapping=db.Column(JSON)    
    OperationID=db.Column(Integer, db.ForeignKey("operation.OperationID")) 
    OperationCode=db.Column(String(64))    
    OperationName =db.Column(String(64))
    OperationDescription = db.Column(String(64))      
    Department = db.Column(String(64))
    PieceRate=db.Column(Integer)      
    OperationType=db.Column(String(64))
    OperationImageUrl=db.Column(String(2056))
    OperationThumbnailUrl=db.Column(String(2056))
    SectionID = db.Column(Integer, db.ForeignKey("section.SectionID"))
    SectionCode=db.Column(String(64))
    SectionDescription=db.Column(String(64))    
    ScanID=db.Column(BIGINT, db.ForeignKey("scan.ScanID"))

    ShortAddress=db.Column(String(64)) 
    LongAddress=db.Column(String(64)) 
    HostIP=db.Column(String(64)) 
    LineCode=db.Column(String(64))
    LineDescription=db.Column(String(64)) 
    WorkerCode=db.Column(String(64))
    WorkerDescription=db.Column(String(64)) 
    WorkerImageUrl=db.Column(String(2056)) 
    WorkerThumbnailUrl=db.Column(String(2056)) 
    AllocatedMachines=db.Column(JSON)
    MachineCode=db.Column(String(64))
    MachineDescription=db.Column(String(64))
    MachineImageUrl=db.Column(String(2056)) 
    MachineThumbnailUrl=db.Column(String(2056))
    MachineTypeID=db.Column(Integer)
    ActiveWorkerID=db.Column(Integer)
    Operations=db.Column(JSON)
    BoxID=db.Column(Integer)
    MachineTypeCode=db.Column(String(64)) 
    MachineTypeDescription=db.Column(String(64)) 
    Allowance=db.Column(Float)
    WorkerScanID=db.Column(BIGINT, db.ForeignKey("worker_scan.WorkerScanID")) 
    WorkerOperations=db.Column(JSON)
    HasExpired=db.Column(Integer)
    EndedAt=db.Column(DateTime) 
    BundleID=db.Column(Integer, db.ForeignKey("cut_report.BundleID"))


    production_order = relationship("ProductionOrder")
    sale_order = relationship("SaleOrder")
    style_template = relationship("StyleTemplate")
    marker = relationship("Marker")
    cut_report = relationship("CutReport")
    cut_job = relationship("Cutjob")
    machine = relationship("Machine")
    line = relationship("Line")
    worker = relationship("Worker")    
    worker_scan = relationship("WorkerScan")
    scan = relationship("Scan") 
    piece_wise_cut_report = relationship("PieceWiseCutReport")     
    operation = relationship("Operation")            
    section = relationship("Section")  


class Module(db.Model):
    __tablename__ = 'module'
    __table_args__ = {'extend_existing': True}

    ModuleID=db.Column(Integer, primary_key = True, autoincrement=False) 
    ModuleCode=db.Column(String(64))
    CreatedAt=db.Column(DateTime) 
    UpdatedAt=db.Column(DateTime) 


class StyleBulletin(db.Model):
    __tablename__ = 'style_bulletin'
    __table_args__ = {'extend_existing': True}

    StyleBulletinID=db.Column(Integer, primary_key = True, autoincrement=False) 
   
    StyleTemplateID=db.Column(Integer,db.ForeignKey("style_template.StyleTemplateID"))
    OperationID=db.Column(Integer, db.ForeignKey("operation.OperationID")) 
    OperationSequence=db.Column(Integer)    
   
    ScanType=db.Column(String(10))
    IsFirst=db.Column(Boolean)
    IsLast=db.Column(Boolean)

    MachineTypeID=db.Column(Integer, db.ForeignKey("machine_type.MachineTypeID"))
    CreatedAt=db.Column(DateTime) 
    UpdatedAt=db.Column(DateTime)  
   
    StyleTemplateCode=db.Column(String(64))

    OperationCode=db.Column(String(64))    
    OperationName =db.Column(String(64))
    OperationDescription = db.Column(String(64))    
    Department = db.Column(String(64))
    PieceRate=db.Column(Float)      
    OperationType=db.Column(String(64))
    OperationImageUrl=db.Column(String(2056))
    OperationThumbnailUrl=db.Column(String(2056))
    SectionID = db.Column(Integer, db.ForeignKey("section.SectionID"))
    SectionCode=db.Column(String(64))
    SectionDescription=db.Column(String(64))    

    MachineTypeCode=db.Column(String(64))
    MachineTypeDescription=db.Column(String(64))
    Allowance=db.Column(Float)


    style_template = relationship("StyleTemplate")
    operation = relationship("Operation")
    section = relationship("Section")
    machine_type = relationship("MachineType")


class Tag(db.Model):
    __tablename__ = 'tag'
    __table_args__ = {'extend_existing': True}

    TagID=db.Column(Integer, primary_key = True, autoincrement=False) 
    
    BundleID=db.Column(Integer, db.ForeignKey("cut_report.BundleID"))
    CreatedAt=db.Column(DateTime) 
    UpdatedAt=db.Column(DateTime)  
    #db.Column ADDED LATER
    PieceID=db.Column(Integer)
    GroupID=db.Column(Integer)
    
    BundleCode=db.Column(String(64))

    BundleQuantity=db.Column(Integer)
    ScannedQuantity=db.Column(Integer)
    RemainingQuantity=db.Column(Integer)
    CutJobID=db.Column(Integer, db.ForeignKey("cut_job.CutJobID"))
    CutNo=db.Column(Integer) 
    ProductionOrderID=db.Column(Integer, db.ForeignKey("production_order.ProductionOrderID"))
    CutQuantity=db.Column(Integer)



    MarkerID=db.Column(Integer, db.ForeignKey("marker.MarkerID")) 
    ProductionOrderCode=db.Column(String(64))
    SaleOrderID=db.Column(Integer, db.ForeignKey("sale_order.SaleOrderID"))
    StyleTemplateID=db.Column(Integer, db.ForeignKey("style_template.StyleTemplateID"))
    IsFollowOperationSequence=db.Column(Boolean)
    SaleOrderCode=db.Column(String(100))

    Customer=db.Column(String(64))

    OrderQuantity=db.Column(Integer)    
    StyleTemplateCode=db.Column(String(64))   
    MarkerCode=db.Column(String(64))    
    
    
    
    MarkerMapping=db.Column(JSON) 


    cut_report = relationship("CutReport")
    cut_job = relationship("CutJob")
    marker = relationship("Marker")
    production_order = relationship("ProdcutionOrder")
    sale_order = relationship("SaleOrder")
    style_template = relationship("StyleTemplate")


class User(db.Model):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}

    UserID=db.Column(Integer, primary_key = True, autoincrement=False) 
    UserName=db.Column(String(64))
    Password=db.Column(String(1024))    
    UserType=db.Column(String(64))

    LineID=db.Column(Integer,db.ForeignKey("line.LineID"))
    SectionID=db.Column(Integer,db.ForeignKey("section.SectionID")) 
    CreatedAt=db.Column(DateTime) 
    UpdatedAt=db.Column(DateTime)  


    LineCode=db.Column(String(64))
    LineDescription=db.Column(String(64))

    SectionCode=db.Column(String(64))
    SectionDescription=db.Column(String(64))


    line = relationship("Line")
    section = relationship("Section")


class UserPermission(db.Model):
    __tablename__ = 'userpermission'
    __table_args__ = {'extend_existing': True}

    UserPermissionID=db.Column(Integer, primary_key = True, autoincrement=False) 
    CreatedAt=db.Column(DateTime) 
    UpdatedAt=db.Column(DateTime)  

    ModuleID=db.Column(Integer, db.ForeignKey("module.ModuleID"))    
    ModuleCode=db.Column(String(64))
    UserID=db.Column(Integer,db.ForeignKey("user.UserID")) 
    

    UserName=db.Column(String(64))
    Password=db.Column(String(1024))    
    UserType=db.Column(String(64))
    LineID=db.Column(Integer,db.ForeignKey("line.LineID"))
    SectionID=db.Column(Integer,db.ForeignKey("section.SectionID")) 
    LineCode=db.Column(String(64))
    LineDescription=db.Column(String(64))
    SectionCode=db.Column(String(64))
    SectionDescription=db.Column(String(64))


    user = relationship("User")
    module = relationship("Module")
    line = relationship("Line")
    section = relationship("Section") 

class Box(db.Model):
    __tablename__ = 'box'
    __table_args__ = {'extend_existing': True}

    BoxID=db.Column(Integer, primary_key = True, autoincrement=False) 
    BoxCode=db.Column(String(64)) 

    IssueDate=db.Column(DateTime)
    CreatedAt=db.Column(DateTime) 
    UpdatedAt=db.Column(DateTime)

class PieceWiseGroup(db.Model):
    __tablename__ = 'piece_wise_group'
    __table_args__ = {'extend_existing': True}

    PieceWiseGroupID=db.Column(Integer, primary_key = True, autoincrement=False) 
    BundleID=db.Column(Integer)
    CreatedAt=db.Column(DateTime) 
    UpdatedAt=db.Column(DateTime)

    GroupName=db.Column(String(1024))    
    GroupID=db.Column(Integer,db.ForeignKey("scan_group.GroupID"))
    PieceID=db.Column(Integer,db.ForeignKey("piece_wise_cut_report.PieceID"))

    PieceNumber=db.Column(Integer) 
    BundleCode=db.Column(String(64))
    BundleQuantity=db.Column(Integer)

    ScannedQuantity=db.Column(Integer)
    RemainingQuantity=db.Column(Integer)
    CutJobID=db.Column(Integer)
        
    CutNo=db.Column(Integer)
    ProductionOrderID=db.Column(Integer)
    CutQuantity=db.Column(Integer)
    
    MarkerID=db.Column(Integer)
    ProductionOrderCode=db.Column(String(64))
    SaleOrderID=db.Column(Integer)

    StyleTemplateID=db.Column(Integer)


    IsFollowOperationSequence=db.Column(Boolean)
    SaleOrderCode=db.Column(String(64))
    Customer=db.Column(String(64))        

    OrderQuantity=db.Column(Integer)
    StyleTemplateCode=db.Column(String(64))        

    MarkerCode=db.Column(String(64))
    MarkerMapping=db.Column(JSON)        


    piece_wise_cut_report = relationship("PieceWiseCutReport")
    scan_group = relationship("ScanGroup")

class MachineDownTime(db.Model):
    __tablename__ = 'machine_down_time'
    __table_args__ = {'extend_existing': True}

    MachineDownTimeID=db.Column(Integer, primary_key = True, autoincrement=False) 
    DownReason=db.Column(String(64))
    StartTime=db.Column(DateTime) 
    EndTime=db.Column(DateTime)

    CreatedAt=db.Column(DateTime)    
    UpdatedAt=db.Column(DateTime)
    MachineID=db.Column(Integer,db.ForeignKey("machine.MachineID"))

    MachineCode=db.Column(String(64)) 
    MachineDescription=db.Column(String(64))
    MachineImageUrl=db.Column(String(64))

    MachineThumbnailUrl=db.Column(String(64))
    MachineTypeID=db.Column(Integer)
    ActiveWorkerID=db.Column(Integer)
    LineID=db.Column(Integer)
    Operations=db.Column(JSON)
    BoxID=db.Column(Integer)
    IsMachineDown=db.Column(Boolean)
    
    LineCode=db.Column(String(64))


    LineDescription=db.Column(String(64))
    WorkerID=db.Column(Integer)

    WorkerCode=db.Column(String(64))      

    WorkerDescription=db.Column(String(64))
    WorkerImageUrl=db.Column(String(64))

    WorkerThumbnailUrl=db.Column(String(64))      

    AllocatedMachines=db.Column(Boolean)
    MachineTypeCode=db.Column(String(64))

    MachineTypeDescription=db.Column(String(64))      
    Allowance=db.Column(Float)

    machine = relationship("Machine")

class LineLayout(Base):
    __tablename__ = 'line_layout'
    __table_args__ = {'extend_existing': True}

    LineLayoutID=db.Column(Integer, primary_key = True, autoincrement=False) 
    RevisionNo=db.Column(Integer)
    LineLayoutDate=db.Column(DateTime) 
    LineLayoutStatus=db.Column(String(64))

    LineLayoutOperationMachines=db.Column(JSON)   

    IsAnyMachines=db.Column(Boolean)
    ParentLineLayoutID=db.Column(Integer)

    CreatedAt=db.Column(DateTime) 
    UpdatedAt=db.Column(DateTime)
    LineID=db.Column(Integer,db.ForeignKey("line.LineID"))

    LineCode=db.Column(String(64))
    LineDescription=db.Column(String(64))
    ProductionOrderID=db.Column(Integer,db.ForeignKey("production_order.ProductionOrderID"))
        
    ProductionOrderCode=db.Column(String(64))
    SaleOrderID=db.Column(Integer)
    StyleTemplateID=db.Column(Integer)
    
    IsFollowOperationSequence=db.Column(Boolean)
    SaleOrderCode=db.Column(String(64))
    Customer=db.Column(String(64))

    OrderQuantity=db.Column(Integer)


    StyleTemplateCode=db.Column(String(64))
     


    line = relationship("Line")
    production_order = relationship("ProductionOrder")