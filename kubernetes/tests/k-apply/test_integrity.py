import unittest
import os
import subprocess
from typing import List


class TestManifestIntegrity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
        cls.manifest_dir = os.path.join(cls.root_dir, 'manifests')
        cls.manifest_ignore_list = ['service-template.yaml']
        cls.k_apply_script = os.path.join(cls.root_dir, 'k-apply')

    def test_all_manifests(self):
        manifests = self.get_manifests()
        for manifest in manifests:
            patches = self.get_patches(manifest)
            for patch in patches:
                with self.subTest(manifest=manifest, patch=patch):
                    result = self.run_test(manifest, patch)
                    self.assertNotEqual(result, "FAIL", f"Failed: {manifest} with {patch}")

    def get_manifests(self) -> List[str]:
        manifests = []
        for file in os.listdir(self.manifest_dir):
            if file.endswith('.yaml') and file not in self.manifest_ignore_list:
                manifests.append(os.path.join(self.manifest_dir, file))
        return manifests

    def get_patches(self, manifest: str) -> List[str]:
        patches = []
        manifest_base = os.path.basename(manifest).split('-')[0]
        for root, dirs, files in os.walk(self.manifest_dir):
            for file in files:
                if file.endswith(f'-{manifest_base}.yaml'):
                    patches.append(os.path.join(root, file))
        return patches

    def run_test(self, manifest: str, patch_file: str) -> str:
        if not os.path.exists(patch_file):
            print(f"WARN: {patch_file} does not exist")
            return "WARN"

        cmd = ['python3', self.k_apply_script, '-f', manifest, '-p', patch_file, '--dry-run=server', '-v']
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            print(f"PASS: {manifest} with {patch_file}")
            return "PASS"
        else:
            print(f"FAIL: {manifest} with {patch_file}")
            print(f"Error: {result.stderr}")
            return "FAIL"

    def test_summary(self):
        results = {'PASS': 0, 'FAIL': 0, 'WARN': 0}
        manifests = self.get_manifests()
        for manifest in manifests:
            patches = self.get_patches(manifest)
            for patch in patches:
                result = self.run_test(manifest, patch)
                results[result] += 1

        self.print_test_summary(results['PASS'], results['FAIL'], results['WARN'])
        self.assertEqual(results['FAIL'], 0, f"Failed {results['FAIL']} tests")

    def print_test_summary(self, pass_count: int, fail_count: int, warn_count: int):
        total = pass_count + fail_count + warn_count
        print("\n==============================")
        print("         Test Summary         ")
        print("==============================")

        if total == 0:
            print("No tests were run.")
        else:
            pass_percentage = (pass_count * 100) // total
            fail_percentage = (fail_count * 100) // total
            warn_percentage = (warn_count * 100) // total

            print(f"{'Passed:':<10} {pass_count:5d} ({pass_percentage:3d}%)")
            print(f"{'Failed:':<10} {fail_count:5d} ({fail_percentage:3d}%)")
            print(f"{'Warnings:':<10} {warn_count:5d} ({warn_percentage:3d}%)")
            print("------------------------------")
            print(f"{'Total:':<10} {total:5d}")

        print("==============================\n")


if __name__ == '__main__':
    unittest.main(verbosity=2)