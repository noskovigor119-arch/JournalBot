import re
import markdown

def format_for_telegram(raw_markdown: str) -> str:
    """
       Converts LLM-generated Markdown to Telegram-safe HTML.
       """
    # 1. Convert Markdown to basic HTML
    html_content = markdown.markdown(raw_markdown)

    # 2. Telegram strictly supports: <b>, <i>, <u>, <s>, <a>, <code>, <pre>, <tg-emoji>
    # The markdown library might output <ul>, <ol>, <li>, <h1>, <h2>, <br> <hr>.

    # We strip <hr> completely or replace with a visible separator if preferred
    html_content = re.sub(r'<hr\s*/?>', '\n---\n', html_content)
    # Strip <br> tags (optional, but often cleaner in Telegram messages)
    html_content = html_content.replace('<br>', '\n').replace('<br />', '\n')

    # Replace list tags with text-based bullets and newlines
    # This keeps it readable while staying compliant
    html_content = html_content.replace('<ul>', '').replace('</ul>', '')
    html_content = html_content.replace('<ol>', '').replace('</ol>', '')
    html_content = html_content.replace('<li>', '• ').replace('</li>', '\n')

    # Replace headers with bold+underline
    html_content = re.sub(r'<(h[1-6])>(.*?)</\1>', r'<b><u>\2</u></b>\n', html_content)

    # Replace <p> tags with double newlines
    html_content = html_content.replace('<p>', '').replace('</p>', '\n\n')

    return html_content