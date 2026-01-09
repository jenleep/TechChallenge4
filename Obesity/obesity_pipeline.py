import os
import pickle
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OrdinalEncoder, OneHotEncoder, MinMaxScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib

class ObesityPipeline:
    """Lightweight wrapper around an sklearn Pipeline for the obesity dataset.

    Parameters
    - col_ordinais: list of ordinal column names
    - ordem_ordinais: dict mapping ordinal column -> ordered categories list
    - col_nominais: list of nominal column names
    - col_numericas: list of numeric column names
    - target: name of the target column in the dataframe (default: 'Obesity')
    """

    def __init__(self, col_ordinais, ordem_ordinais, col_nominais, col_numericas, target='Obesity'):
        self.col_ordinais = list(col_ordinais) if col_ordinais is not None else []
        # create categories list for OrdinalEncoder in same order as col_ordinais
        self.ordem_ordinais = [ordem_ordinais.get(col) for col in self.col_ordinais] if ordem_ordinais else []
        self.col_nominais = list(col_nominais) if col_nominais is not None else []
        self.col_numericas = list(col_numericas) if col_numericas is not None else []
        self.target = target
        self.pipeline = None
        self.model = None
        # defaults collected during training (col -> default value)
        self.defaults = {}
        # expected input columns order for prediction
        self.expected_columns = self.col_ordinais + self.col_nominais + self.col_numericas

    def construir_pipeline(self):
        transformers = []
        if self.col_ordinais:
            # Allow unknown ordinal categories during transform by using a special encoded value
            transformers.append(('ordinais', OrdinalEncoder(categories=self.ordem_ordinais,
                                                            handle_unknown='use_encoded_value',
                                                            unknown_value=-1), self.col_ordinais))
        if self.col_nominais:
            # Ignore unknown categories at transform time
            transformers.append(('nominais', OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore'), self.col_nominais))
        if self.col_numericas:
            transformers.append(('numericas', MinMaxScaler(), self.col_numericas))

        preprocessor = ColumnTransformer(transformers=transformers, remainder='drop')

        self.pipeline = Pipeline(steps=[
            ('preprocessamento', preprocessor),
            ('classificador', RandomForestClassifier(random_state=4242, test_size=0.3, class_weight='balanced'))
        ])

    def treinar(self, df, test_size=0.3, random_state=4242, class_weight='balanced'):
        self.construir_pipeline()
        # Prepare feature matrix and target
        X = df.drop(columns=self.target)
        y = df[self.target]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
        self.pipeline.fit(X_train, y_train)
        # compute sensible defaults from training set to allow partial inputs at predict time
        defaults = {}
        for col in self.col_numericas:
            if col in X_train.columns:
                defaults[col] = float(X_train[col].median())
        for col in self.col_ordinais + self.col_nominais:
            if col in X_train.columns:
                modes = X_train[col].mode()
                if not modes.empty:
                    defaults[col] = modes.iloc[0]
                else:
                    # fallback: first known category from ordem_ordinais if available
                    if col in (self.col_ordinais or []):
                        idx = self.col_ordinais.index(col)
                        cats = self.ordem_ordinais[idx] if idx < len(self.ordem_ordinais) else None
                        defaults[col] = cats[0] if cats else None
                    else:
                        defaults[col] = None
        self.defaults = defaults
        # record expected columns order for building input rows later
        self.expected_columns = [c for c in (self.col_ordinais + self.col_nominais + self.col_numericas) if c in X_train.columns]
        y_pred = self.pipeline.predict(X_test)
        print(f"Acurácia: {accuracy_score(y_test, y_pred):.4f}")
        print("\nRelatório de Classificação:")
        print(classification_report(y_test, y_pred, zero_division=0))
        return X_test, y_test

    def prever(self, df_novo):
        if self.pipeline is None:
            raise RuntimeError('Pipeline not fitted or loaded.')
        # Accept dict/Series/DataFrame inputs. Build a DataFrame with expected columns and fill missing with defaults.
        if isinstance(df_novo, dict):
            df_tmp = pd.DataFrame([df_novo])
        elif isinstance(df_novo, pd.Series):
            df_tmp = pd.DataFrame([df_novo.to_dict()])
        elif isinstance(df_novo, pd.DataFrame):
            df_tmp = df_novo.copy()
        else:
            raise TypeError('df_novo must be a dict, pandas.Series or pandas.DataFrame')

        # Ensure all expected columns exist and fill missing with defaults
        for col in self.expected_columns:
            if col not in df_tmp.columns:
                df_tmp[col] = self.defaults.get(col, None)

        # Keep only expected columns in the proper order
        df_tmp = df_tmp[self.expected_columns]

        return self.pipeline.predict(df_tmp)

    def salvar(self, caminho='pipeline_obesidade.pkl'):
        # Save pipeline together with defaults and expected columns
        payload = {
            'pipeline': self.pipeline,
            'defaults': self.defaults,
            'expected_columns': self.expected_columns,
        }
        joblib.dump(payload, caminho)

    def salvar_pickle(self, caminho='pipeline_obesidade_pickle.pkl'):
        """Save pipeline using the pickle module (alternative to joblib)."""
        payload = {
            'pipeline': self.pipeline,
            'defaults': self.defaults,
            'expected_columns': self.expected_columns,
        }
        with open(caminho, 'wb') as f:
            pickle.dump(payload, f, protocol=pickle.HIGHEST_PROTOCOL)

    def carregar(self, caminho='pipeline_obesidade.pkl'):
        # Apply compatibility shim for sklearn internal symbols before loading
        try:
            from compat import ensure_sklearn_remainder
            try:
                ensure_sklearn_remainder()
            except Exception:
                pass
        except Exception:
            pass

        payload = joblib.load(caminho)
        # Support both legacy files that only contain the pipeline and our payload dict
        if isinstance(payload, dict) and 'pipeline' in payload:
            self.pipeline = payload.get('pipeline')
            self.defaults = payload.get('defaults', {})
            self.expected_columns = payload.get('expected_columns', self.expected_columns)
        else:
            # older files: payload is the pipeline object
            self.pipeline = payload


if __name__ == "__main__":
    # Train a default pipeline using the local CSV file (columns must match dataset)
    base = os.path.dirname(__file__)
    csv_path = os.path.join(base, 'Obesity.csv')
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found at {csv_path}")

    df = pd.read_csv(csv_path)

    # Default column names aligned with the provided dataset
    col_ordinais = ['CAEC', 'CALC']
    ordem_ordinais = {
        'CAEC': ['no', 'Sometimes', 'Frequently', 'Always'],
        'CALC': ['no', 'Sometimes', 'Frequently', 'Always']
    }
    col_nominais = ['FAVC', 'SCC', 'MTRANS', 'family_history']
    col_numericas = ['Age', 'Height', 'Weight', 'FCVC', 'FAF', 'CH2O', 'TUE']

    pipeline = ObesityPipeline(col_ordinais, ordem_ordinais, col_nominais, col_numericas)
    X_test, y_test = pipeline.treinar(df)
    pipeline.salvar()
    pipeline.salvar_pickle()
