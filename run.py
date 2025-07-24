import os 
import json
import requests
import argparse

Bmoji_data = None

def download_emoji_package(target_id, quiet=False):
    """
    根据target_id下载表情包
    
    Args:
        target_id (str): 表情包ID
        quiet (bool): 是否静默模式（不输出下载信息）
        
    Returns:
        bool: 下载成功返回True，否则返回False
    """
    if not quiet:
        print("Starting to download emoji package...")
        print(f"Target ID: {target_id}")
    
    if Bmoji_data is None or 'Bmoji_data' not in globals():
        # Load emoji data
        with open(os.path.join('Bmoji', 'data', 'emoji_data.json'), 'r', encoding='utf-8') as f:
            raw_json = f.read()
    else:
        raw_json = json.dumps(Bmoji_data)
    
    
    json_data = json.loads(raw_json)

    # Find target package
    found = False
    for package in json_data['packages']:
        if package['id'] == int(target_id):
            target_data = package
            found = True
            break

    if not found:
        if not quiet:
            print(f"Package with ID {target_id} not found.")
        return False

    if not quiet:
        print(f"Found package: {target_data['text']} (ID: {target_data['id']})")

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

    # Download icon first
    icon_url = target_data['icon'].replace('{baseURL}', 'https://i0.hdslb.com')
    icon_filepath = os.path.join(emojis_folder, f"{prefix}icon.png")
    
    if not quiet:
        print(f"Downloading icon from {icon_url}")
    response = requests.get(icon_url)
    with open(icon_filepath, 'wb') as f:
        f.write(response.content)

    # Download emojis
    for emoji in target_data['emojis']:
        name = emoji['name']
        url = emoji['url'].replace('{baseURL}', 'https://i0.hdslb.com')
        
        filename = f"{prefix}{name}.png"
        filepath = os.path.join(emojis_folder, filename)
        
        if not quiet:
            print(f"Downloading {name} from {url}")
        response = requests.get(url)
        
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        items.append(name)

    # Set icon name as "icon"
    icon_name = "icon"

    # Create info.json
    info = {
        "name": target_data['text'],
        "prefix": prefix,
        "icon": icon_name,
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

    if not quiet:
        print(f"All emojis downloaded and organized in '{base_folder}' folder")
        print(f"info.json created with {len(items)} items")
    return True

def is_valid_id(id_str):
    """检查ID是否为合法数字"""
    try:
        int(id_str)
        return True
    except ValueError:
        return False

def main():
    parser = argparse.ArgumentParser(description='下载B站表情包工具')
    parser.add_argument('id', nargs='?', default=None, 
                       help='要下载的表情包ID (默认为7961)')
    parser.add_argument('-q', '--quiet', action='store_true',
                       help='静默模式，不输出下载信息')
    parser.add_argument('-d', '--data', default=None,
                       help='指定Bmoji数据文件路径')

    args = parser.parse_args()
    
    # 处理默认ID情况
    if args.id is None:
        default_id = '7961'
        if not args.quiet:
            choice = input(f"未指定ID，是否使用默认ID {default_id}? (y/n): ").strip().lower()
            if choice != 'y':
                print("操作已取消")
                return
        target_id = default_id
    else:
        if not is_valid_id(args.id):
            print("错误: ID必须是数字")
            parser.print_help()
            return
        target_id = args.id
        
    # 如果指定了Bmoji数据文件路径，则加载数据
    if args.data:
        global Bmoji_data
        if not os.path.exists(args.data):
            print(f"错误: 指定的数据文件 {args.data} 不存在")
            return
        with open(args.data, 'r', encoding='utf-8') as f:
            Bmoji_data = json.load(f)
    
    download_emoji_package(target_id, args.quiet)

if __name__ == "__main__":
    main()