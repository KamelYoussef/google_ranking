from utils import *
import yaml
from datetime import datetime

with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)


results = get_insurance_brokers_by_city(config['cities'], config['keywords'])
print(results)
ranks = find_target_rank_by_city_and_keyword(results, config['target_keywords'])
print(ranks)
export_to_excel(ranks, filename=f"broker_ranks_{datetime.now().strftime('%Y%m%d')}.xlsx")