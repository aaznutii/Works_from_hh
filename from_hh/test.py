import pandas as pd
import os
import re


name_vac = ''.join(re.findall(r'[^\d_.json]',
                              os.path.basename(r'C:\Users\aaznu\Works_from_hh\from_hh\docs\pagination\0_Менеджер hh.json')))

print(name_vac)