import logging

from .nodes import (VRAMConfigNode, QuantizationConfigNode, MixedQuantizeConfigNode,
                    ModelConfigNode, VRAMLimitNode, MergeModelConfigsNode, generate_loader_nodes,
                    LoRAClearNode, LoRALoadNode, generate_inference_nodes)
from .pipeline_registry import PIPELINE_REGISTRY

NODE_CLASS_MAPPINGS = {
    "DiffSynthVRAMConfig": VRAMConfigNode,
    "DiffSynthQuantizationConfig": QuantizationConfigNode,
    "DiffSynthMixedQuantizeConfig": MixedQuantizeConfigNode,
    "DiffSynthModelConfig": ModelConfigNode,
    "DiffSynthVRAMLimit": VRAMLimitNode,
    "DiffSynthMergeModelConfigs": MergeModelConfigsNode,
    "DiffSynthLoRAClear": LoRAClearNode,
    "DiffSynthLoRALoad": LoRALoadNode,
}

for type_name, meta in PIPELINE_REGISTRY.items():
    for suffix, generate_nodes in (("Loader", generate_loader_nodes), ("Inference", generate_inference_nodes)):
        try:
            NODE_CLASS_MAPPINGS.update(generate_nodes({type_name: meta}))
        except Exception as e:
            logging.getLogger(__name__).warning(
                "[DiffSynth-ComfyUI] Skipping DiffSynth%s%s (%s): %s: %s",
                type_name, suffix, meta.pipeline_class_path, type(e).__name__, e,
                exc_info=True,
            )

NODE_DISPLAY_NAME_MAPPINGS = {
    "DiffSynthVRAMConfig": "DiffSynth: VRAM Config",
    "DiffSynthQuantizationConfig": "DiffSynth: Quantization Config",
    "DiffSynthMixedQuantizeConfig": "DiffSynth: Mixed Quantize Config",
    "DiffSynthModelConfig": "DiffSynth: ModelConfig",
    "DiffSynthVRAMLimit": "DiffSynth: VRAM Limit",
    "DiffSynthMergeModelConfigs": "DiffSynth: Merge ModelConfigs",
    "DiffSynthLoRAClear": "DiffSynth: LoRA Clear",
    "DiffSynthLoRALoad": "DiffSynth: LoRA Load",
}
for type_name, meta in PIPELINE_REGISTRY.items():
    for suffix in ("Loader", "Inference"):
        node_name = f"DiffSynth{type_name}{suffix}"
        if node_name in NODE_CLASS_MAPPINGS:
            NODE_DISPLAY_NAME_MAPPINGS[node_name] = f"DiffSynth: {meta.display_name} {suffix}"

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
