"""
Train and save a pipeline using a reduced set of features.
This script uses these features:
- Numeric: Age, Height, Weight, FCVC (vegetable freq), FAF (physical activity)
- Ordinal: CAEC (eating between meals)
- Nominal: MTRANS (transport), FAVC (eats high-calorie foods)
"""
import os
import pandas as pd
from obesity_pipeline import ObesityPipeline

base = os.path.dirname(__file__)
csv_path = os.path.join(base, 'Obesity.csv')
if not os.path.exists(csv_path):
    raise FileNotFoundError(f"CSV file not found at {csv_path}")

df = pd.read_csv(csv_path)

# Reduced feature set (updated per request)
# Ordinal: CAEC (eating between meals), CALC (alcohol consumption)
# Nominal: FAVC (high-calorie foods), SCC (monitors calories)
# Numeric: Age, Height, Weight, FCVC (vegetable freq), FAF (physical activity), CH2O (water), TUE (tech use)
col_ordinais = ['CAEC', 'CALC']
order_ordinais = {
    'CAEC': ['no', 'Sometimes', 'Frequently', 'Always'],
    'CALC': ['no', 'Sometimes', 'Frequently', 'Always']
}
col_nominais = ['FAVC', 'SCC', 'MTRANS', 'family_history']
col_numericas = ['Age', 'Height', 'Weight', 'FCVC', 'FAF', 'CH2O', 'TUE']

pipeline = ObesityPipeline(col_ordinais, order_ordinais, col_nominais, col_numericas)
X_test, y_test = pipeline.treinar(df)

# Save with a distinct name
pipeline.salvar('pipeline_subset.pkl')
pipeline.salvar_pickle('pipeline_subset_pickle.pkl')
print('Saved pipeline_subset.pkl and pipeline_subset_pickle.pkl')
