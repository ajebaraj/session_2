# Updated pre_process_data.py
import os
import shutil

def pre_process(usecase_id, dataset_path, experiment_id):
    cwd = os.getcwd()
    project_name = f"project_{usecase_id}"
    project_root = os.path.join(cwd, project_name)
    train_dir = os.path.join(project_root, "images", "train")
    val_dir = os.path.join(project_root, "images", "test")

    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(val_dir, exist_ok=True)

    class_names = []
    for class_name in sorted(os.listdir(dataset_path)):
        class_path = os.path.join(dataset_path, class_name)
        if not os.path.isdir(class_path):
            continue

        class_names.append(class_name)
        images = sorted(os.listdir(class_path))
        split_index = int(len(images) * 0.8)
        train_images = images[:split_index]
        val_images = images[split_index:]

        os.makedirs(os.path.join(train_dir, class_name), exist_ok=True)
        for img in train_images:
            shutil.copy2(os.path.join(class_path, img), os.path.join(train_dir, class_name, img))

        os.makedirs(os.path.join(val_dir, class_name), exist_ok=True)
        for img in val_images:
            shutil.copy2(os.path.join(class_path, img), os.path.join(val_dir, class_name, img))

    class_dict = {i: name for i, name in enumerate(class_names)}

    data_dict = {
        'path': project_root,
        'train': 'images/train',
        'val': 'images/test',
        'names': class_dict
    }
    print("Pre-process complete, returning data dict.")
    return data_dict