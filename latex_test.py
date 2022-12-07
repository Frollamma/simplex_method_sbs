from pylatex import Document, Section, Subsection, Command
from pylatex.utils import italic, NoEscape

doc = Document('basic')

doc.preamble.append(Command('title', 'Simplex method resolution'))
# doc.preamble.append(Command('author', 'Anonymous author'))
# doc.preamble.append(Command('date', NoEscape(r'\today')))
doc.append(NoEscape(r'\maketitle'))

doc.generate_pdf('solved.pdf', clean_tex=False)
doc.generate_tex()