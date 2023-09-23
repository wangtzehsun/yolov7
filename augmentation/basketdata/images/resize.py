from PIL import Image

# 打开原始照片
original_image = Image.open("001.jpg")

# 调整大小为640x640像素
new_size = (640, 640)
resized_image = original_image.resize(new_size)

# 保存调整后的照片
resized_image.save("a001.jpg")

# 关闭原始照片
original_image.close()
