from tasks import preprocess,feature_engineering
from celery import chain
import pandas as pd 
import pandas as pd
from celery import chain

def main():
    df = pd.read_csv(r"C:\project_smt 4\datwer\project ETL\ETL\dirty_cafe_sales.csv")
    task_ids = []

    for idx, row in df.iterrows():
        single_row_df = pd.DataFrame([row])

        json_data = single_row_df.to_json(orient='split')

        result = chain(
            preprocess.s(json_data),
            feature_engineering.s()
        )
        result_id = result.apply_async()
        print(f"ETL chain dispatched for index {idx}, task id: {result_id.id}")
        task_ids.append(result_id.id)
    print(task_ids)
    return task_ids


if __name__ == "__main__":
    main()
