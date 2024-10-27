# 用图搜图

# pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
import torch,os
from PIL import Image
import timm  # timm是一个PyTorch模型库,虽然可能和图像处理没有关系,但是它提供了广泛的预训练模型和计算机视觉模型的集合,这对我们来进行深度学习的时候是非常有帮助的
from sklearn.preprocessing import normalize
from timm.data import resolve_data_config
from timm.data.transforms_factory import create_transform
# HF_ENDPOINT = os.environ.get("HF_ENDPOINT", "https://hf-mirror.com")
import os
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com' # 失败了就手动设置环境变量这个.HF_ENDPOINT.再运行代码.                HF_ENDPOINT=https://hf-mirror.com python 5.py

class FeatureExtractor:
    def __init__(self, modelname):
        # Load the pre-trained model
        self.model = timm.create_model(
            modelname, pretrained=True, num_classes=0, global_pool="avg"
        )
        self.model.eval()

        # Get the input size required by the model
        self.input_size = self.model.default_cfg["input_size"]

        config = resolve_data_config({}, model=modelname)
        # Get the preprocessing function provided by TIMM for the model
        self.preprocess = create_transform(**config)

    def __call__(self, imagepath):
        # Preprocess the input image
        input_image = Image.open(imagepath).convert("RGB")  # Convert to RGB if needed
        input_image = self.preprocess(input_image)

        # Convert the image to a PyTorch tensor and add a batch dimension
        input_tensor = input_image.unsqueeze(0)

        # Perform inference
        with torch.no_grad():
            output = self.model(input_tensor)

        # Extract the feature vector
        feature_vector = output.squeeze().numpy()

        return normalize(feature_vector.reshape(1, -1), norm="l2").flatten()
      
import os

extractor = FeatureExtractor("resnet34") # 这个网络最后特征512的.
from pymilvus import MilvusClient

# Set up a Milvus client
client = MilvusClient(uri="example.db")
# Create a collection in quick setup mode
if 0: #============这个代码运行一次就行.穿件数据库.# 以后运行都设置成if 0.
    if client.has_collection(collection_name="image_embeddings"):
        client.drop_collection(collection_name="image_embeddings")
    client.create_collection(
        collection_name="image_embeddings",
        vector_field_name="vector",
        dimension=512,
        auto_id=True,
        enable_dynamic_field=True,
        metric_type="COSINE",
    )
        
        
        
        
        
        
        
        
        
        
        


    root = "./train"
    insert = True
    if insert is True:
        for dirpath, foldername, filenames in os.walk(root):# 多级目录遍历.
            for filename in filenames:
                if filename.endswith(".JPEG"):
                    filepath = dirpath + "/" + filename
                    image_embedding = extractor(filepath)
                    client.insert(
                        "image_embeddings",
                        {"vector": image_embedding, "filename": filepath},
                    )
                    
                    
import time
print('开始查询')
kaishi=time.time()                
# from IPython.display import display

query_image = "test/Airedale/n02096051_4092.JPEG"

results = client.search(
    "image_embeddings",
    data=[extractor(query_image)],
    output_fields=["filename"],
    search_params={"metric_type": "COSINE"},
)
images = []
for result in results:
    for hit in result[:10]:
        filename = hit["entity"]["filename"]
        img = Image.open(filename)
        img = img.resize((150, 150))
        images.append(img)

width = 150 * 5
height = 150 * 2
concatenated_image = Image.new("RGB", (width, height))

for idx, img in enumerate(images):
    x = idx % 5
    y = idx // 5
    concatenated_image.paste(img, (x * 150, y * 150))
import cv2
Image.open(query_image).save('查询图片.png')
concatenated_image.save('结果图片.png')

print(time.time()-kaishi,'使用的时间')

# cv2.imwrite('查询的.png',query_image)
# cv2.imwrite('招到的的.png',concatenated_image)

# display("query")
# display(Image.open(query_image).resize((150, 150)))
# display("results")
# display(concatenated_image)
                
                
                
                
                
                
                
                
                
                
                
                
                