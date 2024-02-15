import pathlib
from fastapi.templating import Jinja2Templates
from weasyprint import HTML

BASE_DIR = pathlib.Path(__file__).parent
templates = Jinja2Templates(directory=[
    BASE_DIR / "../public/templates",
])

def render_template(template_name: str, context: dict, factureId: int):
    template = templates.get_template(template_name)
    html_content = template.render(request=None, **context)

    filename = f"facture{factureId}.pdf"

    HTML(string=html_content).write_pdf(f"public/factures/{filename}")
    return filename
