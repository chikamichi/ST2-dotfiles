'''
Provides both a trailing spaces highlighter and deletion command.

In order to use the deletion feature, one must add the keymaps by hand
(this should go into "Key Bindings - User"):

  { "keys": ["ctrl+shift+t"], "command": "delete_trailing_spaces" }

One may also change the highlighting color, providing a scope name such
as "invalid", "comment"... in "File Settings - User":

  { "trailing_spaces_highlight_color": "invalid" }

Actually, "invalid" is the default value.

@author: Jean-Denis Vauguet <jd@vauguet.fr>, Oktay Acikalin <ok@ryotic.de>

@license: MIT (http://www.opensource.org/licenses/mit-license.php)

@since: 2011-02-25
'''

import sublime, sublime_plugin

DEFAULT_COLOR_SCOPE_NAME = "invalid"

# Return an array of regions matching trailing spaces.
def find_trailing_spaces(view):
    trails = view.find_all('[ \t]+$')
    regions = []
    for trail in trails:
      regions.append(trail)
    return regions

# Highlight matching regions.
class TrailingSpacesHighlightListener(sublime_plugin.EventListener):
    def on_modified(self, view):
        color_scope_name = view.settings().get('trailing_spaces_highlight_color',
                                               DEFAULT_COLOR_SCOPE_NAME)
        regions = find_trailing_spaces(view)
        view.add_regions('TrailingSpacesHighlightListener',
                         regions, color_scope_name,
                         sublime.DRAW_EMPTY)

# Allows to erase matching regions.
class DeleteTrailingSpacesCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        regions = find_trailing_spaces(self.view)

        if regions:
            # deleting a region changes the other regions positions, so we
            # handle this maintaining an offset
            offset = 0
            for region in regions:
                r = sublime.Region(region.a + offset, region.b + offset)
                self.view.erase(edit, sublime.Region(r.a, r.b))
                offset -= r.size()

            msg_parts = {"nbRegions": len(regions),
                         "plural":    's' if len(regions) > 1 else ''}
            msg = "Deleted %(nbRegions)s trailing spaces region%(plural)s" % msg_parts
        else:
            msg = "No trailing spaces to delete!"

        sublime.status_message(msg)
