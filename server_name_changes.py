import pandas as pd

# Your original list or dataframe of server names
server_names = ['prod-db-01', 'qa-api-02', 'uat-frontend-03']
df = pd.DataFrame({'server_name': server_names})

# Generate aliases like srv001, srv002...
alias_mapping = {name: f"srv{str(i+1).zfill(3)}" for i, name in enumerate(df['server_name'])}
reverse_alias_mapping = {v: k for k, v in alias_mapping.items()}



import re

def alias_server_names(text: str, mapping: dict) -> str:
    for real_name, alias in mapping.items():
        pattern = re.escape(real_name)
        text = re.sub(rf'\b{pattern}\b', alias, text)
    return text
