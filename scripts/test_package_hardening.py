"""Deterministic package regressions, not tests of target-model behavior."""
from __future__ import annotations

import io
import json
import struct
import zlib
import os
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

# Allows an isolated red run against a prior source snapshot.
sys.path.insert(0, os.environ.get("SERVOTAB_TEST_SCRIPTS", str(Path(__file__).parent)))
from build_skills import check, write
from runtime_validate import load_json_object, load_pack_manifest, validate_marketplace, validate_package, validate_plugin_manifest
from selftest import contract_copy
from validate import load_yaml, validate_icon_asset
from PIL import Image

ROOT = Path(os.environ.get("SERVOTAB_TEST_ROOT", str(Path(__file__).resolve().parents[1])))
SVG = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"{attrs}>{body}</svg>'


class AssetTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "asset"

    def svg(self, text):
        self.path.write_text(text, encoding="utf-8")
        return validate_icon_asset(self.path, field="icon_large")

    def test_all_shipped_icons_pass(self):
        for folder in (ROOT / 'plugins/servotab/skills').iterdir():
            with self.subTest(skill=folder.name):
                self.assertEqual(validate_icon_asset(folder/'assets/icon.svg', field='icon_large'), [])
                self.assertEqual(validate_icon_asset(folder/'assets/icon-400.png', field='icon_small'), [])

    def test_malformed_xml(self):
        self.assertTrue(self.svg('<svg viewBox="0 0 48 48"><g>'))

    def test_comment_cannot_supply_root(self):
        self.assertTrue(self.svg('<!-- <svg viewBox="0 0 48 48"> --><html/>'))

    def test_nested_element_cannot_supply_viewbox(self):
        self.assertTrue(self.svg('<svg xmlns="http://www.w3.org/2000/svg"><g viewBox="0 0 48 48"/></svg>'))

    def test_nonfinite_viewbox(self):
        for value in ('NaN', 'Infinity', '-Infinity', '1e999'):
            with self.subTest(value=value):
                self.assertTrue(self.svg(SVG.format(attrs='',body='').replace('48 48',f'{value} {value}')))

    def test_undersized_viewbox_even_with_large_dimensions(self):
        self.assertTrue(self.svg(SVG.format(attrs=' width="48" height="48"',body='').replace('0 0 48 48','0 0 32 32')))

    def test_invalid_explicit_dimensions(self):
        for value in ('-1', 'NaN', '1e999', '32px', '100%', 'auto', ''):
            with self.subTest(value=value):
                self.assertTrue(self.svg(SVG.format(attrs=f' width="{value}"',body='')))

    def test_valid_svg_numbers(self):
        self.assertEqual(self.svg(SVG.format(attrs=' width="4.8e1px" height="48"',body='').replace('0 0 48 48','0,0,48,48')), [])

    def test_event_attributes(self):
        for name in ('onload','onpointerover','ONLOAD'):
            with self.subTest(name=name):
                self.assertTrue(self.svg(SVG.format(attrs=f' {name}="test()"',body='')))

    def test_resource_attributes_and_elements(self):
        for body in ('<g href = "https://example.invalid/a"/>', '<style>rect{fill:red}</style>', '<script/>', '<foreignObject/>', '<animate/>'):
            with self.subTest(body=body):
                self.assertTrue(self.svg(SVG.format(attrs='',body=body)))

    def test_encoded_paint_resource(self):
        self.assertTrue(self.svg(SVG.format(attrs='',body='<rect fill="&#117;rl(https://example.invalid/a)"/>')))

    def test_doctype_and_processing_instruction(self):
        for prefix in ('<!DOCTYPE svg []>', '<?xml-stylesheet href="https://example.invalid/a"?>'):
            self.assertTrue(self.svg(prefix+SVG.format(attrs='',body='')))

    def test_truncated_png(self):
        data = (ROOT/'plugins/servotab/skills/design/assets/icon-400.png').read_bytes()
        for count in (26, 33, len(data)-1, len(data)-12):
            self.path.write_bytes(data[:count])
            self.assertTrue(validate_icon_asset(self.path,field='icon_small'))

    def test_png_bad_crc(self):
        data=bytearray((ROOT/'plugins/servotab/skills/design/assets/icon-400.png').read_bytes())
        data[29] ^= 1
        self.path.write_bytes(data)
        self.assertTrue(validate_icon_asset(self.path,field='icon_small'))

    def test_png_wrong_size_and_mode(self):
        for size,mode in (((399,400),'RGBA'),((400,400),'RGB')):
            Image.new(mode,size).save(self.path,format='PNG')
            self.assertTrue(validate_icon_asset(self.path,field='icon_small'))

    def test_png_16bit_rejected_before_conversion(self):
        def chunk(kind, data):
            return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data))
        data = b"\x89PNG\r\n\x1a\n"
        data += chunk(b"IHDR", struct.pack(">IIBBBBB", 400, 400, 16, 6, 0, 0, 0))
        data += chunk(b"IDAT", zlib.compress((b"\0" + b"\0" * 3200) * 400))
        data += chunk(b"IEND", b"")
        self.path.write_bytes(data)
        self.assertTrue(validate_icon_asset(self.path, field="icon_small"))

    def test_invalid_literal_paint(self):
        for paint in ("#12345", "#1234567"):
            self.assertTrue(self.svg(SVG.format(attrs="", body=f'<rect fill="{paint}"/>')))

    def test_png_trailing_payload(self):
        data=(ROOT/'plugins/servotab/skills/design/assets/icon-400.png').read_bytes()
        self.path.write_bytes(data+b'unexpected')
        self.assertTrue(validate_icon_asset(self.path,field='icon_small'))


class ContractTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root=contract_copy(ROOT,Path(self.temp.name)/'repo')

    def test_duplicate_yaml_key(self):
        with self.assertRaises(ValueError):
            load_yaml('policy:\n  allow_implicit_invocation: false\n  allow_implicit_invocation: true\n','policy')

    def test_duplicate_json_key(self):
        path=self.root/'duplicate.json';path.write_text('{"name":"x","name":"y"}')
        with self.assertRaises(ValueError):
            load_json_object(path,'test')

    def test_nonfinite_json(self):
        path=self.root/'invalid.json'
        for value in ('NaN', 'Infinity', '1e999'):
            path.write_text('{"number": ' + value + '}')
            with self.assertRaises(ValueError):
                load_json_object(path,'test')

    def test_manifest_bad_digest(self):
        path=self.root/'PACK_MANIFEST.json';data=json.loads(path.read_text());data['files'][0]['sha256']='g'*64;path.write_text(json.dumps(data))
        with self.assertRaises(ValueError):
            load_pack_manifest(path)

    def test_manifest_boolean_size(self):
        path=self.root/'PACK_MANIFEST.json';data=json.loads(path.read_text());data['files'][0]['size']=True;path.write_text(json.dumps(data))
        with self.assertRaises(ValueError):
            load_pack_manifest(path)

    def test_unowned_package_file(self):
        (self.root/'plugins/servotab/unowned.txt').write_text('unowned')
        self.assertTrue(validate_package(self.root))

    def test_unowned_empty_directory(self):
        (self.root/'plugins/servotab/hooks').mkdir()
        self.assertTrue(validate_package(self.root))

    def test_symlinked_parent(self):
        path=self.root/'plugins/servotab/skills/design'
        outside=Path(self.temp.name)/'outside';shutil.move(str(path),str(outside));path.symlink_to(outside,target_is_directory=True)
        self.assertTrue(validate_package(self.root))
        self.assertTrue(check(self.root))

    def test_generator_preserves_unowned_content(self):
        extra=self.root/'plugins/servotab/assets/unowned'
        extra.mkdir();(extra/'keep.txt').write_text('keep')
        target=self.root/'plugins/servotab/skills/design/SKILL.md'
        before=target.read_bytes()
        with self.assertRaises(ValueError):
            write(self.root)
        self.assertEqual((extra/'keep.txt').read_text(),'keep')
        self.assertEqual(target.read_bytes(),before)

    def test_generator_no_mutation_on_symlink(self):
        path=self.root/'plugins/servotab/skills/design/SKILL.md'
        outside=Path(self.temp.name)/'keep.txt';outside.write_text('keep')
        path.unlink();path.symlink_to(outside)
        with self.assertRaises(ValueError):
            write(self.root)
        self.assertEqual(outside.read_text(),'keep')

    def test_non_skill_manifest_extension(self):
        path=self.root/'plugins/servotab/.codex-plugin/plugin.json'
        data=json.loads(path.read_text());data['mcpServers']={};path.write_text(json.dumps(data))
        self.assertTrue(validate_plugin_manifest(self.root))

    def test_marketplace_identity(self):
        path=self.root/'.agents/plugins/marketplace.json'
        data=json.loads(path.read_text());data['name']='other';path.write_text(json.dumps(data))
        self.assertTrue(validate_marketplace(self.root))


if __name__ == '__main__':
    unittest.main()
