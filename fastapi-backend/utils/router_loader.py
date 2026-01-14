# utils/router_loader.py

import importlib
import pkgutil
from fastapi import APIRouter, FastAPI
from types import ModuleType
from typing import List, Dict


def load_routers_from_module(module_path: str, tag_prefix: str = '') -> List[Dict]:
    """
    自动从指定模块路径加载控制器中定义的路由对象
    :param module_path: 模块路径，如 'module_admin.controller'
    :param tag_prefix: tags 的前缀，如 '系统管理'
    :return: [{'router': ..., 'tags': [...]}, ...]
    """
    router_list = []

    module = importlib.import_module(module_path)
    module_dir = module.__path__

    for _, name, is_pkg in pkgutil.iter_modules(module_dir):
        if not is_pkg:
            full_module_name = f"{module_path}.{name}"
            sub_module: ModuleType = importlib.import_module(full_module_name)
            for attr in dir(sub_module):
                if attr.endswith("Controller") and isinstance(getattr(sub_module, attr), APIRouter):
                    router = getattr(sub_module, attr)
                    tags = [f"{tag_prefix}-{name.replace('_controller', '')}"] if tag_prefix else [name.replace('_controller', '')]
                    router_list.append({'router': router, 'tags': tags})

    return router_list


def register_all_routers(app: FastAPI):
    """
    注册所有模块下的控制器路由
    """
    controller_sources = [
        {'module': 'module_admin.controller', 'tags': '系统管理', 'prefix': '/admin'},
        {'module': 'module_front.controller', 'tags': '前端模块', 'prefix': '/front'},
        {'module': 'module_generator.controller', 'tags': '代码生成', 'prefix': '/admin'},
        #{'module': 'module_task.controller', 'tag_prefix': '系统任务', 'prefix': '/task'},
    ]

    for source in controller_sources:
        router_list = load_routers_from_module(source['module'], source.get('tags', ''))
        for controller in router_list:
            app.include_router(router=controller['router'], tags=controller['tags'], prefix=source.get('prefix', ''))
