import pytest

from pyresume.css_styles import CssStyles
from pyresume.pdf_generator import PdfGenerator
from pyresume.settings import PROJECT_ROOT, OUTPUT_DIR

OUTPUT_DATA_PATH = f"{PROJECT_ROOT}/output/resume*.pdf"


@pytest.fixture(scope="module")
def css_styles():
    return CssStyles()


@pytest.fixture(scope="module")
def pdf_generator():
    return PdfGenerator()


@pytest.fixture
def cleanup_test_output():
    """Clean up generated PDFs after each test"""
    yield
    for pdf in OUTPUT_DIR.glob("*.pdf"):
        pdf.unlink()


class TestGeneratePdfWithStyles:
    """Test PDF generation with different CSS styles"""

    @pytest.mark.parametrize(
        "style_attr,style_name",
        [
            ("default_style", "default"),
            ("simple_style", "simple"),
            ("bar_style", "bar"),
            ("divider_style", "divider"),
        ],
    )
    def test_generate_pdf_with_builtin_style(
        self, css_styles, pdf_generator, cleanup_test_output, style_attr, style_name
    ):
        style = getattr(css_styles, style_attr)
        pdf_generator.generate_pdf(style, pdf_generator.default_resume_path)

        generated_pdfs = list(OUTPUT_DIR.glob("resume*.pdf"))
        assert len(generated_pdfs) > 0, f"No PDF generated with {style_name} style"
        assert generated_pdfs[0].exists()

    def test_generate_pdf_from_custom_style_file(
        self, pdf_generator, cleanup_test_output
    ):
        custom_style = PROJECT_ROOT / "tests" / "data" / "test-style.css"
        pdf_generator.generate_pdf(custom_style, pdf_generator.default_resume_path)

        generated_pdfs = list(OUTPUT_DIR.glob("resume*.pdf"))
        assert len(generated_pdfs) > 0, "No PDF files were generated"
        assert generated_pdfs[0].exists()


class TestGeneratePdfWithCustomInput:
    """Test PDF generation with custom markdown input"""

    def test_generate_pdf_from_custom_markdown_file(
        self, css_styles, pdf_generator, cleanup_test_output
    ):
        input_file = PROJECT_ROOT / "tests" / "data" / "test-markdown-file.md"
        expected_output = OUTPUT_DIR / "test-markdown-file.pdf"

        pdf_generator.generate_pdf(css_styles.divider_style, input_file)

        assert expected_output.exists(), (
            f"Expected PDF not generated at {expected_output}"
        )

    def test_failure_non_markdown_file(self, css_styles, pdf_generator):
        input_file = PROJECT_ROOT / "tests" / "data" / "non-compliant-file.mk"

        with pytest.raises(
            ValueError, match=r"File must be markdown type.*found \.\w+"
        ):
            pdf_generator.generate_pdf(css_styles.divider_style, input_file)


class TestToPdfMainMethod:
    """Test the main to_pdf entry point method"""

    def test_with_custom_css_file(self, pdf_generator, cleanup_test_output):
        css_file = PROJECT_ROOT / "tests" / "data" / "test-style.css"
        pdf_generator.to_pdf(css_file, pdf_generator.default_resume_path)

        generated_pdfs = list(OUTPUT_DIR.glob("resume*.pdf"))
        assert len(generated_pdfs) > 0, "No PDF files were generated"
        assert generated_pdfs[0].exists()

    def test_with_custom_markdown_file(
        self, css_styles, pdf_generator, cleanup_test_output
    ):
        input_file = PROJECT_ROOT / "tests" / "data" / "test-markdown-file.md"
        expected_output = OUTPUT_DIR / "test-markdown-file.pdf"

        pdf_generator.to_pdf(css_styles.divider_style, input_file)

        assert expected_output.exists()

    def test_with_defaults(self, css_styles, pdf_generator, cleanup_test_output):
        pdf_generator.to_pdf(
            css_styles.default_style, pdf_generator.default_resume_path
        )

        generated_pdfs = list(OUTPUT_DIR.glob("resume*.pdf"))
        assert len(generated_pdfs) > 0, "No PDF files were generated"
        assert generated_pdfs[0].exists()


class TestToPdfErrorHandling:
    """Test error handling in to_pdf method"""

    def test_system_exit_when_css_not_found(self, pdf_generator):
        non_existent_css = PROJECT_ROOT / "non-existent-file.css"

        with pytest.raises(SystemExit):
            pdf_generator.to_pdf(non_existent_css, pdf_generator.default_resume_path)

    def test_system_exit_when_markdown_not_found(self, css_styles, pdf_generator):
        non_existent_md = PROJECT_ROOT / "tests" / "data" / "non-existent-file.md"

        with pytest.raises(SystemExit):
            pdf_generator.to_pdf(css_styles.default_style, non_existent_md)

    def test_system_exit_when_file_not_markdown(self, css_styles, pdf_generator):
        invalid_file = PROJECT_ROOT / "tests" / "data" / "non-existent-file.mk"

        with pytest.raises(SystemExit):
            pdf_generator.to_pdf(css_styles.default_style, invalid_file)
