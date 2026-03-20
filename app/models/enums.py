from enum import Enum

class sourceEnum(str,Enum):
    clinic_emr="clinic_emr"
    hospital_discharge="hospital_discharge"
    patient_reported="patient_reported"
    