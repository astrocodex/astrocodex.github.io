from docutils import nodes
from docutils.parsers.rst import Directive, directives
from sphinx.util.docutils import SphinxDirective

class MetadataNode(nodes.General, nodes.Element):
    pass

def visit_metadata_node(self, node):
    self.body.append(self.starttag(node, 'div', CLASS='metadata'))

def depart_metadata_node(self, node):
    self.body.append('</div>')

class MetadataDirective(SphinxDirective):
    has_content = True
    option_spec = {
        'title': directives.unchanged,
        'author': directives.unchanged,
        'orcid': directives.unchanged,
        'affiliations': directives.unchanged,
    }

    def run(self):
        title = self.options.get('title', '')
        author = self.options.get('author', '')
        orcid = self.options.get('orcid', '')
        affiliations = self.options.get('affiliations', '')

        # Create the metadata node
        metadata_node = MetadataNode()

        # Add children nodes for each metadata field
        if title:
            title_node = nodes.title(text=title)
            metadata_node += title_node
        if author:
            author_node = nodes.paragraph(text=f"Author: {author}", classes=['author'])
            metadata_node += author_node
        if orcid:
            orcid_node = nodes.paragraph(text=f"ORCID: {orcid}", classes=['orcid'])
            metadata_node += orcid_node
        if affiliations:
            affiliations_node = nodes.paragraph(text=f"Affiliations: {affiliations}", classes=['affiliations'])
            metadata_node += affiliations_node

        # Add a horizontal rule to visually separate the metadata
        hr_node = nodes.raw('', '<hr>', format='html')
        metadata_node += hr_node

        return [metadata_node]

def setup(app):
    app.add_node(MetadataNode, html=(visit_metadata_node, depart_metadata_node))
    app.add_directive('metadata', MetadataDirective)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
