import json
import os
import shutil


"""{'儿科': 409, '传染病': 286, '损伤;中毒’：254、‘神经系统疾病’：196、‘妇产科’：191、‘特殊科目’：182、‘皮肤病’：152、‘心血管疾病’：143、‘血液学和肿瘤学’：143、‘胃肠道疾病’：142、‘肌肉骨骼和结缔组织疾病’：131、‘泌尿生殖系统疾病’：130、‘肺部疾病’：125、‘内分泌和代谢疾病’：105、‘眼部疾病’：96、‘耳鼻喉疾病’：96、‘精神疾病’：94， ‘肝脏和胆道疾病’：70，‘重症监护医学’：64，‘营养障碍’：62，‘牙科疾病’：53，‘老年病学’：53，‘免疫学；过敏性疾病’：48，‘临床药理学’：27}"""


n2n={'Pediatrics': 409, 'Infectious Diseases': 286, 'Injuries; Poisoning': 254, 'Neurologic Disorders': 196, 'Gynecology and Obstetrics': 191, 'Special Subjects': 182, 'Dermatologic Disorders': 152, 'Cardiovascular Disorders': 143, 'Hematology and Oncology': 143, 'Gastrointestinal Disorders': 142, 'Musculoskeletal and Connective Tissue Disorders': 131, 'Genitourinary Disorders': 130, 'Pulmonary Disorders': 125, 'Endocrine and Metabolic Disorders': 105, 'Eye Disorders': 96, 'Ear, Nose, and Throat Disorders': 96, 'Psychiatric Disorders': 94, 'Hepatic and Biliary Disorders': 70, 'Critical Care Medicine': 64, 'Nutritional Disorders': 62, 'Dental Disorders': 53, 'Geriatrics': 53, 'Immunology; Allergic Disorders': 48, 'Clinical Pharmacology': 27}


SectionName=["Hematology and Oncology","Gastrointestinal Disorders","Pulmonary Disorders","Hepatic and Biliary Disorders"]


data:list=json.load(open('./MSD/Json/allchapterstopics.json','r',encoding='utf-8-sig'))
for value in n2n.values():
    os.makedirs(f'./MSD{value}',exist_ok=True)
for d in data:
    shutil.copy('./MSD/'+d['Id']+'.html','./MSD2/'+d['Id']+'.html')
    