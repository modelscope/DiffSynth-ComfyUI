# DiffSynth-ComfyUI

A ComfyUI custom node plugin for the open-source framework [DiffSynth-Studio](https://github.com/modelscope/DiffSynth-Studio). It integrates DiffSynth-Studio's model configuration, quantization, LoRA, and inference pipeline capabilities into [ComfyUI](https://github.com/comfyanonymous/ComfyUI), enabling node-based image, video, and audio generation and editing.

<p align="center">
  <img src="https://github.com/user-attachments/assets/8a377098-f022-436c-afa6-c26a4646f262" alt="DiffSynth-ComfyUI" width="100%">
</p>

## Installation

### 1. Install ComfyUI

```bash
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI
pip install -r requirements.txt
```

### 2. Install DiffSynth-Studio

```bash
pip install git+https://github.com/modelscope/DiffSynth-Studio.git
```

> If you need quantization features, install the quantization extras:
> ```bash
> pip install "diffsynth[quant] @ git+https://github.com/modelscope/DiffSynth-Studio.git"
> ```

### 3. Install this plugin

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/modelscope/DiffSynth-ComfyUI.git
cd ..
python main.py
```

Once started, open the ComfyUI address shown in the terminal (typically `http://127.0.0.1:8188`) in your browser.


## Quick Start

### Using Preset Workflows

1. Open the ComfyUI interface
2. Click the **Workflow** (templates) tab in the left sidebar
3. Select any DiffSynth template (e.g., `qwen_image`, `wan_video_t2v_14b`, etc.)
4. Modify parameters such as `prompt` and `seed` in the Inference node
5. Click Run

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
