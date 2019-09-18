# -*- coding:utf-8 -*-
"""
Run script with no args, if wanna regenerate, just delete some useless name
"""
import commentjson as json
import os

os.chdir(os.path.split(os.path.realpath(__file__))[0])
os.chdir('../')  # theme path

src = 'src/'
dst = 'theme/'
assert (os.path.exists(src))


def gen(name):
    assert (src + name)
    with open(src + name, 'r') as f:
        config = json.load(f)
    with open(src + 'default.json', 'r') as f:
        default = json.load(f)

    colormap=config['colormap']

    # color
    colors = default['colors']
    for k, v in default['colors'].items():
        if v in colormap:
            print(k, v)
            colors[k] = colormap[v]

    # token-color
    tokenColors = []
    for item in default['tokenColors']:
        try:
            if item['settings']['foreground'] in colormap:
                item['settings']['foreground'] = colormap[v]
        except:
            pass
        tokenColors.append(item)


    # writting
    default['name'] = config['description']
    default['colors'] = colors
    default['tokenColors'] = tokenColors
    with open(dst + name, 'w') as f:
        json.dump(default, f, indent=4)

    return config['name'], [dst + name, config['uiTheme']]


if __name__ == "__main__":
    info = {}
    # Pre-Load
    with open('package.json', 'r') as f:
        package = json.load(f)
    for theme in package['contributes']['themes']:
        info[theme['label']] = [theme['path'], theme['uiTheme']]

    # Generate and overrite
    name = ['dark', 'less_dark', 'light']
    for n in name:
        n = n + '.json'
        try:
            k, v = gen(n)
            info[k] = v
        except Exception as e:
            print('failed', n, e)
            pass

    # Regen labels
    data = []
    for k, vs in info.items():
        data.append({
            'label': k,
            'path': vs[0],
            'uiTheme': vs[1],
        })
    package['contributes']['themes'] = data

    with open('package.json', 'w') as f:
        json.dump(package, f, indent=4)