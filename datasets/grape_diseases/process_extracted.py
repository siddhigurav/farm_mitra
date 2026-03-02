import os
import shutil
from pathlib import Path
import random

BASE = Path(__file__).parent
TEMP = BASE / 'temp_extract'
TRAIN = BASE / 'train'
VAL = BASE / 'val'

CATEGORIES = [
    'healthy', 'downy_mildew', 'powdery_mildew', 'bacterial_leaf_spot',
    'black_rot', 'esca', 'leaf_blight'
]

IMAGE_EXTS = {'.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff'}


def find_split_files():
    train_file = None
    val_file = None
    for p in TEMP.rglob('*'):
        if p.is_file():
            name = p.name.lower()
            if name in ('train.txt', 'train.csv') or 'train' in name and p.suffix in ('.txt', '.csv'):
                train_file = p
            if name in ('val.txt', 'val.csv', 'validation.txt') or 'val' in name and p.suffix in ('.txt', '.csv'):
                val_file = p
    return train_file, val_file


def read_list_file(p):
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        lines = [l.strip() for l in f if l.strip()]
    return lines


def find_source_for_name(name):
    # search TEMP for a file ending with name
    for p in TEMP.rglob('*'):
        if p.is_file() and p.name == name:
            return p
    # fallback: case-insensitive
    lname = name.lower()
    for p in TEMP.rglob('*'):
        if p.is_file() and p.name.lower() == lname:
            return p
    return None


def infer_category_from_path(p: Path):
    parts = [pp.lower() for pp in p.parts]
    for cat in CATEGORIES:
        if cat in parts:
            return cat
    # try filename match
    name = p.name.lower()
    for cat in CATEGORIES:
        compact = cat.replace('_', '')
        if compact in name:
            return cat
    return 'unknown'


def ensure_dst(split, category):
    dst = BASE / split / category
    dst.mkdir(parents=True, exist_ok=True)
    return dst


def move_file(src: Path, split: str):
    cat = infer_category_from_path(src)
    dst = ensure_dst(split, cat)
    try:
        shutil.move(str(src), str(dst / src.name))
        return True, cat
    except Exception as e:
        print('Failed to move', src, e)
        return False, cat


def move_using_split(train_list, val_list):
    summary = { 'train': {}, 'val': {} }
    for line in train_list:
        name = Path(line).name
        src = find_source_for_name(name)
        if src:
            ok, cat = move_file(src, 'train')
            summary['train'].setdefault(cat, 0)
            if ok: summary['train'][cat] += 1
    for line in val_list:
        name = Path(line).name
        src = find_source_for_name(name)
        if src:
            ok, cat = move_file(src, 'val')
            summary['val'].setdefault(cat, 0)
            if ok: summary['val'][cat] += 1
    return summary


def move_class_dirs():
    # If TEMP contains directories named after classes, move contents to train by default
    summary = {'train': {}}
    for p in TEMP.iterdir():
        if p.is_dir():
            lname = p.name.lower()
            if lname in ('train', 'val'):
                split = lname
                for child in p.iterdir():
                    if child.is_dir():
                        cat = child.name.lower()
                        if cat in CATEGORIES:
                            for img in child.rglob('*'):
                                if img.suffix.lower() in IMAGE_EXTS:
                                    ok, _ = move_file(img, split)
                                    summary.setdefault(split, {}).setdefault(cat, 0)
                                    if ok: summary[split][cat] += 1
            elif lname in CATEGORIES:
                # move all images into train/<lname>
                for img in p.rglob('*'):
                    if img.suffix.lower() in IMAGE_EXTS:
                        ok, _ = move_file(img, 'train')
                        summary['train'].setdefault(lname, 0)
                        if ok: summary['train'][lname] += 1
    return summary


def auto_split_single_folder():
    # Take all images under TEMP and split 80/20 into train/val with unknown category
    imgs = [p for p in TEMP.rglob('*') if p.is_file() and p.suffix.lower() in IMAGE_EXTS]
    random.shuffle(imgs)
    split_idx = int(0.8 * len(imgs))
    train_imgs = imgs[:split_idx]
    val_imgs = imgs[split_idx:]
    summary = {'train': {'unknown': 0}, 'val': {'unknown': 0}}
    for img in train_imgs:
        ok, _ = move_file(img, 'train')
        if ok: summary['train']['unknown'] += 1
    for img in val_imgs:
        ok, _ = move_file(img, 'val')
        if ok: summary['val']['unknown'] += 1
    return summary


def main():
    if not TEMP.exists():
        print('Temp folder not found:', TEMP)
        return

    train_file, val_file = find_split_files()
    if train_file and val_file:
        print('Found split files:', train_file, val_file)
        train_list = read_list_file(train_file)
        val_list = read_list_file(val_file)
        summary = move_using_split(train_list, val_list)
        print('Moved using split files. Summary:')
        print(summary)
        return

    # If extract contains train/val dirs or class dirs
    summary = move_class_dirs()
    if summary and any(summary.values()):
        print('Moved using class dirs. Summary:')
        print(summary)
        return

    # fallback: auto split
    summary = auto_split_single_folder()
    print('Auto-split performed. Summary:')
    print(summary)

if __name__ == '__main__':
    main()
