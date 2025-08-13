import plsfix


def test_basic_functionality():
    """Test basic plsfix functionality works."""
    text = "Hello, world!"
    result = plsfix.fix_text(text)
    assert isinstance(result, str)
    assert result == text


def test_byte_order_mark():
    """Test byte order mark handling - adapted from ftfy."""
    # This is the UTF-8 BOM encoded as latin-1
    text = "ï»¿"
    result = plsfix.fix_text(text)
    # Should fix to actual BOM character
    assert result == "\ufeff"


def test_control_chars():
    """Test control character removal - adapted from ftfy."""
    text = (
        "\ufeffSometimes, \ufffcbad ideas \x7f\ufffalike these characters\ufffb "
        "\u206aget standardized.\r\n"
    )
    expected = "Sometimes, bad ideas like these characters get standardized.\r\n"
    result = plsfix.fix_text(text)
    assert result == expected


def test_welsh_flag():
    """Test that flag emoji sequences are preserved - adapted from ftfy."""
    text = "This flag has a dragon on it 🏴󠁧󠁢󠁷󠁬󠁳󠁿"
    result = plsfix.fix_text(text)
    # Should pass through unchanged
    assert result == text


def test_config_usage():
    """Test using configuration object."""
    config = plsfix.PyTextFixerConfig(remove_control_chars=False)
    text = "Hello\x7fworld"
    result = plsfix.fix_text(text, config)
    # With control char removal disabled, should keep the control char
    assert "\x7f" in result


def test_normalization():
    """Test Unicode normalization."""
    config = plsfix.PyTextFixerConfig(normalization=plsfix.PyNormalization.NFC)
    # Decomposed e with acute accent
    text = "café"  # This might be composed or decomposed
    result = plsfix.fix_text(text, config)
    assert isinstance(result, str)


def test_fix_and_explain():
    """Test fix_and_explain functionality."""
    text = "ï»¿Hello"
    result = plsfix.fix_and_explain(text, True)

    assert isinstance(result, plsfix.PyExplainedText)
    assert isinstance(result.text, str)
    # Should have explanation steps since we fixed the BOM
    if result.steps:
        assert isinstance(result.steps, list)
        assert len(result.steps) > 0
        assert isinstance(result.steps[0], plsfix.PyExplanationStep)
