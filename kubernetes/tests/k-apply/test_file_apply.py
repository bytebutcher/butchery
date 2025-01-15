import unittest
import importlib.machinery
import importlib.util
import os
import yaml

# Load the module
k_apply_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../k-apply'))
loader = importlib.machinery.SourceFileLoader("k_apply", k_apply_path)
spec = importlib.util.spec_from_loader(loader.name, loader)
k_apply = importlib.util.module_from_spec(spec)
spec.loader.exec_module(k_apply)

# Load functions under test
patch_yaml_by_file = k_apply.patch_yaml_by_file


class TestFileApply(unittest.TestCase):
    def setUp(self):
        # Load test data
        self.data_dir = os.path.join(os.path.dirname(__file__), 'data')

        with open(os.path.join(self.data_dir, 'base.yaml'), 'r') as f:
            self.base_yaml = yaml.safe_load(f)

        with open(os.path.join(self.data_dir, 'patch.yaml'), 'r') as f:
            self.patch_yaml = yaml.safe_load(f)

    def test_simple_patch(self):
        result = patch_yaml_by_file(self.base_yaml, self.patch_yaml)
        expected = {
            'apiVersion': 'v1',
            'kind': 'Pod',
            'metadata': {'name': 'test-pod'},
            'spec': {
                'containers': [
                    {'name': 'container1', 'image': 'nginx:latest'},
                    {'name': 'container2', 'image': 'redis:latest'}
                ]
            }
        }
        self.assertEqual(result, expected)

    def test_nested_patch(self):
        base = {
            'level1': {
                'level2': {
                    'key': 'old_value'
                }
            }
        }
        patch = {
            'level1': {
                'level2': {
                    'key': 'new_value'
                }
            }
        }
        result = patch_yaml_by_file(base, patch)
        expected = {
            'level1': {
                'level2': {
                    'key': 'new_value'
                }
            }
        }
        self.assertEqual(result, expected)

    def test_array_patch(self):
        base = {
            'items': ['item1', 'item2']
        }
        patch = {
            'items': ['item3', 'item4']
        }
        result = patch_yaml_by_file(base, patch)
        expected = {
            'items': ['item3', 'item4']
        }
        self.assertEqual(result, expected)

    def test_container_patch(self):
        base = {
            'spec': {
                'containers': [
                    {'name': 'container1', 'image': 'ubuntu:latest'}
                ]
            }
        }
        patch = {
            'spec': {
                'containers': [
                    {'name': 'container1', 'image': 'nginx:latest'},
                    {'name': 'container2', 'image': 'redis:latest'}
                ]
            }
        }
        result = patch_yaml_by_file(base, patch)
        expected = {
            'spec': {
                'containers': [
                    {'name': 'container1', 'image': 'nginx:latest'},
                    {'name': 'container2', 'image': 'redis:latest'}
                ]
            }
        }
        self.assertEqual(result, expected)

    def test_empty_patch(self):
        base = {'key': 'value'}
        patch = {}
        result = patch_yaml_by_file(base, patch)
        self.assertEqual(result, base)

    def test_invalid_patch(self):
        base = {'key': 'value'}
        patch = {'invalid': {'nested': 'structure'}}
        result = patch_yaml_by_file(base, patch)
        expected = {'key': 'value', 'invalid': {'nested': 'structure'}}
        self.assertEqual(result, expected)

    def test_patch_with_null(self):
        base = {'key': 'value'}
        patch = {'key': None}
        result = patch_yaml_by_file(base, patch)
        expected = {'key': None}
        self.assertEqual(result, expected)

    def test_deep_nested_patch(self):
        base = {'l1': {'l2': {'l3': {'l4': 'old'}}}}
        patch = {'l1': {'l2': {'l3': {'l4': 'new'}}}}
        result = patch_yaml_by_file(base, patch)
        expected = {'l1': {'l2': {'l3': {'l4': 'new'}}}}
        self.assertEqual(result, expected)

    def test_patch_array_base(self):
        base = ['item1', 'item2']
        patch = {'1': 'new_item2'}
        result = patch_yaml_by_file(base, patch)
        expected = ['item1', 'new_item2']
        self.assertEqual(result, expected)

    def test_list_append_with_index(self):
        base = {'list': [1, 2, 3]}
        patch = {'list': {'3': 'four'}}
        result = patch_yaml_by_file(base, patch)
        expected = {'list': [1, 2, 3, 'four']}
        self.assertEqual(result, expected)

    def test_list_append_without_index(self):
        base = {'list': [1, 2, 3]}
        patch = {'list': {'+': 'four'}}
        result = patch_yaml_by_file(base, patch)
        expected = {'list': [1, 2, 3, 'four']}
        self.assertEqual(result, expected)

    def test_list_append_multiple(self):
        base = {'list': [1, 2, 3]}
        patch = {'list': {'+': ['four', 'five']}}
        result = patch_yaml_by_file(base, patch)
        expected = {'list': [1, 2, 3, 'four', 'five']}
        self.assertEqual(result, expected)

    def test_list_mixed_operations(self):
        base = {'list': [1, 2, 3]}
        patch = {'list': {'1': 'two', '+': ['four', 'five'], '3': 'three'}}
        result = patch_yaml_by_file(base, patch)
        expected = {'list': [1, 'two', 3, 'three', 'four', 'five']}
        self.assertEqual(result, expected)

    def test_special_characters_in_keys(self):
        base = {'normal': 'value'}
        patch = {'key with spaces': 'value', 'key.with.dots': 'value', 'key-with-dashes': 'value'}
        result = patch_yaml_by_file(base, patch)
        expected = {
            'normal': 'value',
            'key with spaces': 'value',
            'key.with.dots': 'value',
            'key-with-dashes': 'value'
        }
        self.assertEqual(result, expected)

    def test_large_patch(self):
        base = {'key': 'value'}
        large_patch = {f'key{i}': f'value{i}' for i in range(1000)}
        result = patch_yaml_by_file(base, large_patch)
        self.assertEqual(len(result), 1001)  # 1000 new keys + 1 original key

    def test_conflicting_patches(self):
        base = {'key': {'nested': 'old'}}
        patch = {'key': 'new'}
        result = patch_yaml_by_file(base, patch)
        expected = {'key': 'new'}
        self.assertEqual(result, expected)

    def test_empty_string_patch(self):
        base = {'key': 'value'}
        patch = {'key': ''}
        result = patch_yaml_by_file(base, patch)
        expected = {'key': ''}
        self.assertEqual(result, expected)

    def test_boolean_patch(self):
        base = {'key': 'value'}
        patch = {'key': True}
        result = patch_yaml_by_file(base, patch)
        expected = {'key': True}
        self.assertEqual(result, expected)

    def test_numeric_patch(self):
        base = {'int': 'string', 'float': 'string'}
        patch = {'int': 42, 'float': 3.14}
        result = patch_yaml_by_file(base, patch)
        expected = {'int': 42, 'float': 3.14}
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()