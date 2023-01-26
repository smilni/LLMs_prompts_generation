from collections import Counter
import pandas as pd


def get_results(table):
    results = {}
    question_split = table.split('<td colspan=2 style="text-align: center"><b>')
    for question in question_split:
        models_split = question.split(
            """</tr>
<tr>"""
        )
        for model in models_split:
            if (
                "<b>" not in model
                and model.strip()
                and "<caption>" not in model
                and len(model) > 10
            ):
                model_name = (
                    model.split("</td>")[0]
                    .replace("<td>", "")
                    .replace("<tr>", "")
                    .strip()
                )
                corr_value = model.split("</td>")[-2]
                if "Correct" in corr_value:
                    result = "correct"
                if "Incorrect" in corr_value:
                    result = "incorrect"
                if "Partially correct" in corr_value:
                    result = "part_correct"
                if model_name not in results:
                    results[model_name] = [result]
                else:
                    results[model_name].append(result)
    return results


def make_tables(table_file, list_prompts=["spacex", "pizza", "dreambot"]):
    all_tables = []
    with open(table_file, "r") as a:
        tables = a.read()
    tables_split = tables.split('<table BORDER=1 style="width: 100%">')
    dict_res = {
        "spacex": get_results(tables_split[1]),
        "pizza": get_results(tables_split[2]),
        "dreambot": get_results(tables_split[3]),
    }
    for prompt in list_prompts:
        count_dict = {k: Counter(v) for k, v in dict_res[prompt].items()}
        res = (
            pd.DataFrame.from_dict(count_dict, orient="index")
            .fillna(0)
            .astype("int")
            .sort_index()
            .sort_index(1)
        )
        all_tables.append(res)
        res.to_csv(f"tables_models_eval/{prompt}.csv")
    return all_tables


make_tables("html_table.txt")
