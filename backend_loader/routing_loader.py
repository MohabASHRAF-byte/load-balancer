import importlib

def load_routing_algorithm(name, servers):
    module_name = f"routing.{name.lower().replace('-', '_')}"
    class_name = ''.join(part.capitalize() for part in name.split('-'))
    module = importlib.import_module(module_name)
    routing_class = getattr(module, class_name)
    return routing_class(servers)
