from PIL import Image
from transformers import AutoModelForCausalLM, AutoProcessor
#修改成你的Kimi-VL-A3B-Thinking模型路径
model_path = "/input/input0/Kimi-VL-A3B-Thinking"
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    torch_dtype="auto",
    device_map="auto",
    trust_remote_code=True,
        local_files_only=True
)

processor = AutoProcessor.from_pretrained(model_path, trust_remote_code=True,local_files_only=True,)

image_paths = ["./figures/demo1.png", "./figures/demo2.png"]
images = [Image.open(path) for path in image_paths]
messages = [
    {
        "role": "user",
        "content": [
            {"type": "image", "image": image_path} for image_path in image_paths
        ] + [{"type": "text", "text": "Please infer step by step who this manuscript belongs to and what it records"}],
    },
]
text = processor.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt")
inputs = processor(images=images, text=text, return_tensors="pt", padding=True, truncation=True).to(model.device)
generated_ids = model.generate(**inputs, max_new_tokens=2048)
generated_ids_trimmed = [
    out_ids[len(in_ids) :] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
]
response = processor.batch_decode(
    generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
)[0]
print("输出",response)