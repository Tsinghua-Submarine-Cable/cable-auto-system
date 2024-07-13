import openai
from tqdm.autonotebook import tqdm
from utils import *

def station_ai_extract():
    openai.api_key = 'sk-8TVNENpSop8RDTKC8cEfBc77A7Ab4c6388F53a802a364753'
    openai.api_base = 'https://api.xty.app/v1'

    output_path = os.path.join('data', 'data_' + formatted_date, 'ai_output_station')
    create_path_if_not_exists(output_path)

    existed_result = find_all_file(output_path)

    path = os.path.join('data', 'data_' + formatted_date, 'station-articles')
    all_dir = find_all_dir(path)

    f = open('../station_prompt.txt', 'r', encoding='UTF-8')
    prompt = f.read()
    f.close()


    for i in tqdm(range(len(all_dir)), desc='Processing'):
        dir_name = all_dir[i]
        all_subdir = find_all_dir(os.path.join(path, dir_name))
        for j in range(len(all_subdir)):
            subdir_name = all_subdir[j]
            all_file = find_all_file(os.path.join(path, dir_name, subdir_name))
            for k in range(len(all_file)):
                file_name = all_file[k]
                if file_name in existed_result:
                    continue
                f = open(os.path.join(path, dir_name, subdir_name, file_name), 'r', encoding='UTF-8')
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "user", "content": prompt + f.read()}
                    ],
                    response_format={"type": "json_object"},
                )
                print(file_name, response.choices[0].message.content)
                f.close()
                if not os.path.exists(os.path.join(output_path, dir_name, subdir_name)):
                    os.makedirs(os.path.join(output_path, dir_name, subdir_name))
                f = open(os.path.join(output_path, dir_name, subdir_name, file_name), 'w', encoding='UTF-8')
                f.write(response.choices[0].message.content)
                f.close()


if __name__ == '__main__':
    station_ai_extract()
