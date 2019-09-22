import json

def write(file_path, key1, key2, value):
    '''
    desc:
     update value pada json file
     
    input:
     - file_path = lokasi file
     - key1, key2 = key pada json
     - value = value yg akan di update
     
    output:
     - {'status': 'ok', 'value': f'{value} added in {key1} {key2}'}
    '''
    with open(file_path, 'r+') as f:
       data = json.load(f)
       data[key1][key2] = value
       f.seek(0)
       json.dump(data, f, indent=2, sort_keys=True)
       f.truncate()
       f.close()
  
    return {'status': 'ok', 'value': f'{value} added in {key1} {key2}'}
    


def read(file_path, key1, key2):
    '''
    desc:
     membaca value pada json file
     
    input:
     - file_path = lokasi file
     - key1, key2 = key pada json
     
    output:
     - {'status': 'ok', 'value': value yg ingin di baca}
    '''
    with open(file_path, 'r') as f:
        data = json.load(f)
        value = data[key1][key2]
        f.close()
  
    return value
    
