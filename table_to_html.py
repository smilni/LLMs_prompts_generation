import pandas as pd
import json
import os


models = {
    "gptj": "GPT-J 6B",
    "gpt2_large": "GPT2 Large",
    "gpt_neo_2_7": "GPT Neo Large",
    "opt_6_7b": "OPT 6.7B",
    "bloomz": "BLOOMZ 3B",
    "bloom": "BLOOM 3B",
    "bloom_560m": "BLOOM 560M",
    "bloom_7b": "BLOOM 7B",
    "opt_125m": "OPT 125M",
}


def make_tables(questions_file, prompt_names, for_models=[]):
    f = open(questions_file)
    list_of_qs = json.load(f)
    html_templates = []
    big_df = pd.DataFrame()
    for prompt_name in prompt_names:
        html_template = ""
        for filename in os.listdir(f"models_outputs/{prompt_name}"):
            model_name = "_".join(filename.split("_")[: len(filename.split("_")) - 1])
            if for_models:
                if model_name not in for_models:
                    continue
            df = pd.read_csv(
                os.path.join(f"models_outputs/{prompt_name}", filename), sep="\t"
            )
            df["model"] = model_name
            big_df = pd.concat([big_df, df], ignore_index=True)
        dict_for_table = {}
        for question in list_of_qs[prompt_name]:
            if question not in dict_for_table:
                dict_for_table[question] = {}
                dict_for_table[question]["replies"] = {}
            for _, row in big_df.iterrows():
                if question in row["result"]:
                    dict_for_table[question]["question_type"] = row["utterances group"]
                    dict_for_table[question]["replies"][row["model"]] = {}
                    dict_for_table[question]["replies"][row["model"]]["reply"] = (
                        row["result"]
                        .split(question)[1]
                        .split("\n\n")[0]
                        .replace("\n", "")
                        .replace("AI: ", "")
                    )

        for question in dict_for_table.keys():
            html_template += (
                f"""<tr><td colspan=3 style="text-align: center">{question}</td></tr>"""
            )
            for model in dict_for_table[question]["replies"].keys():
                html_template += f"""<tr><td>{models[model]}</td><td>{dict_for_table[question]['replies'][model]['reply']}</td><td>{dict_for_table[question]["question_type"]}</td></tr>"""
        html_templates.append(html_template)
    return html_templates


all_tables = make_tables(
    "list_of_qs.json", ["pizza", "spacex", "dreambot"], for_models=["gptj", "bloom"]
)
print(all_tables)
