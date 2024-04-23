import pytest

from gorigori.source import NihongoKyoshi

H1 = "<h1> HEADING1 </h1>"
H2 = "<h2>例文</h2>"
H2_OTHER = "<h2> HEADING2 OTHER</h2>"
H3 = "<h3> HEADING3 </h3>"
P = "<p>例文です。</p>"
P_ENGLISH = "<p>example english sentence.</p>"
P_TEXT = "例文です。"
DIV_START = "<div>"
DIV_END = "</div>"


@pytest.mark.parametrize(
    "html_lines, expected_output",
    [
        ([H1, H2, P, H2_OTHER], [P_TEXT]),
        (
            [H1, H2, H3, DIV_START, P, DIV_END, H3, DIV_START, P, DIV_END, H2_OTHER],
            [P_TEXT, P_TEXT],
        ),
        ([H1, H2, P_ENGLISH, P], [P_TEXT]),
    ],
    ids=[
        "1 - base case",
        "2 - multiple sections beneath H2 containing target strings",
        "3 - english example should be filtered out",
    ],
)
def test_parse_example_sentences(html_lines, expected_output):
    input_bytes = "\n".join(html_lines).encode()
    actual_output = NihongoKyoshi.parse_example_sentences(input_bytes)
    assert actual_output == expected_output
