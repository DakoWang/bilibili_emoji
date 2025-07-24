import os 
import json
import requests

def download_emoji_package(target_id):
    """
    根据target_id下载表情包
    
    Args:
        target_id (str): 表情包ID
        
    Returns:
        bool: 下载成功返回True，否则返回False
    """
    # Load emoji data
    with open(os.path.join('Bmoji', 'data', 'emoji_data.json'), 'r', encoding='utf-8') as f:
        raw_json = f.read()

    json_data = json.loads(raw_json)

    # Find target package
    found = False
    for package in json_data['packages']:
        if package['id'] == int(target_id):
            target_data = package
            found = True
            break

    if not found:
        print(f"Package with ID {target_id} not found.")
        return False

    # Create output directory
    if not os.path.exists('output'):
        os.mkdir('output')

    base_folder = 'output/' + str(target_data['id']) + '_' + target_data['text']
    if not os.path.exists(base_folder):
        os.mkdir(base_folder)

    emojis_folder = base_folder
    if not os.path.exists(emojis_folder):
        os.mkdir(emojis_folder)

    # Define prefix
    prefix = f"{target_data['id']}_"

    items = []

    # Download emojis
    for emoji in target_data['emojis']:
        name = emoji['name']
        url = emoji['url'].replace('{baseURL}', 'https://i0.hdslb.com')
        
        filename = f"{prefix}{name}.png"
        filepath = os.path.join(emojis_folder, filename)
        
        print(f"Downloading {name} from {url}")
        response = requests.get(url)
        
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        items.append(name)

    # Create info.json
    info = {
        "name": target_data['text'],
        "prefix": prefix,
        "type": "png",
        "items": items
    }

    info_path = os.path.join(base_folder, 'info.json')
    with open(info_path, 'w', encoding='utf-8') as f:
        json.dump(info, f, ensure_ascii=False, indent=2)

    # Create README.md
    readme_content = f"""# {target_data['text']} Emojis

![pic]({target_data['icon'].replace('{baseURL}', 'https://i0.hdslb.com')})

## emoji info
- ID: {target_data['id']}
- Name: {target_data['text']}
- Count: {len(items)}
- prefix: `{prefix}`

## emoji list
"""

    # Add emoji table to README
    readme_content += "| name | pic |\n"
    readme_content += "|------|------|\n"
    for emoji in target_data['emojis']:
        emoji_url = emoji['url'].replace('{baseURL}', 'https://i0.hdslb.com')
        readme_content += f"| {emoji['name']} | ![{emoji['name']}]({emoji_url}) |\n"

    # Save README.md
    readme_path = os.path.join(base_folder, 'README.md')
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)

    print(f"All emojis downloaded and organized in '{base_folder}' folder")
    print(f"info.json created with {len(items)} items")
    return True

# 使用示例
if __name__ == "__main__":
    target_id = '7961'
    download_emoji_package(target_id)