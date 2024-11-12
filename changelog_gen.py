from bs4 import BeautifulSoup
from bs4.element import TemplateString

# Open the changelog file, split it on <script> tag, use the 0th element

with open('frontend/.env') as f:
    version = f.read().replace('"', '').split('=')[1]

with open('frontend/src/components/modals/changelog.vue') as f:
    template = f.read().split('<script>')[0]

soup = BeautifulSoup(template, features='html.parser')

lines = [f'# {version}']
dividers = soup.select('div.divider')

for div in dividers:
    # Get the text from the divider
    lines.append(f'## {str([c for c in div.children][1]).strip()}')

    # Iterate through the siblings until we reach another divider
    sibling = div.find_next_sibling()
    if sibling.name == 'div':
        continue
    elif sibling.name != 'p':
        print('found non p, non div tag', sibling.name)
        continue

    while sibling is not None and sibling.name != 'div':
        is_info = False
        # It's definitely a p tag, got some rules to look at
        # If it's info text, add asterisks for italics
        if 'has-text-info' in sibling.attrs.get('class', set()):
            is_info = True

        # Parse the children elements of the p tag
        for child in sibling.children:
            if isinstance(child, TemplateString):
                line = str(child).strip()
                if len(line) == 0:
                    continue
                elif is_info:
                    lines.append(f'- *{line}*')
                else:
                    lines.append(f'- {line}')
            elif child.name == 'ul':
                for list_item in child.children:
                    if not isinstance(list_item, TemplateString):
                        lines.append(f'  - {str(list_item.contents[0]).strip()}')

        sibling = sibling.find_next_sibling()
    lines.append('\n')

print('\n'.join(lines))
