from password_strength_checker.domain.services.pattern_detector import PatternDetector


def test_detects_repeated_characters() -> None:
    detector = PatternDetector()

    assert detector.find_repeated_characters("AAAbbb123")


def test_detects_sequential_characters() -> None:
    detector = PatternDetector()

    findings = detector.find_sequential_patterns("Safeabc321!")

    assert "abc" in [finding.lower() for finding in findings]
    assert "321" in findings


def test_detects_keyboard_patterns() -> None:
    detector = PatternDetector()

    assert "qwerty" in detector.find_keyboard_patterns("MyQwertyPass12!")


def test_detects_dictionary_words_and_leetspeak() -> None:
    detector = PatternDetector()

    assert "password" in detector.find_dictionary_words("P@ssw0rd2026!")


def test_repeated_character_detection_ignores_pairs() -> None:
    detector = PatternDetector()

    assert detector.find_repeated_characters("AAbb1122") == []


def test_detects_descending_letter_sequences() -> None:
    detector = PatternDetector()

    findings = detector.find_sequential_patterns("zyxSecure!")

    assert "zyx" in findings


def test_sequence_detection_ignores_symbols_between_characters() -> None:
    detector = PatternDetector()

    assert detector.find_sequential_patterns("a-b-c-1-2-3") == []


def test_detects_reversed_keyboard_patterns() -> None:
    detector = PatternDetector()

    assert "qwerty" in detector.find_keyboard_patterns("YTREWQ-safe-2026")


def test_no_dictionary_words_returns_empty_list() -> None:
    detector = PatternDetector()

    assert detector.find_dictionary_words("R4nd0mValue!2026") == []
