import gradio as gr
from PIL import Image
from transformers import AutoModelForCausalLM, AutoProcessor
import os
import time
from datetime import datetime
import re

# 初始化全局模式
global_mode = "Compact mode"

# 加载多模态模型
model_path = "/openbayes/input/input0/Kimi-VL-A3B-Instruct"
model_path_thinking = "/openbayes/input/input0/Kimi-VL-A3B-Thinking"
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    torch_dtype="auto",
    device_map="auto",
    trust_remote_code=True,
    local_files_only=True
)
model_thinking = AutoModelForCausalLM.from_pretrained(
    model_path_thinking,
    torch_dtype="auto",
    device_map="auto",
    trust_remote_code=True,
    local_files_only=True
)

processor = AutoProcessor.from_pretrained(model_path, trust_remote_code=True, local_files_only=True)
processor_thinking = AutoProcessor.from_pretrained(model_path_thinking, trust_remote_code=True, local_files_only=True)

# 配置图片存储路径
save_image_path = "./uploaded_images/"
os.makedirs(save_image_path, exist_ok=True)


def animate_loading(dots):
    """生成动态的...效果"""
    return "..." + "." * (dots % 4)


def process_input(text, image_path, mode, history):
    global global_mode
    global_mode = mode
    current_history = history.copy()  # 关键修改：复制历史记录
    if global_mode == "Detailed mode":
        # 准备显示内容
        user_input_display = text or "(无文字)"
        if image_path:
            user_input_display += " 📷"
            try:
                image = Image.open(image_path)
            except Exception as e:
                error_msg = f"图片加载失败: {str(e)}"
                updated_history = current_history + [(user_input_display, error_msg)]
                yield updated_history, updated_history
                return
        else:
            image = None

        # 第一阶段：显示初始加载状态
        updated_history = current_history + [(user_input_display, animate_loading(0))]
        yield updated_history, updated_history

        # 第二阶段：后台处理与加载动画
        response = None
        error = None
        try:
            # 构建多模态消息
            messages = []
            if text:
                messages.append({"role": "user", "content": [{"type": "text", "text": text}]})
            if image:
                messages.append({"role": "user", "content": [{"type": "image", "image": image_path}]})

            # 准备模型输入
            text_prompt = processor_thinking.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt")

            if image and text:
                inputs = processor_thinking(
                    images=image,
                    text=text_prompt,
                    return_tensors="pt",
                    padding=True,
                    truncation=True
                ).to(model_thinking.device)
            elif text:
                inputs = processor_thinking(
                    text=text_prompt,
                    return_tensors="pt",
                    padding=True,
                    truncation=True
                ).to(model_thinking.device)
            elif image:
                inputs = processor_thinking(
                    images=image,
                    return_tensors="pt",
                    padding=True,
                    truncation=True
                ).to(model_thinking.device)

            # 生成响应
            generated_ids = model_thinking.generate(**inputs, max_new_tokens=512)
            generated_ids_trimmed = [
                out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
            ]
            response = processor_thinking.batch_decode(
                generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
            )[0]


        except Exception as e:
            error = f"处理错误: {str(e)}"

        # 更新最终结果
        final_response = response if response else error
        if "◁think▷" in final_response:
            final_response = re.sub(
                r'◁think▷(.*?)◁/think▷',
                lambda m: f"🤔 思考过程：\n{m.group(1)}\n\n📝 正式回答：\n",
                final_response,
                flags=re.DOTALL
            )
        final_history = current_history + [(user_input_display, final_response)]
        yield final_history, final_history
    else:
        # 准备显示内容
        user_input_display = text or "(无文字)"
        if image_path:
            user_input_display += " 📷"
            try:
                image = Image.open(image_path)
            except Exception as e:
                error_msg = f"图片加载失败: {str(e)}"
                updated_history = history + [(user_input_display, error_msg)]
                yield updated_history, updated_history
                return
        else:
            image = None

        # 第一阶段：显示初始加载状态
        updated_history = current_history + [(user_input_display, animate_loading(0))]
        yield updated_history, updated_history

        # 第二阶段：后台处理与加载动画
        response = None
        error = None
        try:
            # 构建多模态消息
            messages = []
            if text:
                messages.append({"role": "user", "content": [{"type": "text", "text": text}]})
            if image:
                messages.append({"role": "user", "content": [{"type": "image", "image": image_path}]})

            # 准备模型输入
            text_prompt = processor.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt")

            if image and text:
                inputs = processor(
                    images=image,
                    text=text_prompt,
                    return_tensors="pt",
                    padding=True,
                    truncation=True
                ).to(model.device)
            elif text:
                inputs = processor(
                    text=text_prompt,
                    return_tensors="pt",
                    padding=True,
                    truncation=True
                ).to(model.device)
            elif image:
                inputs = processor(
                    images=image,
                    return_tensors="pt",
                    padding=True,
                    truncation=True
                ).to(model.device)

            # 生成响应
            generated_ids = model.generate(**inputs, max_new_tokens=512)
            generated_ids_trimmed = [
                out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
            ]
            response = processor.batch_decode(
                generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
            )[0]

        except Exception as e:
            error = f"处理错误: {str(e)}"

        # 更新最终结果
        final_response = response if response else error
        final_history = current_history + [(user_input_display, final_response)]
        yield final_history, final_history


def capture_and_process(text_input, image_input, mode, history):
    current_history = history.copy()  # 关键修改：保持历史连续性
    """处理输入并保持加载动画"""
    # 清空输入并保存到临时文件
    image_path = None
    if image_input:
        try:
            image_path = os.path.join(save_image_path, f"temp_{int(time.time())}.png")
            image_input.save(image_path)
        except Exception as e:
            error_msg = f"图片保存失败: {str(e)}"
            return history + [(error_msg, "")], history + [(error_msg, "")], "", None

    # 返回清空后的输入组件值
    return "", None, text_input, image_path, current_history


with gr.Blocks(title="Kimi-VL") as demo:
    gr.Markdown("## Kimi-VL")

    with gr.Row():
        chatbot = gr.Chatbot(label="Session flow", height=500, elem_classes=["dots"])
        history = gr.State([])

    with gr.Row():
        with gr.Column(scale=3):
            text_input = gr.Textbox(label="Input text", placeholder="Enter text content...", lines=4)
            image_input = gr.Image(label="Upload pictures", type="pil", height=200)

        with gr.Column(scale=1):
            mode = gr.Dropdown(choices=["Compact mode", "Detailed mode"], value="Compact mode", label="Response mode")
            submit_btn = gr.Button("send", variant="primary")
            clear_btn = gr.Button("Clear history", variant="secondary")

    temp_text = gr.State()
    temp_image = gr.State()

    submit_btn.click(
        capture_and_process,
        inputs=[text_input, image_input, mode, history],
        outputs=[text_input, image_input, temp_text, temp_image, history],
        queue=False
    ).then(
        process_input,
        inputs=[temp_text, temp_image, mode, history],
        outputs=[chatbot, history]
    )

    clear_btn.click(
        lambda: ([], []),
        inputs=[],
        outputs=[chatbot, history]
    )

demo.launch(server_name="0.0.0.0", server_port=8080)