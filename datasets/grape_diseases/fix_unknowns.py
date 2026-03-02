import re
from pathlib import Path

base = Path(__file__).parent
splits = ['train','val']

# mapping function based on filename tokens
def infer_class(name):
    s = re.sub(r'[^a-z0-9]', ' ', name.lower())
    tokens = s.split()
    if 'esca' in s:
        return 'esca'
    if 'healthy' in s or 'heal' in s:
        return 'healthy'
    if 'powdery' in s:
        return 'powdery_mildew'
    if 'downy' in s:
        return 'downy_mildew'
    if 'blight' in s:
        return 'leaf_blight'
    if 'bacterial' in s or ('leaf' in tokens and 'spot' in tokens) or 'bact' in s:
        return 'bacterial_leaf_spot'
    # black rot heuristics
    if 'black' in s or 'rot' in tokens or 'b rot' in s or 'brot' in s or 'b rot' in s:
        return 'black_rot'
    return None

summary = {}
for split in splits:
    summary[split] = {}
    unknown_dir = base / split / 'unknown'
    if not unknown_dir.exists():
        continue
    for p in unknown_dir.iterdir():
        if not p.is_file():
            continue
        cls = infer_class(p.name)
        if cls is None:
            cls = 'unknown'
        dest_dir = base / split / cls
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / p.name
        try:
            p.replace(dest)
            summary[split].setdefault(cls, 0)
            summary[split][cls] += 1
        except Exception as e:
            summary[split].setdefault('errors', 0)
            summary[split]['errors'] += 1

print('Move summary:')
for split, data in summary.items():
    print(split)
    for k, v in data.items():
        print(f'  {k}: {v}')
