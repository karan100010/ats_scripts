import torch
from transformers import AutoFeatureExtractor, AutoModel
import os 
import pandas as pd
import librosa

#read all files inside subdirectories
def get_files_in_subfolders(folder):
    file_list = []
    for root, directories, files in os.walk(folder):
        for file in files:
            file_list.append(os.path.join(root, file))
    return file_list

def create_df(path):
    df=pd.DataFrame()
    files=get_files_in_subfolders(path)
    content=[]
    uuid=[]
    lang=[]
    features=[]

    for i in files:
    
        #lang.append(i.split("/")[1].split("_")[0])
        content.append(librosa.load(i, sr=16000)[0])
        if i.split("/")[1].split("\\")[0]=="srk":
            features.append({"artist": i.split("/")[1].split("\\")[0],"emo":"mild","path":i})
        else:
            features.append({"artist": i.split("/")[1].split("\\")[0],"emo":"angry","path":i})
    # df["uuid"]=uuid
    # df["lang"]=lang
    df["features"]=features
    df["content"]=content
    return df
        


df=create_df("language_identifucation_test/")


def genrate_wav_to_vec(df):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = AutoModel.from_pretrained('facebook/wav2vec2-base').to(device)
    feature_extractor = AutoFeatureExtractor.from_pretrained('facebook/wav2vec2-base')
    for i in range(len(df)):
        inputs = feature_extractor(
        df["content"].to_list(), sampling_rate=16_000, return_tensors="pt",
        padding=True, return_attention_mask=True, truncation=True, max_length=16_000).to("cuda")
        with torch.no_grad():
            embeddings = model(**inputs).last_hidden_state.mean(dim=1)
            df["embeddings"]=[i.cpu().numpy() for i in embeddings]
            return df

# from qdrant_client import QdrantClient
# client = QdrantClient("localhost", port=6333
# client.recreate_collection(
#     collection_name="bollywood",
#     vectors_config=models.VectorParams(size=768, distance=models.Distance.COSINE)
# )
# #lang=df.lang.to_list()
# client.upsert(
#     collection_name="bollywood",
#     points=models.Batch(
#         ids=[i for i in range(len(df))],
#         vectors=x["embeddings"],
#         payloads=x["features"].to_list()

    
#     )

# client.search(
#     collection_name="svs",
#     query_vector=df["embeddings"][13],
#     limit=10)
