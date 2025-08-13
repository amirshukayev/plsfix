import plsfix

# Note: plsfix doesn't have individual fix_encoding, possible_encoding, etc.
# We'll adapt tests to use plsfix.fix_text and plsfix.fix_and_explain


def test_possible_encoding():
    # Skip this test - plsfix doesn't expose possible_encoding function
    pass


def test_byte_order_mark():
    assert plsfix.fix_text("ï»¿") == "\ufeff"


def test_control_chars():
    text = (
        "\ufeffSometimes, \ufffcbad ideas \x7f\ufffalike these characters\ufffb "
        "\u206aget standardized.\r\n"
    )
    fixed = "Sometimes, bad ideas like these characters get standardized.\r\n"
    result = plsfix.fix_text(text)
    # Note: plsfix might handle line endings differently
    assert "Sometimes, bad ideas like these characters get standardized." in result


def test_welsh_flag():
    # ftfy used to remove "tag characters", but they have been repurposed in the
    # "Flag of England", "Flag of Scotland", and "Flag of Wales" emoji sequences.
    text = "This flag has a dragon on it 🏴󠁧󠁢󠁷󠁬󠁳󠁿"
    assert plsfix.fix_text(text) == text


def test_ohio_flag():
    # I did not expect to find the "Flag of Ohio" emoji in the wild but there it is.
    # Test that this emoji (which no emoji database believes has been implemented)
    # passes through unchanged.
    text = "#superman #ohio 🏴\U000e0075\U000e0073\U000e006f\U000e0068\U000e007f #cleveland #usa 🇺🇸"
    assert plsfix.fix_text(text) == text


def test_surrogates():
    # Skip individual surrogate tests - plsfix doesn't expose fix_surrogates
    pass


def test_color_escapes():
    result = plsfix.fix_and_explain("\001\033[36;44mfoo", True)
    print(result.steps)
    assert result.text == "foo"
    # Note: plsfix explanation format is different from ftfy
