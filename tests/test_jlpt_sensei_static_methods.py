import pytest

from gorigori.source import JLPTSensei

H1 = "<h1> HEADING1 </h1>"
EXAMPLE_CONTAINER_DIV = "<div id=examples >"
EXAMPLE_1_DIV = '<div class="example-cont py-5" id="example_1" >'
EXAMPLE_2_DIV = '<div class="example-cont py-5" id="example_2" >'
P = '<p class="m-0 jp">例文です。</p>'
P_TEXT = "例文です。"
DIV_END = "</div>"


@pytest.mark.parametrize(
    "html_lines, expected_output",
    [
        ([H1, EXAMPLE_CONTAINER_DIV, EXAMPLE_1_DIV, P, DIV_END, DIV_END], [P_TEXT]),
    ],
    ids=[
        "1 - base case",
    ],
)
def test_parse_example_sentences(html_lines, expected_output):
    input_bytes = "\n".join(html_lines).encode()
    actual_output = JLPTSensei.parse_example_sentences(input_bytes)
    assert actual_output == expected_output
