import argparse
from pathlib import Path

import json
import pandas as pd
import pyarrow.parquet as pq

ROOT_DIR = Path(__file__).resolve().parents[1]

def read_jsonl(filepath: str) -> pd.DataFrame:
    with open(filepath, 'r', encoding='utf-8') as file:
        lines = []
        for line in file:
            line = line.strip()
            if line:
                lines.append(json.loads(line))
    return pd.DataFrame(lines)

def lowercase_column_names(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [str(col_name).lower() for col_name in df.columns]
    return df

def main(input_filename: str, trx_status: str, payment_method_type_col_nested: str='payment_method_type'):
    
    input_file_path = ROOT_DIR / "data" / "input" / input_filename
    
    if not input_file_path.exists():
        raise FileNotFoundError(f"El archivo {input_file_path} no fue encontrado.")
    
    if str(trx_status).lower() not in ['approved', 'declined', 'error']:
        raise ValueError(f"""
            El estado de la transacción sobre la que se solicita la vista agregada
            debe ser: approved, declined o error.
        """)
        
    trx_status = str(trx_status).lower()
    
    trx_df = read_jsonl(input_file_path)
    trx_df = lowercase_column_names(trx_df)
    input_file_record_count = len(trx_df)
    
    payment_method_type_df = pd.json_normalize(trx_df[payment_method_type_col_nested])
    payment_method_type_df.index = trx_df.index
    payment_method_type_df.columns = payment_method_type_df.columns.str.replace('.', '_', regex=False)
    
    trx_df = trx_df.drop(columns=[payment_method_type_col_nested])
    trx_normalized_df = pd.concat([trx_df, payment_method_type_df], axis=1)
    trx_normalized_df['trx_date'] = pd.to_datetime(trx_normalized_df['created_at']).dt.date
    
    trx_aggregated = trx_normalized_df[
        trx_normalized_df['status'].str.lower()==trx_status
    ]
    
    view_df = trx_aggregated.groupby(['extra_bin', 'trx_date']).agg(
        **{
            f"{trx_status}_count": ('id', 'count'),
            f"{trx_status}_amount": ('amount_in_cents', 'sum')
        }
    ).reset_index()

    view_df.columns = view_df.columns.str.replace('extra_', '', regex=False)
    
    view_df["audit_input_file"] = input_filename
    
    output_path = ROOT_DIR / "data" / "output" / f"view_{trx_status}_trxs.parquet"
    view_df = view_df.sort_values(["bin", "trx_date"]).reset_index(drop=True)
    view_df.to_parquet(output_path, index=False)

    audit_data = {
        "executed_at"               : pd.Timestamp.utcnow().isoformat(),
        "input_file"                : input_filename,
        "trx_status"                : trx_status,
        "input_record_count"        : input_file_record_count,
        "output_record_count"       : len(view_df),
        "output_file"               : output_path.name,
    }

    meta_path = ROOT_DIR / "data" / "output" / f"view_{trx_status}_trxs.meta.json"
    with open(meta_path, "w") as f:
        json.dump(audit_data, f, indent=4)
    
    return view_df

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input-filename", 
        required=True,
        help="Nombre del archivo JSONL a procesar dentro de la carpeta data/input")
    parser.add_argument(
        "--trx-status",
        required=False,
        default="approved", 
        help="Estado de la transacción sobre la que se solicita la vista agregada debe ser: approved, declined o error. Por defecto: approved"
    )
    
    args = parser.parse_args()
    
    main(input_filename=args.input_filename, trx_status=args.trx_status)