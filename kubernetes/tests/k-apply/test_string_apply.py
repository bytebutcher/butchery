import json
import unittest
import importlib.machinery
import importlib.util
import os

# Load the module
k_apply_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../k-apply'))
loader = importlib.machinery.SourceFileLoader("k_apply", k_apply_path)
spec = importlib.util.spec_from_loader(loader.name, loader)
k_apply = importlib.util.module_from_spec(spec)
spec.loader.exec_module(k_apply)

# Load function under test
patch_yaml_by_string = k_apply.patch_yaml_by_string


class TestStringApply(unittest.TestCase):

    def setUp(self):
        # Base YAML content for testing
        self.base_yaml = {
            "metadata": {
                "labels": {}
            },
            "spec": {
                "replicas": 1,
                "template": {
                    "spec": {
                        "containers": [
                            {
                                "image": "mycontainer",
                                "args": []
                            }
                        ]
                    }
                }
            }
        }

    def test_override_single_value(self):
        patched = patch_yaml_by_string(self.base_yaml, ["spec.replicas=2"])
        self.assertEqual(patched["spec"]["replicas"], 2)

    def test_override_single_list_item(self):
        patched = patch_yaml_by_string(self.base_yaml, ["spec.template.spec.containers[0].image='mycontainer:v2'"])
        self.assertEqual(patched["spec"]["template"]["spec"]["containers"][0]["image"], "mycontainer:v2")

    def test_override_all_list_items(self):
        # First, add another container to test
        self.base_yaml["spec"]["template"]["spec"]["containers"].append(
            {"name": "secondcontainer", "image": "secondcontainer:latest"})
        patched = patch_yaml_by_string(self.base_yaml, ["spec.template.spec.containers[].image='mycontainer:latest'"])
        self.assertEqual(patched["spec"]["template"]["spec"]["containers"][0]["image"], "mycontainer:latest")
        self.assertEqual(patched["spec"]["template"]["spec"]["containers"][1]["image"], "mycontainer:latest")

    def test_increment_integer(self):
        patched = patch_yaml_by_string(self.base_yaml, ["spec.replicas+=2"])
        self.assertEqual(patched["spec"]["replicas"], 3)

    def test_append_string(self):
        patched = patch_yaml_by_string(self.base_yaml, ["spec.template.spec.containers[0].image+=':v2'"])
        self.assertEqual(patched["spec"]["template"]["spec"]["containers"][0]["image"], "mycontainer:v2")

    def test_append_to_list(self):
        patched = patch_yaml_by_string(self.base_yaml, ["spec.template.spec.containers[0].args+=['--verbose']"])
        self.assertEqual(patched["spec"]["template"]["spec"]["containers"][0]["args"], ["--verbose"])


    def test_update_nested_structure(self):
        patched = patch_yaml_by_string(self.base_yaml, ["spec.template.spec.containers[0].image=nginx:latest"])
        self.assertEqual(patched["spec"]["template"]["spec"]["containers"][0]["image"], "nginx:latest")

    def test_add_to_list(self):
        patched = patch_yaml_by_string(self.base_yaml, ["spec.template.spec.containers[0].ports=[{containerPort: 8080}]"])
        self.assertEqual(patched["spec"]["template"]["spec"]["containers"][0]["ports"][0]["containerPort"], 8080)

    def test_multiple_patches(self):
        patched = patch_yaml_by_string(self.base_yaml, [
            "metadata.labels.env=prod",
            "spec.replicas=5"
        ])
        self.assertEqual(patched["metadata"]["labels"]["env"], "prod")
        self.assertEqual(patched["spec"]["replicas"], 5)

    def test_complex_structure_modifications(self):
        self.base_yaml["spec"]["template"]["spec"]["containers"].append({})
        patched = patch_yaml_by_string(self.base_yaml, [
            "spec.template.spec.containers[0].image=nginx:latest",
            "spec.template.spec.containers[1].resources.limits.cpu=500m"
        ])
        self.assertEqual(patched["spec"]["template"]["spec"]["containers"][0]["image"], "nginx:latest")
        self.assertEqual(patched["spec"]["template"]["spec"]["containers"][1]["resources"]["limits"]["cpu"], "500m")

    def test_complex_list_operations(self):
        patched = patch_yaml_by_string(self.base_yaml, [
            "spec.template.spec.containers[0].env=[{name: DEBUG, value: 'true'}]",
            "spec.template.spec.containers[0].ports=[{containerPort: 8080}, {containerPort: 8081}]"
        ])
        self.assertEqual(patched["spec"]["template"]["spec"]["containers"][0]["env"][0]["name"], "DEBUG")
        self.assertEqual(patched["spec"]["template"]["spec"]["containers"][0]["env"][0]["value"], "true")
        self.assertEqual(patched["spec"]["template"]["spec"]["containers"][0]["ports"][0]["containerPort"], 8080)
        self.assertEqual(patched["spec"]["template"]["spec"]["containers"][0]["ports"][1]["containerPort"], 8081)

if __name__ == '__main__':
    unittest.main()