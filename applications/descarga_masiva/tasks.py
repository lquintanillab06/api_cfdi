from datetime import datetime,date
from apscheduler.schedulers.background import BackgroundScheduler





def start():
    scheduler = BackgroundScheduler()
    #scheduler.add_job(myTask, 'interval', seconds=15)
    scheduler.add_job(SolicitudDescargaTask, 'cron', day_of_week='mon-sun', hour="1", minute="5")
    scheduler.add_job(ConsultarSolitudDescargaTask, 'cron', day_of_week='mon-sun', hour='1-4', minute='*/20')
    scheduler.add_job(CargarXMLSolicitudTask, 'cron', day_of_week='mon-sun', hour='4-8', minute='*/30')
    scheduler.start()

def SolicitudDescargaTask():
    from .services.service import descarga_auto
    descarga_auto()
    
def ConsultarSolitudDescargaTask():
    from .services.service import consultar_solicitud_auto
    consultar_solicitud_auto()
   

def CargarXMLSolicitudTask():
    from .services.service import cargar_xmls_auto
    cargar_xmls_auto()