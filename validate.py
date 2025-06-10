import sys
from html.parser import HTMLParser

class HTMLValidator(HTMLParser):
    VOID_ELEMENTS = {
        'area','base','br','col','embed','hr','img','input','link','meta',
        'param','source','track','wbr'
    }

    def __init__(self):
        super().__init__()
        self.stack = []
        self.errors = []

    def handle_startendtag(self, tag, attrs):
        if tag not in self.VOID_ELEMENTS:
            # treat as a tag that opens and closes immediately
            return

    def handle_starttag(self, tag, attrs):
        if tag not in self.VOID_ELEMENTS:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if not self.stack or self.stack[-1] != tag:
            self.errors.append(f"Mismatched closing tag: {tag}")
        else:
            self.stack.pop()

    def close(self):
        super().close()
        if self.stack:
            self.errors.append(f"Unclosed tags: {', '.join(self.stack)}")


def validate_html(path):
    parser = HTMLValidator()
    with open(path, 'r', encoding='utf-8') as f:
        data = f.read()
    parser.feed(data)
    parser.close()
    if parser.errors:
        for err in parser.errors:
            print(f"HTML error: {err}")
        return False
    return True


def validate_css(path):
    stack = []
    with open(path, 'r', encoding='utf-8') as f:
        for lineno, line in enumerate(f, start=1):
            for ch in line:
                if ch == '{':
                    stack.append((lineno, ch))
                elif ch == '}':
                    if not stack:
                        print(f"CSS error: unmatched }} at line {lineno}")
                        return False
                    stack.pop()
    if stack:
        line, _ = stack[-1]
        print(f"CSS error: unmatched {{ at line {line}")
        return False
    return True


def main():
    html_ok = validate_html('index.html')
    css_ok = validate_css('style.css')
    if not (html_ok and css_ok):
        sys.exit(1)


if __name__ == '__main__':
    main()
