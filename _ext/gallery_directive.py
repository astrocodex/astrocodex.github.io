import json
from pathlib import Path

from docutils import nodes
from sphinx.util.docutils import SphinxDirective


class GalleryDirective(SphinxDirective):
    has_content = True
    required_arguments = 1  # Path to the JSON file containing exercise data

    def run(self):
        print("Running GalleryDirective")
        json_path = self.resolve_path(self.arguments[0])
        print(f"Resolved JSON path: {json_path}")

        if not json_path.exists():
            raise self.error(f"JSON file not found: {json_path}")

        with json_path.open() as f:
            exercises = json.load(f)

        print(f"Loaded exercises: {exercises}")

        # Create the outer container
        gallery_node = nodes.container(classes=["gallery-container"])

        # Add search input
        search_node = nodes.container(classes=["gallery-search"])
        search_node += nodes.raw(
            "",
            '<input type="text" id="gallerySearch" placeholder="Search exercises..." class="form-control">',
            format="html",
        )
        gallery_node += search_node

        # Add filter buttons container
        filter_buttons_node = nodes.container(
            classes=["gallery-filters"], ids=["galleryFilters"]
        )
        gallery_node += filter_buttons_node

        # Add custom CSS for spacing and layout
        style_node = nodes.raw(
            "",
            """
<style>
    .gallery-search {
        margin-bottom: 20px;
    }
    .gallery-filters {
        margin-bottom: 20px;
    }
    .gallery-grid {
        margin-top: 20px;
        display: flex;
        flex-wrap: wrap;
        justify-content: space-around;
    }
    .gallery-grid .col {
        padding: 10px;
        flex: 0 1 calc(33.333% - 5px);
        box-sizing: border-box;
    }
    .gallery-grid .card {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        height: 100%;
        padding: 0px;
        text-decoration: none; /* Ensure no underline for the link */
        color: inherit; /* Inherit color to avoid link color */
        transition: box-shadow 0.3s ease-in-out;
    }
    .gallery-grid .card:hover {
        text-decoration: none; /* Remove hover underline */
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Add a drop shadow on hover */
    }
    .card-body {
        padding: 10px;
        flex-grow: 1; /* Ensure card body takes available space */
    }
    .card-title {
        margin-bottom: 10px;
        font-weight: bold;
        padding-left: 15px;
        padding-top: 15px;
        padding-right: 15px;
    }
    .card-description {
        padding-left: 15px;
        padding-right: 15px;
        margin-bottom: 10px;
        flex-grow: 1;
        display: -webkit-box;
        -webkit-line-clamp: 3;
        -webkit-box-orient: vertical;
        overflow: hidden;
        text-overflow: ellipsis;
        font-size: 0.7em;
    }
    .card-footer {
        padding-top: 2px;
        padding-bottom: 2px;
        padding-left: 5px;
        margin-top: auto; /* Ensure footer is pushed to the bottom */
        border-top: 1px solid #ddd;
        background-color: #f9f9f9;
    }
    .card-text {
        margin-left: 5px;
        padding: 5px 15px; /* Add padding to move tags inward */
        display: flex;
        flex-wrap: wrap;
        gap: 3px; /* Small gap between tags */
    }
    .card-text .badge {
        margin: 0px;
        margin-left: 5px;
        background-color: #737272; /* Set your desired background color */
        color: white; /* Set your desired text color */
    }
</style>
            """,
            format="html",
        )
        gallery_node += style_node

        # Add gallery grid
        grid_node = nodes.container(
            classes=[
                "gallery-grid",
                "row",
                "row-cols-1",
                "row-cols-md-2",
                "row-cols-lg-3",
                "g-4",
            ],
            ids=["galleryGrid"],
        )

        for exercise in exercises:
            url = self.resolve_url(exercise["url"])
            card_html = f"""
            <div class="col">
                <a href="{url}" class="card h-100">
                    <div class="card-body">
                        <p class="card-title">{exercise['title']}</p>
                        <p class="card-description">{exercise.get('description', '')}</p>
                    </div>
                    <div class="card-footer">
                        <div class="card-text">
                            {''.join(f'<span class="badge">{tag}</span>' for tag in exercise['tags'])}
                        </div>
                    </div>
                </a>
            </div>
            """
            card_node = nodes.raw("", card_html, format="html")
            grid_node += card_node

        gallery_node += grid_node

        # Add JavaScript for filtering and search
        js_node = nodes.raw("", self.get_javascript(), format="html")
        gallery_node += js_node

        return [gallery_node]

    def resolve_path(self, path):
        return Path(self.env.app.srcdir) / path

    def resolve_url(self, url):
        # If the url does not start with http or https, treat it as a relative path within the project
        if not url.startswith(("http://", "https://")):
            # Handle Jupyter Book style paths
            return f"{url}.html"
        return url

    def get_javascript(self):
        return """
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                const galleryGrid = document.getElementById('galleryGrid');
                const searchInput = document.getElementById('gallerySearch');
                const filterButtons = document.getElementById('galleryFilters');
                let activeFilters = new Set();

                // Create filter buttons
                const allTags = [...new Set([...galleryGrid.querySelectorAll('.badge')].map(badge => badge.textContent))];
                allTags.forEach(tag => {
                    const button = document.createElement('button');
                    button.className = 'filter-button btn btn-outline-primary me-2 mb-2';
                    button.textContent = tag;
                    button.onclick = () => toggleFilter(tag, button);
                    filterButtons.appendChild(button);
                });

                // Filter exercises based on search input and active filters
                function filterExercises() {
                    const searchTerm = searchInput.value.toLowerCase();
                    const cards = galleryGrid.children;
                    for (let card of cards) {
                        const title = card.querySelector('.card-title').textContent.toLowerCase();
                        const description = card.querySelector('.card-description').textContent.toLowerCase();
                        const tags = Array.from(card.querySelectorAll('.badge')).map(span => span.textContent.toLowerCase());
                        const matchesSearch = title.includes(searchTerm) || description.includes(searchTerm) || tags.some(tag => tag.includes(searchTerm));
                        const matchesFilters = activeFilters.size === 0 || tags.some(tag => activeFilters.has(tag));
                        card.style.display = matchesSearch && matchesFilters ? '' : 'none';
                    }
                }

                // Toggle filter
                function toggleFilter(tag, button) {
                    if (activeFilters.has(tag)) {
                        activeFilters.delete(tag);
                        button.classList.remove('active');
                    } else {
                        activeFilters.add(tag);
                        button.classList.add('active');
                    }
                    filterExercises();
                }

                // Initialize
                searchInput.addEventListener('input', filterExercises);
            });
        </script>
        """


def setup(app):
    print("Setting up GalleryDirective")
    app.add_directive("gallery", GalleryDirective)

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
