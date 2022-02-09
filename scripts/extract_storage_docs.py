#
# extract_storage_docs.py
#
# Extracts the "storage resources" section from selected .md files
# and writes them to standalone .md files.
#

#%% Imports

import os
import re


#%% Constants

# import os; os.chdir('c:/git/AIforEarthDataSets/')

input_dir = 'data'
output_dir = 'storage-docs'
datasets = ['naip','aster','landsat-8','sentinel-2','mobi','hgb','hrea','mtbs','nasadem',
            'io-lulc','deltares-floods','goes-r','noaa-cdr','gbif','forest-inventory-and-analysis','terraclimate',
            'alos-dem','copernicus-dem']

# Capture the entire "storage resources" section, up to the next ## heading
start_token = '## Storage resources'
end_token = '[^#]## '

pat = '{}(?P<storage>.*?){}'.format(start_token,end_token)
re_storage = re.compile(pat, re.DOTALL)
    
custom_encodings = {'gbif':'utf-8'}


#%% The doing of the doing

for dataset_name in datasets:

    encoding = None
    if dataset_name in custom_encodings:
        encoding = custom_encodings[dataset_name]
        
    input_fn = os.path.join(input_dir,dataset_name + '.md')
    output_fn = os.path.join(output_dir,dataset_name + '-storage.md')
    assert os.path.isfile(input_fn)
    
    with open(input_fn,'r',encoding=encoding) as f:
        content = f.read()
    
    m = re_storage.search(content)
    storage_content = m.group('storage').strip()
    
    with open(output_fn,'w',encoding=encoding) as f:
        f.write(storage_content)        
    
# ...for each data set    