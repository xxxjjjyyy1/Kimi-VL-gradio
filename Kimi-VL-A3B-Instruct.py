from PIL import Image
from transformers import AutoModelForCausalLM, AutoProcessor
import torch
#修改成你的Kimi-VL-A3B-Instruct模型路径
model_path = "/input/input0/Kimi-VL-A3B-Instruct"
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    torch_dtype="auto",
    device_map="auto",
   trust_remote_code=True,
    local_files_only=True
)

processor = AutoProcessor.from_pretrained(model_path, trust_remote_code=True,local_files_only=True)

image_path = "./figures/demo.png"
image = Image.open(image_path)
#messages = [{"role": "user", "content": [{"type": "image", "image": image_path}, {"type": "text", "text": "你好"}]}]
messages = [{"role": "user", "content": [{"type": "text", "text": "年后"}]}]
text = processor.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt")

inputs = processor( text=text, return_tensors="pt", padding=True, truncation=True).to(model.device)

generated_ids = model.generate(**inputs, max_new_tokens=512)

generated_ids_trimmed = [
    out_ids[len(in_ids) :] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
]
response = processor.batch_decode(
    generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
)[0]
print("输出",response)