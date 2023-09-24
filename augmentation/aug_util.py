import albumentations as A
import cv2
import os

from albumentations import OneOf, MotionBlur, MedianBlur, Blur

"""
该脚本主要实现了利用albumentations工具包对yolo标注数据进行增强
给定一个存放图像和标注文件的主目录，在主目录下自动生成增强的图像和标注文件
"""


def get_enhance_save(old_images_files, old_labels_files, label_list, enhance_images_files, enhance_labels_files):
    # 这里设置指定的数据增强方法
    transform = A.Compose([
        # A.RandomCrop(width=450, height=450),
        # A.HorizontalFlip(p=1),
        # A.RandomShadow(shadow_roi=(0, 0.5, 1, 1), num_shadows_lower=1, num_shadows_upper=2, shadow_dimension=5, always_apply=False, p=0.5),
        A.VerticalFlip(p=0.5),
        OneOf([
            # 模糊相关操作
            MotionBlur(p=.2),
            MedianBlur(blur_limit=3, p=0.2),
            Blur(blur_limit=3, p=0.1),
        ], p=0.2),
        A.RandomBrightnessContrast(p=0.9),
    ], bbox_params=A.BboxParams(format='yolo', min_area=1024, min_visibility=0.2, label_fields=['class_labels']))

    # 这里指定修改后image和label的文件名
    mid_name = "_VerticalFlip"

    label_files_name = os.listdir(old_labels_files)

    for name in label_files_name:

        if name == "classes.txt":
            continue

        for i in range(0, 20):

            label_files = os.path.join(old_labels_files, name)

            yolo_b_boxes = open(label_files).read().splitlines()

            bboxes = []

            class_labels = []

            # 对一个txt文件的每一行标注数据进行处理
            for b_box in yolo_b_boxes:
                b_box = b_box.split(" ")
                m_box = b_box[1:5]

                m_box = list(map(float, m_box))

                m_class = b_box[0]

                bboxes.append(m_box)
                class_labels.append(label_list[int(m_class)])

            # 读取对应的图像
            image_path = os.path.join(old_images_files, name.replace(".txt", ".jpg"))
            if os.path.exists(image_path) is False:
                image_path = os.path.join(old_images_files, name.replace(".txt", ".jpg"))

            image = cv2.imread(image_path)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # 调用上面定义的图像增强方法进行数据增强
            transformed = transform(image=image, bboxes=bboxes, class_labels=class_labels)
            transformed_image = transformed['image']
            transformed_image = cv2.cvtColor(transformed_image, cv2.COLOR_BGR2RGB)
            transformed_b_boxes = transformed['bboxes']
            transformed_class_labels = transformed['class_labels']

            # 先判断目标文件夹路径是否存在
            if os.path.exists(enhance_images_files) is False:
                os.mkdir(enhance_images_files)
            a, b = os.path.splitext(name)

            int_name = str(int(a) + i)

            new_name = int_name + mid_name + b
            cv2.imwrite(os.path.join(enhance_images_files, new_name.replace(".txt", ".jpg")), transformed_image)

            if os.path.exists(enhance_labels_files) is False:
                os.mkdir(enhance_labels_files)

            new_txt_file = open(os.path.join(enhance_labels_files, new_name), "w")

            new_bboxes = []

            for box, label in zip(transformed_b_boxes, transformed_class_labels):

                new_class_num = label_list.index(label)
                box = list(box)
                for i in range(len(box)):
                    box[i] = str(('%.5f' % box[i]))
                box.insert(0, str(new_class_num))
                new_bboxes.append(box)

            for new_box in new_bboxes:

                for ele in new_box:
                    if ele is not new_box[-1]:
                        new_txt_file.write(ele + " ")
                    else:
                        new_txt_file.write(ele)

                new_txt_file.write('\n')

            new_txt_file.close()


def main():
    root = r"F:\ESCI\yolov7\augmentation\basketdata"

    old_images_files = os.path.join(root, "raw_images")
    old_labels_files = os.path.join(root, "raw_labels")

    enhance_images_files = os.path.join(root, "images")
    enhance_labels_files = os.path.join(root, "labels")

    # 这里设置数据集的类别
    label_list = ["Banana", "Pluot", "Tomato", "Orange", "Apple"]

    # 实现对传入的数据文件进行遍历读取，并进行数据增强
    get_enhance_save(old_images_files, old_labels_files, label_list, enhance_images_files, enhance_labels_files)


if __name__ == '__main__':
    main()