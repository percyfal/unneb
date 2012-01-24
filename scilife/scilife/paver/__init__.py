"""
scilife utilities
"""
from paver.easy import *
from ngs.paver import *
import yaml

@task
@cmdopts([('fcid=', 'f', 'flowcell'), ('run_info=', 'r', 'run_info file'), ('project_info=', 'p', 'project_info file'),
          ('lanes=', 'l', 'lanes'), ('barcode_ids=', 'b', 'barcodes'), ('project_desc', 'd', 'project description')])

def get_project_files():
    """Get project files to work with"""
    options.order('get_project_files')
    run_info_file = options.get('run_info', 'run_info.yaml')
    project_info_file = options.get('project_info', 'post_process.yaml')
    flowcell = options.get('fcid', None)
    lanes = options.get('lanes', None)
    barcode_ids = options.get('barcode_ids', None)
    project_desc = options.get('project_desc', None)

    # Read run info
    with open(run_info_file) as fp:
        run_info = yaml.load(fp)
    # Read config
    with open(project_info_file) as fp:
        config = yaml.load(fp)

    # Traverse info file
    for lane in run_info:
        if not project_desc is None:
            if not lane.get("description").find(project_desc):
                continue
        elif not lanes is None:
            if not lane['lane'] in lanes.split(","):
                continue
        
        print lane
        
