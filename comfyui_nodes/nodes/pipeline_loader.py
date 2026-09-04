import torch
from ..pipeline_registry import PIPELINE_REGISTRY, get_pipeline_class, get_from_pretrained_extra_params
from ..type_defs import MODEL_CONFIG, MODEL_CONFIG_LIST, PIPE, VRAM_LIMIT


def _dtype(name):
    return {"float16": torch.float16, "bfloat16": torch.bfloat16, "float32": torch.float32}[name]


def generate_loader_nodes():
    nodes = {}
    for type_name, meta in PIPELINE_REGISTRY.items():
        extra_params = get_from_pretrained_extra_params(type_name)

        required = {
            "torch_dtype": (["bfloat16", "float16", "float32"], {"default": "bfloat16"}),
            "device": (["cuda", "cpu"], {"default": "cuda"}),
            "model_configs": (MODEL_CONFIG_LIST,),
        }
        optional = {}
        for name, type_str, default in extra_params:
            if type_str == "MODEL_CONFIG":
                optional[name] = (MODEL_CONFIG,)
            elif type_str == "BOOLEAN":
                optional[name] = ("BOOLEAN", {"default": default})
            elif type_str == "FLOAT":
                optional[name] = ("FLOAT", {"default": default, "min": 0.0, "max": 10.0, "step": 0.1})
            else:
                optional[name] = ("STRING", {"default": default})
        optional["vram_limit"] = (VRAM_LIMIT,)

        param_names = [name for name, _, _ in extra_params]

        def execute(self, model_configs, torch_dtype="bfloat16", device="cuda",
                    vram_limit=0.0, _type_name=type_name, _param_names=param_names, **kwargs):
            cls = get_pipeline_class(_type_name)
            call_kwargs = {
                "torch_dtype": _dtype(torch_dtype),
                "device": device,
                "model_configs": model_configs,
                "vram_limit": vram_limit,
            }
            for name in _param_names:
                if name in kwargs and kwargs[name] is not None:
                    call_kwargs[name] = kwargs[name]
            pipe = cls.from_pretrained(**call_kwargs)
            return (pipe,)

        def input_types(cls, _required=required, _optional=optional):
            return {"required": _required, "optional": _optional}

        node_name = f"DiffSynth{type_name}Loader"
        node_class = type(node_name, (), {
            "INPUT_TYPES": classmethod(input_types),
            "RETURN_TYPES": (PIPE,),
            "RETURN_NAMES": ("pipe",),
            "FUNCTION": "execute",
            "CATEGORY": "DiffSynth/loader",
            "execute": execute,
        })
        nodes[node_name] = node_class
    return nodes
