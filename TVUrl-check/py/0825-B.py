import json

# 原始文件路径
original_file_path = './code/0825.json'  # 请替换为实际路径
# 新的 "sites" 数据文件路径
replacement_file_path = './out/0825.txt'  # 请替换为实际路径
# 输出文件路径
output_file_path = '0825.json'

# 加载原始数据
with open(original_file_path, 'r', encoding='utf-8') as file:
    original_data = json.load(file)

replacement_sites = []
# 读取想替换的 "sites" 部分
with open(replacement_file_path, 'r', encoding='utf-8') as file:
    content_list = file.readlines()
    for content in content_list:
        try:
            """
            '{"key":"豆豆","name":"豆瓣┃搜索","type": 3, "api": "csp_DouDou","searchable": 0,"quickSearch": 0,"filterable": 0}, 这种格式换成
            '{"key":"豆豆","name":"豆瓣┃搜索","type": 3, "api": "csp_DouDou","searchable": 0,"quickSearch": 0,"filterable": 0}  去除逗号
            """
            replacement_sites.append(json.loads(content.strip()[0:-1])) ## 格式化字符串
        except:
            pass

# 替换 "sites" 部分
original_data['sites'] = replacement_sites

new_logo_url = "https://ghproxy.net/https://raw.githubusercontent.com/ne7359/url/main/fan/AW1.gif"
# Check if 'logo' line exists
if 'logo":' not in content:
    # Construct the logo line to add
    logo_line = f'    "logo": "{new_logo_url}",\n'
    # Insert the logo line after "spider": line
    content = re.sub(r'("spider": "[^"]+",\n)', fr'\1{logo_line}', content)

# 保存更新后的数据到新文件
with open(output_file_path, 'w', encoding='utf-8') as file:
    json.dump(original_data, file, ensure_ascii=False, indent=4)

print("更新后的数据已保存。")
