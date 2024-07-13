import json

import openai
from tqdm.autonotebook import tqdm
from utils import *

def station_ai_extract():
    openai.api_key = 'sk-l3tKgucSLpTjADcl51C48460D6Eb4eC2B60c2147B25f0b5d'
    openai.api_base = 'https://api.xty.app/v1'

    output_path = os.path.join('data', 'data_' + formatted_date, 'ai_output_cable')
    create_path_if_not_exists(output_path)

    existed_result = find_all_file(output_path)

    path = os.path.join('data', 'data_' + formatted_date, 'cable_introduction')
    all_file = find_all_file(path)

    f = open('../cable_prompt.txt', 'r', encoding='UTF-8')
    prompt = f.read()
    f.close()


    for i in tqdm(range(len(all_file)), desc='Processing'):
        for k in range(len(all_file)):
            file_name = all_file[k]
            if file_name in existed_result:
                continue
            f = open(os.path.join(path, file_name), 'r', encoding='UTF-8')
            dic = json.load(f)
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "user", "content": prompt + dic['content']}
                ],
                response_format={"type": "json_object"},
            )
            print(file_name, response.choices[0].message.content)
            f.close()
            f = open(os.path.join(output_path, file_name), 'w', encoding='UTF-8')
            f.write(response.choices[0].message.content)
            f.close()


if __name__ == '__main__':
    station_ai_extract()
