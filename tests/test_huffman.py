import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from Node import Node, creationarbre
import Main


def test_is_leaf():
    leaf = Node(1, 'a')
    assert leaf.is_leaf() is True
    parent = Node(2, left_child=leaf, right_child=Node(1, 'b'))
    assert parent.is_leaf() is False


def test_parcours_profondeur():
    left = Node(1, 'a')
    right = Node(1, 'b')
    root = Node(2, left_child=left, right_child=right)
    codes = root.parcours_profondeur()
    result = {label: code for label, _, code in codes}
    assert result['a'] == [0]
    assert result['b'] == [1]


def test_compress_decompress(tmp_path):
    text_file = tmp_path / 'sample.txt'
    text_file.write_text('ababa')
    Main.compress(str(text_file))
    Main.decompress(str(text_file))

    output_file = tmp_path / 'sample_decomp.txt'
    assert output_file.read_text() == 'ababa'

    # ensure intermediate files were created
    assert (tmp_path / 'sample_comp.bin').exists()
    assert (tmp_path / 'sample_freq.txt').exists()
