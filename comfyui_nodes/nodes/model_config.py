import json
from ..type_defs import MODEL_CONFIG, VRAM_CONFIG, QUANT_CONFIG, MODEL_CONFIG_LIST


def _register_sidecar(model_config, download_source):
    from diffsynth.configs import MODEL_CONFIGS
    from diffsynth.core import ModelConfig
    pattern = model_config.origin_file_pattern
    if not isinstance(pattern, str) or not pattern.endswith(".safetensors"):
        raise ValueError(f"`register_sidecar` needs `origin_file_pattern` to point at a .safetensors package, got {pattern!r}.")
    kwargs = {"model_id": model_config.model_id,
              "origin_file_pattern": pattern[: -len(".safetensors")] + ".json"}
    if download_source:
        kwargs["download_source"] = download_source
    sidecar = ModelConfig(**kwargs)
    sidecar.download_if_necessary()
    with open(sidecar.path) as handle:
        entry = json.load(handle)
    if any(config.get("model_hash") == entry.get("model_hash") for config in MODEL_CONFIGS):
        return
    MODEL_CONFIGS.append(entry)


class ModelConfigNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {
            "model_id": ("STRING", {"default": ""}),
            "origin_file_pattern": ("STRING", {"default": ""}),
        }, "optional": {
            "vram_config": (VRAM_CONFIG,),
            "quant_config": (QUANT_CONFIG,),
            "path": ("STRING", {"default": ""}),
            "download_source": (["modelscope", "huggingface"], {"default": "modelscope"}),
            "register_sidecar": ("BOOLEAN", {"default": False}),
        }}

    RETURN_TYPES = (MODEL_CONFIG,)
    RETURN_NAMES = ("model_config",)
    FUNCTION = "execute"
    CATEGORY = "DiffSynth/config"

    def execute(self, model_id, origin_file_pattern, vram_config=None, quant_config=None,
                path="", download_source="modelscope", register_sidecar=False):
        from diffsynth.core import ModelConfig
        kwargs = {}
        if vram_config:
            kwargs.update(vram_config)
        if quant_config is not None:
            kwargs["quantize"] = quant_config
        if path and path.strip():
            kwargs["path"] = path.strip()
        if download_source:
            kwargs["download_source"] = download_source
        model_config = ModelConfig(model_id=model_id.strip() or None, origin_file_pattern=origin_file_pattern.strip() or None, **kwargs)
        model_config.download_if_necessary()
        if register_sidecar:
            _register_sidecar(model_config, download_source)
        return (model_config,)


class MergeModelConfigsNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"model_config_1": (MODEL_CONFIG,)},
                "optional": {f"model_config_{i}": (MODEL_CONFIG,) for i in range(2, 9)}}

    RETURN_TYPES = (MODEL_CONFIG_LIST,)
    RETURN_NAMES = ("model_configs",)
    FUNCTION = "execute"
    CATEGORY = "DiffSynth/config"

    def execute(self, model_config_1, **kwargs):
        return ([model_config_1] + [kwargs[name] for name in sorted(kwargs) if kwargs[name] is not None],)
