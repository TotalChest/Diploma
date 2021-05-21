import argparse
import logging
import re
import json
from pathlib import Path


logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description='Extract statistics from result directories')
parser.add_argument('result_dirs', type=Path, nargs='+', help='List of result directories.')
parser.add_argument('-o', dest='output', required=True, type=Path, help='Output file with statistics.')
options = parser.parse_args()

statistics = {}
for result_dir in options.result_dirs:
    if not (result_dir / 'utg.js').exists():
        logger.warning(f'File utg.js is not exists in {result_dir}.')

    with open(result_dir / 'utg.js') as f:
        raw_contents = f.read()
    
    contents_start = re.search(r'\{|\[', raw_contents)
    index = contents_start.start() if contents_start is not None else 0
    result_json = json.loads(raw_contents[index:])
    
    statistics[str(result_dir)] = {
        'activities': result_json['num_reached_activities'],
        'effective_events': result_json['num_effective_events'],
        'events': result_json['num_input_events'],
        'exploration_perf': result_json['exploration_perf'],
        'states': result_json['num_nodes'],
        'total_activities': result_json['app_num_total_activities'],
        'crashes': result_json['num_unique_crashes'],
        'anrs': result_json['num_unique_anrs']
    }

with open(options.output, 'w') as f:
    json.dump(statistics, f)