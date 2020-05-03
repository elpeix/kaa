
import ast
import importlib
import inspect

import definitions


class OpenApi:

    def generate(self, kaa):
        elements = []

        for module_name in kaa.resources:
            for class_name in kaa.resources[module_name]:
                elements.append(self.__fn(module_name, class_name))

        result = {
            'openapi': '3.0.3',
            'info': {
                'title': definitions.NAME,
                'version': definitions.VERSION
            },
            'paths': self.__get_paths(elements),
            # 'components': {
            #     'schemas': {
            #         'Default': {}
            #     }
            # }

        }
        return result

    def __get_paths(self, elements):
        paths = {}
        for element in elements:
            for k in element:
                r = element[k]
                parameters = []

                if 'path_params' in r:
                    parameters += (self.__path_params(r['path_params']))
                if 'query_params' in r:
                    parameters += (self.__query_params(r['query_params']))

                paths[r['url']] = {
                    r['method'].lower(): {
                        'operationId': k,
                        'parameters': parameters,
                        'description': r['description'] if 'description' in r else '',
                        'responses': {
                            '200': {
                                'description': 'Response description',
                                'content': {'application/json':{}},
                                # '$ref': '#/components/schemas/Default'
                            }
                        }
                    }
                }
        return paths

    def __fn(self, module_name, class_name):
        module = importlib.import_module(module_name)
        class_ = getattr(module, class_name)
        return get_decorators(class_)

    def __path_params(self, parameters):
        pm = []
        for k in parameters:
            parameter = parameters[k]
            p = {
                'name': k,
                'description': parameter['description'] if 'description' in parameter else '',
                'in': 'path',
                'schema': {
                    'type': self.__get_type(parameter['type']) if 'type' in parameter else 'string'
                },
                'required': True,
            }
            pm.append(p)
        return pm

    def __query_params(self, parameters):
        pm = []
        for k in parameters:
            parameter = parameters[k]
            p = {
                'name': k,
                'description': parameter['description'] if 'description' in parameter else '',
                'in': 'query',
                'schema': {
                    'type': self.__get_type(parameter['type']) if 'type' in parameter else 'string'
                },
                # 'default': parameter['default'] if 'default' in parameter else '',
                'required': parameter['required'] if 'required' in parameter else False,
            }
            pm.append(p)
        return pm

    def __get_type(self, param_type):
        if param_type == 'int':
            return 'integer'
        elif param_type == 'float':
            return 'number'
        return 'string'


def get_decorators(cls):
    AVAILABLE_METHODS = ['GET', 'PUT', 'POST', 'DELETE']
    PATH = 'PATH'
    AUTH = 'AUTH'
    target = cls
    decorators = {}

    def visit_FunctionDef(node):
        if node.name[:2] == "__":
            return
        decorators[node.name] = {}
        for n in node.decorator_list:
            if isinstance(n, ast.Call):
                name = n.func.attr if isinstance(n.func, ast.Attribute) else n.func.id
                if name == PATH:
                    decorators[node.name].update(parse_path(n))
                elif name == AUTH:
                    decorators[node.name]['authorization'] = True
            else:
                name = n.attr if isinstance(n, ast.Attribute) else n.id
                if name in AVAILABLE_METHODS:
                    decorators[node.name]['method'] = name

    node_iter = ast.NodeVisitor()
    node_iter.visit_FunctionDef = visit_FunctionDef
    node_iter.visit(ast.parse(inspect.getsource(target)))
    return decorators


def parse_path(node):
    res = {}

    def _parse(node):
        if isinstance(node, ast.AST):
            fields = [(a, b) for a, b in ast.iter_fields(node)]
            for field in fields:
                if field[0] == 'args':
                    res.update(_parse_args(field[1]))
                elif field[0] == 'keywords':
                    res.update(_parse_kw(field[1]))
                elif isinstance(field[1], ast.AST):
                    _parse(field[1])

    def _parse_args(node):
        if not isinstance(node, list):
            return {}
        args = {}
        count = 0
        for arg in node:
            count += 1
            if count == 1:
                args['url'] = [b for a, b in ast.iter_fields(arg)][0]
            if count == 2:
                args['query_params'] = _parse_dict(arg)
        return args

    def _parse_kw(node):
        args = {}
        for arg in node:
            a = [b for a, b in ast.iter_fields(arg)]
            args[a[0]] = _parse_dict(a[1])
        return args

    def _parse_dict(node):
        params = []
        values = []
        for a, b in ast.iter_fields(node):
            if a == 'keys':
                for k in b:
                    params += [d for c, d in ast.iter_fields(k)]
            elif a == 'values':
                for k in b:
                    flds = [d for c, d in ast.iter_fields(k)]
                    if len(flds) == 1:
                        values.append(flds[0])
                        continue
                    values.append(_parse_dict(k))
            else:
                return b
        c = 0
        result = {}
        for param in params:
            result[param] = values[c]
            c += 1
        return result

    _parse(node)
    return res
