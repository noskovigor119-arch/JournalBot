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


def split_html_hybrid(text: str, max_chars: int = 4000) -> list[str]:
    """
    To be used for formatted strings
    Optimized Telegram Splitter:
    1. Tries to group text cleanly by double newlines (paragraphs).
    2. If a single paragraph/list block exceeds max_chars, it falls back
       to splitting THAT specific block by single newlines (lines).
    """
    if len(text) <= max_chars:
        return [text]

    chunks = []
    current_chunk = []
    current_length = 0

    # Phase 1: Try splitting by clean paragraph boundaries
    paragraphs = text.split("\n\n")

    for para in paragraphs:
        # +2 accounts for the '\n\n' we add back when joining
        para_len = len(para) + 2

        # CRITICAL FALLBACK: If a single paragraph/list is too massive for one message
        if para_len > max_chars:
            # 1. Flush whatever clean paragraphs we accumulated so far
            if current_chunk:
                chunks.append("\n\n".join(current_chunk))
                current_chunk = []
                current_length = 0

            # 2. Drop down to Phase 2: Split this specific monster block by lines
            lines = para.split("\n")
            for line in lines:
                line_len = len(line) + 1 # +1 for '\n'

                # Extreme safety case: If a single line is somehow > max_chars
                if line_len > max_chars:
                    sub_chunks = [line[i:i+max_chars] for i in range(0, len(line), max_chars)]
                    chunks.extend(sub_chunks)
                    continue

                if current_length + line_len > max_chars:
                    if current_chunk:
                        chunks.append("\n".join(current_chunk))
                    current_chunk = [line]
                    current_length = line_len
                else:
                    current_chunk.append(line)
                    current_length += line_len

            # Flush out the remaining line fragments from the fallback layer
            if current_chunk:
                chunks.append("\n".join(current_chunk))
                current_chunk = []
                current_length = 0

            continue # Move on to the next paragraph block

        # Normal Flow: Accumulate paragraphs cleanly
        if current_length + para_len > max_chars:
            if current_chunk:
                chunks.append("\n\n".join(current_chunk))
            current_chunk = [para]
            current_length = para_len
        else:
            current_chunk.append(para)
            current_length += para_len

    # Catch any remaining text lingering in the accumulator
    if current_chunk:
        chunks.append("\n\n".join(current_chunk))

    return chunks