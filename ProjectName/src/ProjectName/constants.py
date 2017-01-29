import os.path

MODULE_ROOT = os.path.dirname(__import__('<% project_name %>').__file__)
DATA_ROOT = os.path.join(MODULE_ROOT, 'data')
