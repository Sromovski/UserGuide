def test_every_theme_display_name_is_correctly_cased():
    # .title() mangles internal capitals: 'CHATGPT ...'.title() -> 'Chatgpt'.
    from fieldguide.theme import THEMES
    expected = {'claude': 'Claude Ai Field Guide Series',
                # 'Ai' (lowercase i) is what .title() has always produced for
                # CLAUDE and is what four live Claude-themed products already
                # ship with — pre-existing and deliberately left alone here.
                'copilot': 'Copilot Field Guide Series',
                'codex': 'Codex Field Guide Series',
                'gpt': 'ChatGPT Field Guide Series'}
    wrong = {k: t.series_display for k, t in THEMES.items()
             if k in expected and t.series_display != expected[k]}
    assert wrong == {}, wrong
