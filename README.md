# DiffSynth-ComfyUI

A ComfyUI custom node plugin for the open-source framework [DiffSynth-Studio](https://github.com/modelscope/DiffSynth-Studio). It integrates DiffSynth-Studio's model configuration, quantization, LoRA, and inference pipeline capabilities into [ComfyUI](https://github.com/comfyanonymous/ComfyUI), enabling node-based image, video, and audio generation and editing.

<p align="center">
  <img src="https://github.com/user-attachments/assets/be990357-5b44-4f3b-b646-a80f2f7567d5" alt="DiffSynth-ComfyUI" width="100%">
</p>

## Installation

### Option 1: ComfyUI Registry

**ComfyUI Desktop** / **ComfyUI-Manager**:

- Open the sidebar **Manage Extensions** or **Manager**
- Search for DiffSynth-ComfyUI
- Click Install, then restart ComfyUI

### Option 2: Manual git clone

1. Install ComfyUI

```bash
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI
pip install -r requirements.txt
```

2. Install DiffSynth-Studio

```bash
pip install git+https://github.com/modelscope/DiffSynth-Studio.git
```

3. Install this plugin

```bash
cd custom_nodes
git clone https://github.com/modelscope/DiffSynth-ComfyUI.git
cd ..
python main.py
```


> If you need quantization features, install the quantization extras:
> ```bash
> pip install "diffsynth[quant] @ git+https://github.com/modelscope/DiffSynth-Studio.git"
> ```

Once started, open the ComfyUI address shown in the terminal (typically `http://127.0.0.1:8188`) in your browser.


## Quick Start

### Using Preset Workflows

Open the ComfyUI interface and load a preset using either method:

- **Template:** Click the **Template** tab in the left sidebar and select a DiffSynth template.
- **JSON file:** Choose a workflow from the [Workflow Index](#workflow-index). Use the `.json` file from your local `example_workflows/` directory, or download it from GitHub using **Download raw file** on the file page, then drag it onto the ComfyUI canvas.

Modify parameters such as `prompt` and `seed` in the Inference node, provide any required input images, video, or audio, then click Run.

### Building a Workflow from Scratch

Right-click on a blank canvas to add nodes, then connect them in the following order:

```
VRAMConfig → ModelConfig → MergeModelConfigs ───┐
                                                ├──→ Loader → Inference → SaveImage
                              VRAMLimit ────────┘
```

#### Example: Qwen-Image Text-to-Image

1. Add a VRAM Config node to configure VRAM strategy for each stage (optional)
2. Add 3 ModelConfig nodes with the following settings:
   - `model_id`: `Qwen/Qwen-Image`, `origin_file_pattern`: `transformer/diffusion_pytorch_model*.safetensors`
   - `model_id`: `Qwen/Qwen-Image`, `origin_file_pattern`: `text_encoder/model*.safetensors`
   - `model_id`: `Qwen/Qwen-Image`, `origin_file_pattern`: `vae/diffusion_pytorch_model.safetensors`
3. Connect the VRAM Config output to the `vram_config` input of all 3 ModelConfig nodes
4. Add a Merge ModelConfigs node and connect the outputs of the 3 ModelConfig nodes
5. Add a VRAM Limit node (optional)
6. Add a Qwen Image Loader node and connect `model_configs` and `vram_limit`
7. Add a Qwen Image Inference node and connect the `pipe` output from the Loader
8. Add a built-in SaveImage node and connect the `image` output from the Inference node
9. Fill in the `prompt` in the Inference node and click Run



## Workflow Index

All workflow JSON files are in [example_workflows/](example_workflows/). Both `general_*` and `featured_*` files can be imported using the steps above.

### Image Generation & Editing

| Model | Workflows |
|-------|-----------|
| Anima | [Preview](example_workflows/general_anima_preview.json) |
| Boogu Image | [Base](example_workflows/general_boogu_image_base.json) · [Turbo](example_workflows/general_boogu_image_turbo.json) · [Edit](example_workflows/general_boogu_image_edit.json) |
| ERNIE Image | [Standard](example_workflows/general_ernie_image.json) · [Turbo](example_workflows/general_ernie_image_turbo.json) |
| Fibo 2.0 | [Dev](example_workflows/general_fibo_2.json) |
| FLUX.1 | [Dev](example_workflows/general_flux_flux1_dev.json) · [FLEX.2 Preview](example_workflows/general_flux_flex2_preview.json) |
| FLUX.2 | [Dev](example_workflows/general_flux2_dev.json) · [Klein 4B](example_workflows/general_flux2_klein_4b.json) · [Klein 9B](example_workflows/general_flux2_klein_9b.json) |
| FLUX.3 | [Klein](example_workflows/general_flux3_klein.json) · [EntroPack](example_workflows/general_flux3_entropack.json) |
| HiDream O1 | [Image](example_workflows/general_hidream_o1_image.json) |
| Ideogram 4 | [FP8](example_workflows/general_ideogram4_fp8.json) |
| JoyAI Image | [Edit](example_workflows/general_joyai_image_edit.json) |
| Krea 2 | [Raw](example_workflows/general_krea2_raw.json) · [Turbo](example_workflows/general_krea2_turbo.json) |
| MiniMax H3 Image | [Text-to-Image](example_workflows/general_minimax_h3_image.json) · [Edit](example_workflows/general_minimax_h3_image_edit.json) · [EntroPack](example_workflows/featured_minimax_h3_image_entropack.json) |
| MOSS Image | [Base](example_workflows/general_moss_image_base.json) · [SFT](example_workflows/general_moss_image_sft.json) |
| Qwen Image | [Standard](example_workflows/general_qwen_image.json) · [2512](example_workflows/general_qwen_image_2512.json) · [Edit](example_workflows/general_qwen_image_edit.json) · [Edit 2511 Lightning](example_workflows/featured_qwen_image_edit_2511_lightning.json) |
| Qwen Image 2.1 | [Featured](example_workflows/featured_qwen_image_2_1.json) · [EntroPack](example_workflows/general_qwen_image_2_1_entropack.json) |
| SenseNova U1.5 | [MoT](example_workflows/general_sensenova_u1_5_mot.json) |
| Stable Diffusion | [v1.5](example_workflows/general_stable_diffusion_v1_5.json) · [XL Base 1.0](example_workflows/general_stable_diffusion_xl_base_1_0.json) |
| Z-Image | [Standard](example_workflows/general_z_image.json) · [Turbo](example_workflows/general_z_image_turbo.json) · [Turbo Featured](example_workflows/featured_z_image_turbo.json) · [Turbo EntroPack](example_workflows/general_z_image_turbo_entropack.json) |

### Video & Audio-Video Generation

| Model | Workflows |
|-------|-----------|
| LingBot Video | [Text-to-Video](example_workflows/general_lingbot_video_t2v.json) |
| LTX-2 | [Two-Stage](example_workflows/general_ltx2_t2av_two_stage.json) · [2.3 Two-Stage](example_workflows/general_ltx2_3_t2av_two_stage.json) |
| MiniMax H3 | [FL2VA](example_workflows/general_minimax_h3_fl2va.json) · [FL2VA EntroPack](example_workflows/general_minimax_h3_fl2va_entropack.json) · [Ref2VA](example_workflows/general_minimax_h3_ref2va.json) · [Ref2VA EntroPack](example_workflows/general_minimax_h3_ref2va_entropack.json) · [Pruned NF4](example_workflows/featured_minimax_h3_prund_nf4.json) |
| MOVA | [360P Image-to-Audio-Video](example_workflows/general_mova_360p_i2av.json) |
| Qwen Video Edit | [Video Editing](example_workflows/general_qwen_video_edit.json) |
| Wan Video | [Text-to-Video 1.3B](example_workflows/general_wan_video_t2v_1_3b.json) · [Text-to-Video 14B](example_workflows/general_wan_video_t2v_14b.json) · [Fun A14B Control](example_workflows/general_wan_video_fun_a14b_control.json) |

### Audio Generation

| Model | Workflows |
|-------|-----------|
| ACE-Step 1.5 | [Standard](example_workflows/general_ace_step_1_5.json) · [XL SFT](example_workflows/featured_ace_step_1_5_xl_sft.json) |
| MiniMax Music 3 | [Music Generation](example_workflows/general_minimax_music3.json) |
| YuE2 | [Music Generation](example_workflows/general_yue2.json) |

## Node Reference

All nodes are located under the `DiffSynth` category in the ComfyUI node menu, organized into 4 subcategories:

### DiffSynth/config — Model & VRAM Configuration

| Node | Function |
|------|----------|
| **VRAM Config** | Configures DiffSynth-Studio's four-level VRAM management strategy (offload / onload / preparing / computation), specifying device and data dtype for each stage. Connect the output to the `vram_config` input of ModelConfig nodes. |
| **VRAM Limit** | Limits the available VRAM during inference, reserving `buffer_size` GB for the system. Connect the output to the `vram_limit` input of the Loader. |
| **ModelConfig** | Declares a model file's download source (`model_id`) and file path (`origin_file_pattern`). |
| **Merge ModelConfigs** | Merges multiple ModelConfig nodes into a single list for the Loader's `model_configs` input. |
| **Quantization Config** | Configures the model quantization scheme. `method` selects the quantization method (supports bitsandbytes NF4/FP4, etc.), `mode` selects the quantization mode. Optionally use `target_modules` and `exclude_modules` to control the quantization scope. Connect the output to the `quant_config` input of ModelConfig. |
| **Mixed Quantize Config** | Combines multiple Quantization Configs to apply different quantization strategies to different modules. Outputs a merged quant_config after connecting multiple Quantization Config inputs. |

### DiffSynth/loader — Pipeline Loaders

Each pipeline has a corresponding Loader node that loads model weights, applies VRAM management strategy, and returns a `pipe` object.

Inputs:
- `model_configs` (required): Merged configuration from Merge ModelConfigs
- `torch_dtype`: Model precision
- `device`: Inference device
- `vram_limit` (optional): From a VRAM Limit node
- Other optional parameters: Vary by pipeline

### DiffSynth/inference — Pipeline Inference

Each pipeline has a corresponding Inference node that receives a `pipe` object and performs inference.

Parameters fall into two categories:
- **Widgets**: Parameters such as prompt, seed, num_inference_steps, height, and width that can be edited directly on the node
- **Connection inputs**: Parameters such as input_image and edit_image that are passed in via connections

### DiffSynth/LoRA — LoRA Management

| Node | Function |
|------|----------|
| **LoRA Clear** | Clears all loaded LoRA weights on the pipeline. Usage: connect the `pipe` output from the Loader, then chain to LoRA Load after clearing old weights |
| **LoRA Load** | Loads a LoRA weight to a specified module. `lora_config` connects to a ModelConfig (declaring the LoRA file source), `module` specifies the target module, and `alpha` controls the strength. Multiple LoRA Load nodes can be chained to stack multiple LoRAs: `Loader → LoRA Clear → LoRA Load → LoRA Load → Inference` |
