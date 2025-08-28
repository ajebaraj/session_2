import os
MONGO_SERVER_HOST = os.getenv('MONGO_SERVER_HOST', "164.52.207.106")

#Settings for MongoDB

IS_MONGO_AUTH_ENABLED =  os.getenv('IS_MONGO_AUTH_ENABLED', 'yes')

MONGO_SERVER_PORT = int(os.getenv('MONGO_SERVER_PORT', 30272))

MONGO_DB = os.getenv('MONGO_DB', "livis_v2_qa")  

MONGO_USERNAME = os.getenv('MONGO_USERNAME', "livis_qa_admin")

MONGO_PASS = os.getenv('MONGO_PASS', "litv46ikd8ks@sd6dakbb")

INSPECTION_DATA_COLLECTION = "inspection_summary"
MONGO_COLLECTION_PARTS = "parts"
MONGO_COLLECTIONS = {MONGO_COLLECTION_PARTS: "parts"}
WORKSTATION_COLLECTION = 'workstations'
PARTS_COLLECTION = 'parts'
SHIFT_COLLECTION = 'shift'
TRAINING_MANAGER = 'lincodetraining_manager'
USECASE_COLLECTION = 'usecase'
GLOBAL_MODEL_URL = 'model_data_drive/'
LOCAL_DATA_DRIVE  = "/home/server3/livis_training/bucket"
HTTP_BASE_URL = os.getenv('HTTP_BASE_URL', "https://livis.ai:8443/")  



# #Settings for Redis
REDIS_CLIENT_HOST = os.getenv('REDIS_CLIENT_HOST', "localhost")
REDIS_CLIENT_PORT = int(os.getenv('REDIS_CLIENT_PORT', 6379))
DATA_STORAGE = "/yolo/model_save/"
BEST_WEIGHTS= "/best.pt"

# DATA_STORAGE = "/home/lincode-product/livis_training/modelsave"
# BEST_WEIGHTS= f"{DATA_STORAGE}/best.pt"