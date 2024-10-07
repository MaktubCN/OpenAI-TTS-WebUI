# app.py

import gradio as gr
import requests
import tempfile
from languages import languages

def generate_audio(input_text, voice, output_format, base_url_input, api_key_input, request: gr.Request):
    # 获取 URL 参数
    query_params = request.query_params
    # 优先使用 URL 参数中的 base_url 和 api_key
    base_url = query_params.get("base_url", base_url_input)
    api_key = query_params.get("api_key", api_key_input)
    # 准备请求负载
    payload = {
        "model": "tts-1",
        "input": input_text,
        "voice": voice.lower(),
        "format": output_format
    }
    headers = {
        'Authorization': api_key,
        'Content-Type': 'application/json'
    }
    # 构造请求 URL
    url = f"{base_url}/v1/audio/speech"
    # 发起 POST 请求
    response = requests.post(url, headers=headers, json=payload)
    # 检查是否有错误
    if response.status_code != 200:
        raise gr.Error(f"错误：{response.status_code} {response.text}")
    # 获取音频内容
    audio_content = response.content
    # 创建临时文件
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=f".{output_format}")
    with open(temp_file.name, 'wb') as f:
        f.write(audio_content)
    # 返回文件路径
    return temp_file.name

def on_generate_click(input_text_value, voice_value, output_format_value, base_url_value, api_key_value, request: gr.Request):
    audio_path = generate_audio(input_text_value, voice_value, output_format_value, base_url_value, api_key_value, request)
    return audio_path

def update_settings_from_url(request: gr.Request):
    # 获取 URL 参数
    query_params = request.query_params
    base_url = query_params.get("base_url", None)
    api_key = query_params.get("api_key", None)
    base_url_update = gr.update()
    api_key_update = gr.update()
    if base_url is not None:
        base_url_update = gr.update(value=base_url)
    if api_key is not None:
        api_key_update = gr.update(value=api_key)
    return base_url_update, api_key_update

def update_language(language_choice):
    labels = languages[language_choice]
    updates = [
        gr.update(value=f"# {labels['title']}"),  # title_markdown
        gr.update(value=labels['intro']),  # intro_text
        gr.update(label=labels['input_text_label'], placeholder=labels['input_text_placeholder']),  # input_text
        gr.update(label=labels['voice_label']),  # voice
        gr.update(label=labels['output_format_label']),  # output_format
        gr.update(value=labels['generate_button_label']),  # generate_button
        gr.update(label=labels['output_audio_label']),  # audio_output
        gr.update(label=labels['settings_label']),  # settings_accordion
        gr.update(label=labels['base_url_label']),  # base_url_input
        gr.update(label=labels['api_key_label']),  # api_key_input
        gr.update(value=labels['BOW']),  # mode_toggle_btn now uses value instead of label
        gr.update(label=labels['language_label']),  # language_choice_comp
    ]
    return updates

def toggle_dark_mode(current_mode):
    # 切换明亮/黑暗模式
    if current_mode == "light":
        return "dark"
    return "light"

# 获取初始主题和模式（可以从配置文件或其他方式获取）
initial_mode = "light"

# 添加主题设置
with gr.Blocks(css=None, theme="Zarkel/IBM_Carbon_Theme", title="TTS Web") as demo:
    # 使用状态存储当前模式
    mode_state = gr.State(value=initial_mode)

    # 布局
    with gr.Row():
        with gr.Column(scale=3):
            title_markdown = gr.Markdown("# OpenAI TTS Web")
            intro_text = gr.Markdown(languages["中文"]["intro"])  # 初始加载中文的介绍
            # 输入文本
            input_text = gr.Textbox(label="输入文本", placeholder="请输入要合成的文本")
            # 选择声音
            voice = gr.Radio(choices=["Alloy", "Echo", "Fable", "Onyx", "Nova", "Shimmer"], label="声音", value="Alloy")
            # 选择输出格式
            output_format = gr.Radio(choices=["mp3", "opus", "aac", "flac", "pcm"], label="输出格式", value="mp3")
            # 生成按钮
            generate_button = gr.Button("生成")
            # 输出音频
            audio_output = gr.Audio(label="输出音频", type="filepath")
        with gr.Column(scale=1):
            # 设置
            with gr.Accordion("设置", open=True) as settings_accordion:
                # 切换界面模式按钮
                mode_toggle_btn = gr.Button("切换黑白模式")
                # 选择语言
                language_choice_comp = gr.Radio(choices=["中文", "English"], label="界面语言", value="中文")
                # 基础设置
                base_url_input = gr.Textbox(label="Base URL", value="https://api.maktubcn.info")
                api_key_input = gr.Textbox(label="API Key", type="password")

    # 界面加载时更新设置
    demo.load(
        update_settings_from_url,
        inputs=None,
        outputs=[base_url_input, api_key_input]
    )

    # 语言选择事件
    language_choice_comp.change(
        update_language,
        inputs=language_choice_comp,
        outputs=[
            title_markdown,
            intro_text,  # 添加 intro_text 的更新
            input_text,
            voice,
            output_format,
            generate_button,
            audio_output,
            settings_accordion,
            base_url_input,
            api_key_input,
            mode_toggle_btn,
            language_choice_comp,
        ]
    )

    # 切换黑白模式按钮
    mode_toggle_btn.click(
        lambda current_mode: toggle_dark_mode(current_mode),
        inputs=[mode_state],
        outputs=[mode_state],
        js="""
        () => {
            if (document.body.classList.contains('dark')) {
                document.body.classList.remove('dark');
            } else {
                document.body.classList.add('dark');
            }
        }
        """
    )

    # 按钮点击事件
    generate_button.click(
        on_generate_click,
        inputs=[input_text, voice, output_format, base_url_input, api_key_input],
        outputs=[audio_output]
    )

demo.launch(server_name="0.0.0.0", server_port=7860)
