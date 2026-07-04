from backend.utils.validation import is_allowed_image


def test_jpg_by_extension():
    assert is_allowed_image("photo.jpg", None) is True


def test_jpeg_mime_type():
    assert is_allowed_image("photo.jpeg", "image/jpeg") is True


def test_png_mime_type():
    assert is_allowed_image("photo.png", "image/png") is True


def test_unsupported_file():
    assert is_allowed_image("document.pdf", "application/pdf") is False
