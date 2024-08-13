from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.util.docutils import SphinxDirective


class ExerciseNode(nodes.Admonition, nodes.Element):
    pass


class ExerciseDirective(SphinxDirective):
    has_content = True
    optional_arguments = 1
    option_spec = {"class": directives.class_option}

    def run(self):
        docname = self.env.docname

        # Initialize or reset the counter for this document
        if not hasattr(self.env, "exercises_count"):
            self.env.exercises_count = {}
        if docname not in self.env.exercises_count:
            self.env.exercises_count[docname] = 0

        # Increment the exercise count for the current document
        self.env.exercises_count[docname] += 1
        exercise_number = self.env.exercises_count[docname]

        if not self.arguments:
            title_text = f"Exercise {exercise_number}"
        else:
            title_text = self.arguments[0]

        title_node = nodes.title(title_text, title_text)

        # Use nested_parse to correctly handle nested content
        node = nodes.container()
        self.state.nested_parse(self.content, self.content_offset, node)

        exercise_node = ExerciseNode()
        exercise_node += title_node
        exercise_node += node

        if "class" in self.options:
            exercise_node["classes"] += self.options["class"]
        exercise_node["classes"] += ["exercise"]

        return [exercise_node]


def visit_exercise_node(self, node):
    self.visit_admonition(node)


def depart_exercise_node(self, node):
    self.depart_admonition(node)


def setup(app):
    app.add_node(ExerciseNode, html=(visit_exercise_node, depart_exercise_node))
    app.add_directive("exercise", ExerciseDirective)
    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
