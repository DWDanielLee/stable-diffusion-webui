# hires_fix_presets.py
#
# AUTOMATIC1111 Stable Diffusion WebUI용
# Hires.fix 프리셋 스크립트 (run() 기반 버전)
#
# 사용법:
# 1. 이 파일을 stable-diffusion-webui/scripts/ 폴더에 넣고 WebUI 재시작
# 2. txt2img 우측 아래 "Script" 드롭다운에서 "Hires Fix Presets" 선택
# 3. 원하는 프리셋 선택 후 Generate 누르면, 해당 프리셋으로 Hires.fix 자동 세팅

import gradio as gr
from modules import scripts, processing

# 여기서 프리셋들을 설정합니다.
# 필요하면 값/프리셋 이름을 자유롭게 바꿔도 됩니다.
HIRES_PRESETS = {
    "Z Flip4 (1080 x 2640)": {
        "hr_resize_x": 1080,
        "hr_resize_y": 2640,
        "hr_second_pass_steps": 10,
        "hr_denoising_strength": 0.4,
        # 네가 자주 쓰는 업스케일러 이름으로 바꿔도 됨
        # "hr_upscaler": "R-ESRGAN 4x+ Anime6B",
        "hr_upscaler": "Latent (bicubic)",
    },
    "iPhone 15 Pro Max (1290 x 2796)": {
        "hr_resize_x": 1290,
        "hr_resize_y": 2796,
        "hr_second_pass_steps": 10,
        "hr_denoising_strength": 0.4,
        "hr_upscaler": "R-ESRGAN 4x+ Anime6B",
    },
    "Desktop FHD (1920 x 1080)": {
        "hr_resize_x": 1920,
        "hr_resize_y": 1080,
        "hr_second_pass_steps": 10,
        "hr_denoising_strength": 0.4,
        "hr_upscaler": "R-ESRGAN 4x+ Anime6B",
    },
    "Instagram Square (1024 x 1024)": {
        "hr_resize_x": 1024,
        "hr_resize_y": 1024,
        "hr_second_pass_steps": 10,
        "hr_denoising_strength": 0.4,
        "hr_upscaler": "R-ESRGAN 4x+ Anime6B",
    },
    "Portrait 9:16 (1080 x 1920)": {
        "hr_resize_x": 1080,
        "hr_resize_y": 1920,
        "hr_second_pass_steps": 10,
        "hr_denoising_strength": 0.4,
        "hr_upscaler": "R-ESRGAN 4x+ Anime6B",
    },
}


class Script(scripts.Script):
    def title(self):
        # Scripts 드롭다운에 표시될 이름
        return "Hires Fix Presets"

    # txt2img에만 표시, img2img에서는 숨김
    def show(self, is_img2img):
        return not is_img2img

    # UI 정의
    def ui(self, is_img2img):
        with gr.Group():
            gr.Markdown(
                "### Hires Fix Presets\n"
                "프리셋을 선택하면 Generate 시 자동으로 Hires.fix 설정이 적용됩니다.\n"
                "※ 기본 해상도(예: 512x768)는 직접 설정하고,\n"
                "   여기서는 최종 해상도 / Hires 값만 바꿉니다."
            )

            preset_names = list(HIRES_PRESETS.keys())

            preset = gr.Radio(
                choices=preset_names,
                value=preset_names[0] if preset_names else None,
                label="선택할 프리셋",
            )

            enable = gr.Checkbox(
                value=True,
                label="이 프리셋을 사용하여 Hires.fix 자동 설정하기",
            )

        # 이 순서대로 run(p, preset, enable) 인자로 들어감
        return [preset, enable]

    # 실제 이미지를 생성하는 부분
    def run(self, p, preset_name, enable_preset):
        # 프리셋 사용 안 함 체크면 그냥 일반 생성
        if not enable_preset:
            return processing.process_images(p)

        preset = HIRES_PRESETS.get(preset_name)
        if not preset:
            print(f"[Hires Fix Presets] 알 수 없는 프리셋: {preset_name}")
            return processing.process_images(p)

        # ===== 여기서 Hires.fix 설정 강제 적용 =====
        p.enable_hr = True

        p.hr_resize_x = preset.get("hr_resize_x", 0)
        p.hr_resize_y = preset.get("hr_resize_y", 0)
        p.hr_second_pass_steps = preset.get("hr_second_pass_steps", 10)
        p.hr_denoising_strength = preset.get("hr_denoising_strength", 0.4)
        p.hr_upscaler = preset.get("hr_upscaler", "Latent (bicubic)")

        # scale은 0으로 두고, resize_x/resize_y를 기준으로 동작하게 함
        p.hr_scale = 0

        print("[Hires Fix Presets] 적용된 프리셋:", preset_name)
        print(f"  enable_hr = {p.enable_hr}")
        print(f"  hr_resize_x = {p.hr_resize_x}")
        print(f"  hr_resize_y = {p.hr_resize_y}")
        print(f"  hr_second_pass_steps = {p.hr_second_pass_steps}")
        print(f"  hr_denoising_strength = {p.hr_denoising_strength}")
        print(f"  hr_upscaler = {p.hr_upscaler}")

        # 실제 이미지 생성
        return processing.process_images(p)
